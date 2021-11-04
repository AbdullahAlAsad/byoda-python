'''
Class ServiceServer derived from Server class for modelling
a server that hosts a BYODA Service

:maintainer : Steven Hessing <steven@byoda.org>
:copyright  : Copyright 2021
:license    : GPLv3
'''

import logging
from typing import TypeVar

from byoda.util import Paths
from byoda import config
from byoda.util.api_client import RestApiClient

from .server import Server
from .server import ServerType


_LOGGER = logging.getLogger(__name__)

Network = TypeVar('Network')
RegistrationStatus = TypeVar('RegistrationStatus')


class PodServer(Server):
    def __init__(self):
        super().__init__()

        self.server_type = ServerType.Pod
        self.service_summaries = None

    def load_secrets(self, password: str = None):
        '''
        Loads the secrets used by the podserver
        '''
        self.account.load_secrets()

        # We use the account secret as client TLS cert for outbound
        # requests and as private key for the TLS server
        filepath = self.account.tls_secret.save_tmp_private_key()

        config.requests.cert = (
            self.account.tls_secret.cert_file, filepath
        )

    def get_registered_services(self):
        '''
        Downloads a list of service summaries
        '''

        network = self.network

        url = network.paths.get(Paths.NETWORKSERVICES_API)
        response = RestApiClient.call(url)

        if response.status_code == 200:
            self.service_summaries = response.json()
            _LOGGER.debug(
                f'Read summaries for {len(self.service_summaries)} services'
            )
        else:
            _LOGGER.debug(
                'Failed to retrieve list of services from the network: '
                f'HTTP {response.status_code}'
            )

    def load_joined_services(self, network):
        '''
        Load the services that the account for the pod has joined
        '''

        self.network = network

        folders = network.paths.storage_driver.get_folders(
            Paths.SERVICES_DIR
        )
        for folder in [f for f in folders if f.startswith('service-')]:
            service_id = folder.split('-')[-1]

            service = network.add_service(
                service_id, RegistrationStatus.SchemaSigned
            )

            service_file = self.network.paths.get(
                Paths.SERVICE_FILE, service_id=service_id
            )

            try:
                service.load_schema(service_file)
            except (ValueError, RuntimeError, OSError) as exc:
                _LOGGER.exception(
                    f'Failed to load service from {service_file}: {exc}'
                )