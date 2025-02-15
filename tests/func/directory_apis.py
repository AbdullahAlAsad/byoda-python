#!/usr/bin/env python3

'''
Test the Directory APIs

As these test cases are directly run against the web APIs, they mock
the headers that would normally be set by the reverse proxy

:maintainer : Steven Hessing <steven@byoda.org>
:copyright  : Copyright 2021, 2022
:license
'''

import sys
import os
import yaml
import orjson
import shutil
import asyncio
import unittest
import requests
from uuid import uuid4
from copy import copy

from cryptography import x509
from cryptography.hazmat.primitives import serialization

from multiprocessing import Process
import uvicorn

from byoda.datamodel.network import Network
from byoda.datamodel.schema import Schema

from byoda.servers.directory_server import DirectoryServer

from byoda.util.message_signature import SignatureType

from byoda.secrets import Secret
from byoda.secrets import AccountSecret
from byoda.secrets import ServiceCaSecret
from byoda.secrets import ServiceSecret
from byoda.secrets import ServiceDataSecret

from byoda.util.logger import Logger

from byoda import config

from byoda.util.fastapi import setup_api

from dirserver.routers import account as AccountRouter
from dirserver.routers import service as ServiceRouter
from dirserver.routers import member as MemberRouter

# Settings must match config.yml used by directory server
NETWORK = 'test.net'
DEFAULT_SCHEMA = 'tests/collateral/dummy-unsigned-service-schema.json'
SERVICE_ID = 12345678

CONFIG_FILE = 'tests/collateral/config.yml'
TEST_DIR = '/tmp/byoda-tests/dir_apis'
SERVICE_DIR = TEST_DIR + '/service'
TEST_PORT = 9000
BASE_URL = f'http://localhost:{TEST_PORT}/api'

_LOGGER = None


class TestDirectoryApis(unittest.IsolatedAsyncioTestCase):
    PROCESS = None
    APP_CONFIG = None

    async def asyncSetUp(self):
        Logger.getLogger(sys.argv[0], debug=True, json_out=False)

        with open(CONFIG_FILE) as file_desc:
            TestDirectoryApis.APP_CONFIG = yaml.load(
                file_desc, Loader=yaml.SafeLoader
            )

        app_config = TestDirectoryApis.APP_CONFIG
        app_config['dirserver']['root_dir'] = TEST_DIR
        try:
            shutil.rmtree(TEST_DIR)
        except FileNotFoundError:
            pass

        os.makedirs(TEST_DIR)
        os.makedirs(
            f'{SERVICE_DIR}/network-{app_config["application"]["network"]}'
            f'/services/service-{SERVICE_ID}'
        )

        network = await Network.create(
            app_config['application']['network'],
            app_config['dirserver']['root_dir'],
            app_config['dirserver']['private_key_password'],
        )

        config.server = DirectoryServer(network)
        await config.server.connect_db(app_config['dirserver']['dnsdb'])

        app = setup_api(
            'Byoda test dirserver', 'server for testing directory APIs',
            'v0.0.1', [], [AccountRouter, ServiceRouter, MemberRouter]
        )
        TestDirectoryApis.PROCESS = Process(
            target=uvicorn.run,
            args=(app,),
            kwargs={
                'host': '127.0.0.1',
                'port': TEST_PORT,
                'log_level': 'debug'
            },
            daemon=True
        )
        TestDirectoryApis.PROCESS.start()
        await asyncio.sleep(1)

    @classmethod
    async def asyncTearDown(cls):
        TestDirectoryApis.PROCESS.terminate()

    def test_network_account_put(self):
        API = BASE_URL + '/v1/network/account'

        uuid = uuid4()

        network_name = TestDirectoryApis.APP_CONFIG['application']['network']

        # PUT, with auth
        headers = {
            'X-Client-SSL-Verify': 'SUCCESS',
            'X-Client-SSL-Subject': f'CN={uuid}.accounts.{network_name}',
            'X-Client-SSL-Issuing-CA': f'CN=accounts-ca.{network_name}'
        }
        response = requests.put(API, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['ipv4_address'], '127.0.0.1')
        self.assertEqual(data['ipv6_address'], None)

    async def test_network_account_post(self):
        API = BASE_URL + '/v1/network/account'

        network = Network(
            TestDirectoryApis.APP_CONFIG['dirserver'],
            TestDirectoryApis.APP_CONFIG['application']
        )
        await network.load_network_secrets()

        uuid = uuid4()
        secret = AccountSecret(
            account='dir_api_test', account_id=uuid, network=network
        )
        csr = secret.create_csr()
        csr = csr.public_bytes(serialization.Encoding.PEM)
        fqdn = AccountSecret.create_commonname(uuid, network.name)
        headers = {
            'X-Client-SSL-Verify': 'SUCCESS',
            'X-Client-SSL-Subject': f'CN={fqdn}',
            'X-Client-SSL-Issuing-CA': f'CN=accounts-ca.{network.name}'
        }
        response = requests.post(
            API, json={'csr': str(csr, 'utf-8')}, headers=headers
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        issuing_ca_cert = x509.load_pem_x509_certificate(       # noqa:F841
            data['cert_chain'].encode()
        )
        account_cert = x509.load_pem_x509_certificate(          # noqa:F841
            data['signed_cert'].encode()
        )
        network_data_cert = x509.load_pem_x509_certificate(     # noqa:F841
            data['network_data_cert_chain'].encode()
        )

        # Retry same CSR, with same TLS client cert:
        response = requests.post(
            API, json={'csr': str(csr, 'utf-8')}, headers=headers
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        issuing_ca_cert = x509.load_pem_x509_certificate(       # noqa:F841
            data['cert_chain'].encode()
        )
        account_cert = x509.load_pem_x509_certificate(          # noqa:F841
            data['signed_cert'].encode()
        )
        network_data_cert = x509.load_pem_x509_certificate(     # noqa:F841
            data['network_data_cert_chain'].encode()
        )

        # Retry same CSR, without client cert:
        response = requests.post(
            API, json={'csr': str(csr, 'utf-8')}, headers=None
        )
        self.assertEqual(response.status_code, 401)

    async def test_network_service_creation(self):
        API = BASE_URL + '/v1/network/service'

        # We can not use deepcopy here so do two copies
        network = copy(config.server.network)
        network.paths = copy(config.server.network.paths)
        network.paths._root_directory = SERVICE_DIR
        if not await network.paths.secrets_directory_exists():
            await network.paths.create_secrets_directory()

        service_id = SERVICE_ID
        serviceca_secret = ServiceCaSecret(
            service='dir_api_test', service_id=service_id, network=network
        )
        csr = serviceca_secret.create_csr()
        csr = csr.public_bytes(serialization.Encoding.PEM)

        response = requests.post(
            API, json={'csr': str(csr, 'utf-8')}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        issuing_ca_cert = x509.load_pem_x509_certificate(       # noqa:F841
            data['cert_chain'].encode()
        )
        serviceca_cert = x509.load_pem_x509_certificate(        # noqa:F841
            data['signed_cert'].encode()
        )
        # TODO: populate a secret from a CertChain
        serviceca_secret.cert = serviceca_cert
        serviceca_secret.cert_chain = [issuing_ca_cert]
        network_data_cert = x509.load_pem_x509_certificate(     # noqa:F841
            data['network_data_cert_chain'].encode()
        )

        # Check that the service CA public cert was written to the network
        # directory of the dirserver
        testsecret = ServiceCaSecret(
            service='dir_api_test', service_id=service_id,
            network=config.server.network
        )
        await testsecret.load(with_private_key=False)

        service_secret = ServiceSecret('dir_api_test', service_id, network)
        service_csr = service_secret.create_csr()
        certchain = serviceca_secret.sign_csr(service_csr)
        service_secret.from_signed_cert(certchain)
        await service_secret.save()

        service_cn = Secret.extract_commonname(certchain.signed_cert)
        serviceca_cn = Secret.extract_commonname(serviceca_cert)

        # Create and register the the public cert of the data secret,
        # which the directory server needs to validate the service signature
        # of the schema for the service
        service_data_secret = ServiceDataSecret(
            'dir_api_test', service_id, network
        )
        service_data_csr = service_data_secret.create_csr()
        data_certchain = serviceca_secret.sign_csr(service_data_csr)
        service_data_secret.from_signed_cert(data_certchain)
        await service_data_secret.save()

        headers = {
            'X-Client-SSL-Verify': 'SUCCESS',
            'X-Client-SSL-Subject': f'CN={service_cn}',
            'X-Client-SSL-Issuing-CA': f'CN={serviceca_cn}'
        }

        data_certchain = service_data_secret.certchain_as_pem()

        response = requests.put(
            API + '/service_id/' + str(service_id), headers=headers,
            json={'certchain': data_certchain}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['ipv4_address'], '127.0.0.1')

        # Send the service schema
        with open(DEFAULT_SCHEMA) as file_desc:
            data = file_desc.read()
            schema_data = orjson.loads(data)

        schema_data['service_id'] = service_id
        schema_data['version'] = 1

        schema = Schema(schema_data)
        schema.create_signature(service_data_secret, SignatureType.SERVICE)

        headers = {
            'X-Client-SSL-Verify': 'SUCCESS',
            'X-Client-SSL-Subject': f'CN={service_cn}',
            'X-Client-SSL-Issuing-CA': f'CN={serviceca_cn}'
        }

        response = requests.patch(
            API + f'/service_id/{service_id}', headers=headers,
            json=schema.json_schema
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ACCEPTED')
        self.assertEqual(len(data['errors']), 0)

        # Get the fully-signed data contract for the service
        API = BASE_URL + '/v1/network/service'

        response = requests.get(API + f'/service_id/{service_id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)
        self.assertEqual(data['service_id'], SERVICE_ID)
        self.assertEqual(data['version'], 1)
        self.assertEqual(data['name'], 'dummyservice')
        self.assertEqual(len(data['signatures']), 2)
        schema = Schema(data)

        # Get the list of service summaries
        API = BASE_URL + '/v1/network/services'
        response = requests.get(API)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        service_summary = data['service_summaries'][0]
        self.assertEqual(service_summary['service_id'], SERVICE_ID)
        self.assertEqual(service_summary['version'], 1)
        self.assertEqual(service_summary['name'], 'dummyservice')

        # Now test membership registration against the directory server
        API = BASE_URL + '/v1/network/member'

        headers = {
            'X-Client-SSL-Verify': 'SUCCESS',
            'X-Client-SSL-Subject':
                f'CN={uuid4()}.members-{service_id}.{network.name}',
            'X-Client-SSL-Issuing-CA':
            f'CN=members-ca.members-ca-{service_id}.{network.name}'
        }

        response = requests.put(API, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['ipv4_address'], '127.0.0.1')


if __name__ == '__main__':
    _LOGGER = Logger.getLogger(sys.argv[0], debug=True, json_out=False)

    unittest.main()
