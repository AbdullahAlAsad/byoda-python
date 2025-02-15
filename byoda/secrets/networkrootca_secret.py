'''
Cert manipulation of network secrets: root CA, accounts CA and services CA

:maintainer : Steven Hessing <steven@byoda.org>
:copyright  : Copyright 2021, 2022
:license    : GPLv3
'''

import os
import logging
from copy import copy

from cryptography.hazmat.primitives import serialization

from byoda.util.paths import Paths

from byoda.datatypes import CsrSource, EntityId
from byoda.datatypes import IdType

from byoda.storage.filestorage import FileStorage
from byoda.storage.filestorage import FileMode

from .secret import CSR
from .ca_secret import CaSecret

_LOGGER = logging.getLogger(__name__)


class NetworkRootCaSecret(CaSecret):
    ACCEPTED_CSRS = [
        IdType.ACCOUNTS_CA, IdType.SERVICES_CA, IdType.NETWORK_DATA
    ]

    def __init__(self, paths: Paths = None, network: str = None):
        '''
        Class for the network root CA secret. Either paths or network
        parameters must be provided. If paths parameter is not provided,
        the cert_file and private_key_file attributes of the instance must
        be set before the save() or load() members are called
        :param paths: instance of Paths class defining the directory structure
        and file names of a BYODA network
        :param paths: object containing all the file paths for the network. If
        this parameter has a value then the 'network' parameter must be None
        :param network: name of the network. If this parameter has a value then
        the 'paths' parameter must be None
        :returns: ValueError if both 'paths' and 'network' parameters are
        specified
        :raises: (none)
        '''

        if paths and network:
            raise ValueError('Either paths or network parameters must be set')

        if paths:
            self.paths = copy(paths)
            self.network = paths.network
            super().__init__(
                cert_file=self.paths.get(Paths.NETWORK_ROOT_CA_CERT_FILE),
                key_file=self.paths.get(Paths.NETWORK_ROOT_CA_KEY_FILE),
                storage_driver=self.paths.storage_driver
            )
        else:
            super().__init__()
            self.network = network
            self.paths = None

        # X.509 constraints
        self.ca: bool = True
        self.max_path_length: int = 3

        self.is_root_cert = True
        self.signs_ca_certs = True
        self.accepted_csrs = NetworkRootCaSecret.ACCEPTED_CSRS

    def create(self, expire: int = 10950):
        '''
        Creates an RSA private key and X.509 cert

        :param int expire: days after which the cert should expire
        :returns: (none)
        :raises: ValueError if the Secret instance already
                            has a private key or cert

        '''

        common_name = f'root-ca.{self.network}'
        super().create(common_name, expire=expire, key_size=4096, ca=self.ca)

    def create_csr(self):
        raise NotImplementedError

    def review_commonname(self, commonname: str) -> str:
        '''
        Checks if the structure of common name matches with a common name of
        an root CA Secret.

        :param commonname: the commonname to check
        :returns: the common name with the network domain stripped off
        :raises: ValueError if the commonname is not valid for this class
        '''

        # TODO: SECURITY: add constraints

        # Checks on commonname type and the network postfix
        entity_id = super().review_commonname(
            commonname, uuid_identifier=False, check_service_id=False
        )

        return entity_id

    @staticmethod
    def review_commonname_by_parameters(commonname: str, network: str
                                        ) -> str:
        '''
        Review the commonname for the specified network. Allows CNs to be
        reviewed without instantiating a class instance.

        :param commonname: the CN to check
        :raises: ValueError if the commonname is not valid for certs signed
        by instances of this class        '''

        entity_id = CaSecret.review_commonname_by_parameters(
            commonname, network, NetworkRootCaSecret.ACCEPTED_CSRS,
            uuid_identifier=False, check_service_id=False
        )

        return entity_id

    def review_csr(self, csr: CSR, source: CsrSource = CsrSource.WEBAPI
                   ) -> EntityId:
        '''
        Review a CSR. CSRs from NetworkAccountCA and NetworkServicesCA are
        permissable.

        :param csr: cryptography.X509.CertificateSigningRequest
        :param source: source of the CSR
        :returns: entity_id for the common name in the CSR
        :raises: ValueError if this object is not a CA because it only has
        access to the cert and not the private_key) or if the CommonName is
        not valid in the CSR for signature by this CA
        '''

        if not self.private_key_file:
            _LOGGER.exception('CSR received while we are not a CA')
            raise ValueError('CSR received while we are not a CA')

        if source == CsrSource.WEBAPI:
            raise ValueError(
                'This CA does not accept CSRs received via API call'
            )

        common_name = super().review_csr(csr)

        entity_id = self.review_commonname(common_name)

        return entity_id

    async def save(self, password: str = 'byoda', overwrite: bool = False,
                   storage_driver: FileStorage = None):
        '''
        Save a cert and private key to their respective files

        :param password: password to decrypt the private_key
        :param overwrite: should any existing files be overwritten
        :param storage_driver: the storage driver to use
        :returns: (none)
        :raises: PermissionError if the file for the cert and/or key
        already exist and overwrite == False
        '''

        if not storage_driver:
            storage_driver = self.storage_driver

        if not overwrite and await storage_driver.exists(self.cert_file):
            raise PermissionError(
                f'Can not save cert because the certificate '
                f'already exists at {self.cert_file}'
            )
        if (not overwrite and self.private_key
                and await storage_driver.exists(self.private_key_file)):
            raise PermissionError(
                f'Can not save the private key because the key already '
                f'exists at {self.private_key_file}'
            )

        _LOGGER.debug('Saving cert to %s', self.cert_file)
        data = self.cert_as_pem()

        directory = os.path.dirname(self.cert_file)
        await storage_driver.create_directory(directory)

        await storage_driver.write(
            self.cert_file, data, file_mode=FileMode.BINARY
        )

        if self.private_key:
            _LOGGER.debug('Saving private key to %s', self.private_key_file)
            private_key_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(
                    str.encode(password)
                )
            )

            await storage_driver.write(
                self.private_key_file, private_key_pem,
                file_mode=FileMode.BINARY
            )