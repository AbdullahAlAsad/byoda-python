'''
Cert manipulation of network secrets: root CA, accounts CA and services CA

:maintainer : Steven Hessing <stevenhessing@live.com>
:copyright  : Copyright 2021
:license    : GPLv3
'''

import logging


from byoda.util import Paths

from . import Secret, CsrSource, CSR

_LOGGER = logging.getLogger(__name__)


class NetworkRootCaSecret(Secret):
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
            self.network = paths.network
            super().__init__(
                cert_file=paths.get(Paths.NETWORK_ROOT_CA_CERT_FILE),
                key_file=paths.get(Paths.NETWORK_ROOT_CA_KEY_FILE)
            )
        else:
            super().__init__()
            self.network = network

        self.ca = True
        self.issuing_ca = None
        self.csrs_accepted_for = (
            'accounts-ca', 'services-ca'
        )

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

        # Checks on commonname type and the network postfix
        commonname_prefix = super().review_commonname(commonname)

        if commonname_prefix not in self.csrs_accepted_for:
            raise ValueError(
                f'A root CA does not sign CSRs for commonname {commonname}'
            )

        return commonname_prefix

    def review_csr(self, csr: CSR, source: CsrSource = CsrSource.WEBAPI
                   ) -> str:
        '''
        Review a CSR. CSRs from NetworkAccountCA and NetworkServicesCA are
        permissable.

        :param csr: cryptography.X509.CertificateSigningRequest
        :param source: source of the CSR
        :returns: 'accounts-ca' or 'services-ca'
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

        common_name_prefix = super().review_csr(csr)

        if common_name_prefix not in self.csrs_accepted_for:
            _LOGGER.warning(
                f'Common name prefix {common_name_prefix} does not match one '
                f'of: {", ".join(self.csrs_accepted_for)}'
            )

        return common_name_prefix
