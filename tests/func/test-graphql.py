#!/usr/bin/env python3

'''
Test the GraphQL API

As these test cases are directly run against the GraphQL APIs, they mock
the headers that would normally be set by the reverse proxy

:maintainer : Steven Hessing <steven@byoda.org>
:copyright  : Copyright 2021
:license
'''

import sys
import unittest

from gql import Client
from gql import gql
from gql.transport.requests import RequestsHTTPTransport
# this is for GQL 3.x
# from gql.transport.aiohttp import AIOHTTPTransport

from byoda.util.logger import Logger
from byoda.config import DEFAULT_NETWORK

NETWORK = DEFAULT_NETWORK
BASE_URL = 'http://localhost:8001/api'

uuid = '3ceae39e-e4aa-4975-94a2-6ac8654c577c'
service_id = 0

TRANSPORT = RequestsHTTPTransport(
    url=BASE_URL + '/v1/data/service-0',
    timeout=300,
    use_json=True,
    headers={
        'X-Client-SSL-Verify': 'SUCCESS',
        'X-Client-SSL-Subject': f'CN={uuid}.members-{service_id}.{NETWORK}',
        'X-Client-SSL-Issuing-CA': f'CN=members-ca.{NETWORK}'
    }
)


class TestGraphQL(unittest.TestCase):
    def test_member_get(self):
        # Create a GraphQL client using the defined transport
        client = Client(
            transport=TRANSPORT, fetch_schema_from_transport=True,
        )
        query = gql(
            '''
                query {
                    person {
                        givenName
                        additionalNames
                        familyName
                        email
                        homepageUrl
                        avatarUrl
                    }
                }
            '''
        )
        result = client.execute(query)
        self.assertEqual(result['person']['givenName'], 'Steven')

        query = gql(
            '''
                mutation Mutation {
                    mutatePerson(
                        givenName: "Peter",
                        additionalNames: "",
                        familyName: "Hessing",
                        email: "steven@byoda.org",
                        homepageUrl: "https://some.place/",
                        avatarUrl: "https://some.place/avatar"
                    ) {
                        person {
                            givenName
                            additionalNames
                            familyName
                            email
                            homepageUrl
                            avatarUrl
                        }
                    }
                }
            '''
        )
        result = client.execute(query)
        self.assertEqual(
            result['mutatePerson']['person']['givenName'], 'Peter'
        )

        query = gql(
            '''
                mutation Mutation {
                    mutatePerson(
                        givenName: "Steven",
                        additionalNames: "",
                        familyName: "Hessing",
                        email: "steven@byoda.org",
                        homepageUrl: "https://some.place/",
                        avatarUrl: "https://some.place/avatar"
                    ) {
                        person {
                            givenName
                            additionalNames
                            familyName
                            email
                            homepageUrl
                            avatarUrl
                        }
                    }
                }
            '''
        )

        result = client.execute(query)
        self.assertEqual(
            result['mutatePerson']['person']['givenName'], 'Steven'
        )
        query = gql(
            '''
                mutation Mutation {
                    mutateMember(
                        memberId: "0",
                        joined: "2021-09-19T09:04:00+07:00"
                    ) {
                        member {
                            memberId
                        }
                    }
                }
            '''
        )
        result = client.execute(query)
        self.assertEqual(
            result['mutateMember']['member']['memberId'], '0'
        )


if __name__ == '__main__':
    _LOGGER = Logger.getLogger(sys.argv[0], debug=True, json_out=False)

    unittest.main()