'''
Automatically generated code for GraphQL support for a Byoda service.
The code was generated by the 'generate_graphql_queries script'
using the 'podserver/files/grahphql_schema.jinja' template

:maintainer : Steven Hessing <steven@byoda.org>
:copyright  : Copyright 2021, 2022
:license    : GPLv3
'''

GRAPHQL_STATEMENTS = {}


QUERY_NETWORK_LINK = '''
query ($filters: networkLinkInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    network_link_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            network_link {
                timestamp
                member_id
                relation
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['network_link'] = {'query': QUERY_NETWORK_LINK}

MUTATE_NETWORK_LINK = '''
mutation(
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $relation: String,
) {
    mutate_network_link(
                    timestamp: $timestamp,
                    member_id: $member_id,
                    relation: $relation,
    ) {
                    timestamp
                    member_id
                    relation
    }
}
'''

GRAPHQL_STATEMENTS['network_link']['mutate'] = MUTATE_NETWORK_LINK


QUERY_NETWORK_INVITE = '''
query ($filters: networkInviteInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    network_invite_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            network_invite {
                timestamp
                member_id
                relation
                text
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['network_invite'] = {'query': QUERY_NETWORK_INVITE}

MUTATE_NETWORK_INVITE = '''
mutation(
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $relation: String,
                    $text: String,
) {
    mutate_network_invite(
                    timestamp: $timestamp,
                    member_id: $member_id,
                    relation: $relation,
                    text: $text,
    ) {
                    timestamp
                    member_id
                    relation
                    text
    }
}
'''

GRAPHQL_STATEMENTS['network_invite']['mutate'] = MUTATE_NETWORK_INVITE


QUERY_ASSET_LINK = '''
query ($filters: assetLinkInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    asset_link_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset_link {
                timestamp
                member_id
                asset_id
                asset_url
                relation
                nonce
                signature
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['asset_link'] = {'query': QUERY_ASSET_LINK}

MUTATE_ASSET_LINK = '''
mutation(
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $asset_id: UUID,
                    $asset_url: String,
                    $relation: String,
                    $nonce: String,
                    $signature: String,
) {
    mutate_asset_link(
                    timestamp: $timestamp,
                    member_id: $member_id,
                    asset_id: $asset_id,
                    asset_url: $asset_url,
                    relation: $relation,
                    nonce: $nonce,
                    signature: $signature,
    ) {
                    timestamp
                    member_id
                    asset_id
                    asset_url
                    relation
                    nonce
                    signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_link']['mutate'] = MUTATE_ASSET_LINK


QUERY_ASSET_REACTION = '''
query ($filters: assetReactionInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    asset_reaction_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset_reaction {
                timestamp
                member_id
                asset_id
                relation
                nonce
                signature
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['asset_reaction'] = {'query': QUERY_ASSET_REACTION}

MUTATE_ASSET_REACTION = '''
mutation(
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $asset_id: UUID,
                    $relation: String,
                    $nonce: String,
                    $signature: String,
) {
    mutate_asset_reaction(
                    timestamp: $timestamp,
                    member_id: $member_id,
                    asset_id: $asset_id,
                    relation: $relation,
                    nonce: $nonce,
                    signature: $signature,
    ) {
                    timestamp
                    member_id
                    asset_id
                    relation
                    nonce
                    signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_reaction']['mutate'] = MUTATE_ASSET_REACTION


QUERY_MEMBERLOG = '''
query ($filters: memberlogInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    memberlog_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            memberlog {
                timestamp
                remote_addr
                action
                message
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['memberlog'] = {'query': QUERY_MEMBERLOG}

MUTATE_MEMBERLOG = '''
mutation(
                    $timestamp: DateTime,
                    $remote_addr: String,
                    $action: String,
                    $message: String,
) {
    mutate_memberlog(
                    timestamp: $timestamp,
                    remote_addr: $remote_addr,
                    action: $action,
                    message: $message,
    ) {
                    timestamp
                    remote_addr
                    action
                    message
    }
}
'''

GRAPHQL_STATEMENTS['memberlog']['mutate'] = MUTATE_MEMBERLOG


QUERY_ASSET = '''
query ($filters: assetInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    asset_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset {
                timestamp
                asset_id
                asset_type
                locale
                creator
                created
                content_warnings
                copyright_years
                publisher
                title
                subject
                contents
                keywords
                forum
                response_to
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['asset'] = {'query': QUERY_ASSET}

MUTATE_ASSET = '''
mutation(
                    $timestamp: DateTime,
                    $asset_id: UUID,
                    $asset_type: String,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    mutate_asset(
                    timestamp: $timestamp,
                    asset_id: $asset_id,
                    asset_type: $asset_type,
                    locale: $locale,
                    creator: $creator,
                    created: $created,
                    content_warnings: $content_warnings,
                    copyright_years: $copyright_years,
                    publisher: $publisher,
                    title: $title,
                    subject: $subject,
                    contents: $contents,
                    keywords: $keywords,
                    forum: $forum,
                    response_to: $response_to,
    ) {
                    timestamp
                    asset_id
                    asset_type
                    locale
                    creator
                    created
                    content_warnings
                    copyright_years
                    publisher
                    title
                    subject
                    contents
                    keywords
                    forum
                    response_to
    }
}
'''

GRAPHQL_STATEMENTS['asset']['mutate'] = MUTATE_ASSET


QUERY_MEMBER = '''
query ($filters: memberInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    member_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            member {
                joined
                member_id
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['member'] = {'query': QUERY_MEMBER}

MUTATE_MEMBER = '''
mutation(
                    $joined: DateTime,
                    $member_id: UUID,
) {
    mutate_member(
                    joined: $joined,
                    member_id: $member_id,
    ) {
                    joined
                    member_id
    }
}
'''

GRAPHQL_STATEMENTS['member']['mutate'] = MUTATE_MEMBER


QUERY_PERSON = '''
query ($filters: personInputFilter, $first: Int, $after: String,
        $depth: Int, $relations: [String!]) {
    person_connection(
            filters: $filters, first: $first, after: $after, depth: $depth,
            relations: $relations) {
        total_count
        edges {
            cursor
            origin
            person {
                additional_names
                avatar_url
                email
                family_name
                given_name
                homepage_url
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['person'] = {'query': QUERY_PERSON}

MUTATE_PERSON = '''
mutation(
                    $additional_names: String,
                    $avatar_url: String,
                    $email: String,
                    $family_name: String,
                    $given_name: String,
                    $homepage_url: String,
) {
    mutate_person(
                    additional_names: $additional_names,
                    avatar_url: $avatar_url,
                    email: $email,
                    family_name: $family_name,
                    given_name: $given_name,
                    homepage_url: $homepage_url,
    ) {
                    additional_names
                    avatar_url
                    email
                    family_name
                    given_name
                    homepage_url
    }
}
'''

GRAPHQL_STATEMENTS['person']['mutate'] = MUTATE_PERSON


QUERY_NETWORK_LINKS = '''
query ($filters: networkLinkInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    network_links_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            network_link {
                timestamp
                member_id
                relation
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['network_links'] = {'query': QUERY_NETWORK_LINKS}

APPEND_NETWORK_LINKS = '''
mutation (
                    $timestamp: DateTime!,
                    $member_id: UUID!,
                    $relation: String!,
) {
    append_network_links (
            timestamp: $timestamp,
            member_id: $member_id,
            relation: $relation,
    ) {
            timestamp
            member_id
            relation
    }
}
'''

GRAPHQL_STATEMENTS['network_links']['append'] = APPEND_NETWORK_LINKS

UPDATE_NETWORK_LINKS = '''
mutation (
    $filters: networkLinkInputFilter!,
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $relation: String,
) {
    update_network_links(
        filters: $filters,
        timestamp: $timestamp,
        member_id: $member_id,
        relation: $relation,
    ) {
        timestamp
        member_id
        relation
    }
}
'''

GRAPHQL_STATEMENTS['network_links']['update'] = UPDATE_NETWORK_LINKS

DELETE_FROM_NETWORK_LINKS = '''
mutation ($filters: networkLinkInputFilter!) {
    delete_from_network_links(filters: $filters) {
        timestamp
        member_id
        relation
    }
}
'''

GRAPHQL_STATEMENTS['network_links']['delete'] = DELETE_FROM_NETWORK_LINKS

QUERY_NETWORK_INVITES = '''
query ($filters: networkInviteInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    network_invites_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            network_invite {
                timestamp
                member_id
                relation
                text
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['network_invites'] = {'query': QUERY_NETWORK_INVITES}

APPEND_NETWORK_INVITES = '''
mutation (
                    $timestamp: DateTime!,
                    $member_id: UUID!,
                    $relation: String!,
                    $text: String,
) {
    append_network_invites (
            timestamp: $timestamp,
            member_id: $member_id,
            relation: $relation,
            text: $text,
    ) {
            timestamp
            member_id
            relation
            text
    }
}
'''

GRAPHQL_STATEMENTS['network_invites']['append'] = APPEND_NETWORK_INVITES

UPDATE_NETWORK_INVITES = '''
mutation (
    $filters: networkInviteInputFilter!,
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $relation: String,
                    $text: String,
) {
    update_network_invites(
        filters: $filters,
        timestamp: $timestamp,
        member_id: $member_id,
        relation: $relation,
        text: $text,
    ) {
        timestamp
        member_id
        relation
        text
    }
}
'''

GRAPHQL_STATEMENTS['network_invites']['update'] = UPDATE_NETWORK_INVITES

DELETE_FROM_NETWORK_INVITES = '''
mutation ($filters: networkInviteInputFilter!) {
    delete_from_network_invites(filters: $filters) {
        timestamp
        member_id
        relation
        text
    }
}
'''

GRAPHQL_STATEMENTS['network_invites']['delete'] = DELETE_FROM_NETWORK_INVITES

QUERY_ASSET_LINKS = '''
query ($filters: assetLinkInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    asset_links_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset_link {
                timestamp
                member_id
                asset_id
                asset_url
                relation
                nonce
                signature
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['asset_links'] = {'query': QUERY_ASSET_LINKS}

APPEND_ASSET_LINKS = '''
mutation (
                    $timestamp: DateTime!,
                    $member_id: UUID!,
                    $asset_id: UUID,
                    $asset_url: String,
                    $relation: String!,
                    $nonce: String,
                    $signature: String,
) {
    append_asset_links (
            timestamp: $timestamp,
            member_id: $member_id,
            asset_id: $asset_id,
            asset_url: $asset_url,
            relation: $relation,
            nonce: $nonce,
            signature: $signature,
    ) {
            timestamp
            member_id
            asset_id
            asset_url
            relation
            nonce
            signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_links']['append'] = APPEND_ASSET_LINKS

UPDATE_ASSET_LINKS = '''
mutation (
    $filters: assetLinkInputFilter!,
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $asset_id: UUID,
                    $asset_url: String,
                    $relation: String,
                    $nonce: String,
                    $signature: String,
) {
    update_asset_links(
        filters: $filters,
        timestamp: $timestamp,
        member_id: $member_id,
        asset_id: $asset_id,
        asset_url: $asset_url,
        relation: $relation,
        nonce: $nonce,
        signature: $signature,
    ) {
        timestamp
        member_id
        asset_id
        asset_url
        relation
        nonce
        signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_links']['update'] = UPDATE_ASSET_LINKS

DELETE_FROM_ASSET_LINKS = '''
mutation ($filters: assetLinkInputFilter!) {
    delete_from_asset_links(filters: $filters) {
        timestamp
        member_id
        asset_id
        asset_url
        relation
        nonce
        signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_links']['delete'] = DELETE_FROM_ASSET_LINKS

QUERY_ASSET_REACTIONS_RECEIVED = '''
query ($filters: assetReactionInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    asset_reactions_received_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset_reaction {
                timestamp
                member_id
                asset_id
                relation
                nonce
                signature
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['asset_reactions_received'] = {'query': QUERY_ASSET_REACTIONS_RECEIVED}

APPEND_ASSET_REACTIONS_RECEIVED = '''
mutation (
                    $timestamp: DateTime!,
                    $member_id: UUID!,
                    $asset_id: UUID!,
                    $relation: String!,
                    $nonce: String,
                    $signature: String,
) {
    append_asset_reactions_received (
            timestamp: $timestamp,
            member_id: $member_id,
            asset_id: $asset_id,
            relation: $relation,
            nonce: $nonce,
            signature: $signature,
    ) {
            timestamp
            member_id
            asset_id
            relation
            nonce
            signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_reactions_received']['append'] = APPEND_ASSET_REACTIONS_RECEIVED

UPDATE_ASSET_REACTIONS_RECEIVED = '''
mutation (
    $filters: assetReactionInputFilter!,
                    $timestamp: DateTime,
                    $member_id: UUID,
                    $asset_id: UUID,
                    $relation: String,
                    $nonce: String,
                    $signature: String,
) {
    update_asset_reactions_received(
        filters: $filters,
        timestamp: $timestamp,
        member_id: $member_id,
        asset_id: $asset_id,
        relation: $relation,
        nonce: $nonce,
        signature: $signature,
    ) {
        timestamp
        member_id
        asset_id
        relation
        nonce
        signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_reactions_received']['update'] = UPDATE_ASSET_REACTIONS_RECEIVED

DELETE_FROM_ASSET_REACTIONS_RECEIVED = '''
mutation ($filters: assetReactionInputFilter!) {
    delete_from_asset_reactions_received(filters: $filters) {
        timestamp
        member_id
        asset_id
        relation
        nonce
        signature
    }
}
'''

GRAPHQL_STATEMENTS['asset_reactions_received']['delete'] = DELETE_FROM_ASSET_REACTIONS_RECEIVED

QUERY_MEMBERLOGS = '''
query ($filters: memberlogInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    memberlogs_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            memberlog {
                timestamp
                remote_addr
                action
                message
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['memberlogs'] = {'query': QUERY_MEMBERLOGS}

APPEND_MEMBERLOGS = '''
mutation (
                    $timestamp: DateTime!,
                    $remote_addr: String!,
                    $action: String!,
                    $message: String,
) {
    append_memberlogs (
            timestamp: $timestamp,
            remote_addr: $remote_addr,
            action: $action,
            message: $message,
    ) {
            timestamp
            remote_addr
            action
            message
    }
}
'''

GRAPHQL_STATEMENTS['memberlogs']['append'] = APPEND_MEMBERLOGS

UPDATE_MEMBERLOGS = '''
mutation (
    $filters: memberlogInputFilter!,
                    $timestamp: DateTime,
                    $remote_addr: String,
                    $action: String,
                    $message: String,
) {
    update_memberlogs(
        filters: $filters,
        timestamp: $timestamp,
        remote_addr: $remote_addr,
        action: $action,
        message: $message,
    ) {
        timestamp
        remote_addr
        action
        message
    }
}
'''

GRAPHQL_STATEMENTS['memberlogs']['update'] = UPDATE_MEMBERLOGS

DELETE_FROM_MEMBERLOGS = '''
mutation ($filters: memberlogInputFilter!) {
    delete_from_memberlogs(filters: $filters) {
        timestamp
        remote_addr
        action
        message
    }
}
'''

GRAPHQL_STATEMENTS['memberlogs']['delete'] = DELETE_FROM_MEMBERLOGS

QUERY_PUBLIC_ASSETS = '''
query ($filters: assetInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    public_assets_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset {
                timestamp
                asset_id
                asset_type
                locale
                creator
                created
                content_warnings
                copyright_years
                publisher
                title
                subject
                contents
                keywords
                forum
                response_to
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['public_assets'] = {'query': QUERY_PUBLIC_ASSETS}

APPEND_PUBLIC_ASSETS = '''
mutation (
                    $timestamp: DateTime!,
                    $asset_id: UUID!,
                    $asset_type: String!,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    append_public_assets (
            timestamp: $timestamp,
            asset_id: $asset_id,
            asset_type: $asset_type,
            locale: $locale,
            creator: $creator,
            created: $created,
            content_warnings: $content_warnings,
            copyright_years: $copyright_years,
            publisher: $publisher,
            title: $title,
            subject: $subject,
            contents: $contents,
            keywords: $keywords,
            forum: $forum,
            response_to: $response_to,
    ) {
            timestamp
            asset_id
            asset_type
            locale
            creator
            created
            content_warnings
            copyright_years
            publisher
            title
            subject
            contents
            keywords
            forum
            response_to
    }
}
'''

GRAPHQL_STATEMENTS['public_assets']['append'] = APPEND_PUBLIC_ASSETS

UPDATE_PUBLIC_ASSETS = '''
mutation (
    $filters: assetInputFilter!,
                    $timestamp: DateTime,
                    $asset_id: UUID,
                    $asset_type: String,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    update_public_assets(
        filters: $filters,
        timestamp: $timestamp,
        asset_id: $asset_id,
        asset_type: $asset_type,
        locale: $locale,
        creator: $creator,
        created: $created,
        content_warnings: $content_warnings,
        copyright_years: $copyright_years,
        publisher: $publisher,
        title: $title,
        subject: $subject,
        contents: $contents,
        keywords: $keywords,
        forum: $forum,
        response_to: $response_to,
    ) {
        timestamp
        asset_id
        asset_type
        locale
        creator
        created
        content_warnings
        copyright_years
        publisher
        title
        subject
        contents
        keywords
        forum
        response_to
    }
}
'''

GRAPHQL_STATEMENTS['public_assets']['update'] = UPDATE_PUBLIC_ASSETS

DELETE_FROM_PUBLIC_ASSETS = '''
mutation ($filters: assetInputFilter!) {
    delete_from_public_assets(filters: $filters) {
        timestamp
        asset_id
        asset_type
        locale
        creator
        created
        content_warnings
        copyright_years
        publisher
        title
        subject
        contents
        keywords
        forum
        response_to
    }
}
'''

GRAPHQL_STATEMENTS['public_assets']['delete'] = DELETE_FROM_PUBLIC_ASSETS

QUERY_SERVICE_ASSETS = '''
query ($filters: assetInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    service_assets_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset {
                timestamp
                asset_id
                asset_type
                locale
                creator
                created
                content_warnings
                copyright_years
                publisher
                title
                subject
                contents
                keywords
                forum
                response_to
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['service_assets'] = {'query': QUERY_SERVICE_ASSETS}

APPEND_SERVICE_ASSETS = '''
mutation (
                    $timestamp: DateTime!,
                    $asset_id: UUID!,
                    $asset_type: String!,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    append_service_assets (
            timestamp: $timestamp,
            asset_id: $asset_id,
            asset_type: $asset_type,
            locale: $locale,
            creator: $creator,
            created: $created,
            content_warnings: $content_warnings,
            copyright_years: $copyright_years,
            publisher: $publisher,
            title: $title,
            subject: $subject,
            contents: $contents,
            keywords: $keywords,
            forum: $forum,
            response_to: $response_to,
    ) {
            timestamp
            asset_id
            asset_type
            locale
            creator
            created
            content_warnings
            copyright_years
            publisher
            title
            subject
            contents
            keywords
            forum
            response_to
    }
}
'''

GRAPHQL_STATEMENTS['service_assets']['append'] = APPEND_SERVICE_ASSETS

UPDATE_SERVICE_ASSETS = '''
mutation (
    $filters: assetInputFilter!,
                    $timestamp: DateTime,
                    $asset_id: UUID,
                    $asset_type: String,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    update_service_assets(
        filters: $filters,
        timestamp: $timestamp,
        asset_id: $asset_id,
        asset_type: $asset_type,
        locale: $locale,
        creator: $creator,
        created: $created,
        content_warnings: $content_warnings,
        copyright_years: $copyright_years,
        publisher: $publisher,
        title: $title,
        subject: $subject,
        contents: $contents,
        keywords: $keywords,
        forum: $forum,
        response_to: $response_to,
    ) {
        timestamp
        asset_id
        asset_type
        locale
        creator
        created
        content_warnings
        copyright_years
        publisher
        title
        subject
        contents
        keywords
        forum
        response_to
    }
}
'''

GRAPHQL_STATEMENTS['service_assets']['update'] = UPDATE_SERVICE_ASSETS

DELETE_FROM_SERVICE_ASSETS = '''
mutation ($filters: assetInputFilter!) {
    delete_from_service_assets(filters: $filters) {
        timestamp
        asset_id
        asset_type
        locale
        creator
        created
        content_warnings
        copyright_years
        publisher
        title
        subject
        contents
        keywords
        forum
        response_to
    }
}
'''

GRAPHQL_STATEMENTS['service_assets']['delete'] = DELETE_FROM_SERVICE_ASSETS

QUERY_NETWORK_ASSETS = '''
query ($filters: assetInputFilter,
        $first: Int, $after: String, $depth: Int, $relations: [String!]) {
    network_assets_connection(filters: $filters, first: $first, after: $after,
    depth: $depth, relations: $relations) {
        total_count
        edges {
            cursor
            origin
            asset {
                timestamp
                asset_id
                asset_type
                locale
                creator
                created
                content_warnings
                copyright_years
                publisher
                title
                subject
                contents
                keywords
                forum
                response_to
            }
        }
        page_info {
            end_cursor
            has_next_page
        }
    }
}
'''

GRAPHQL_STATEMENTS['network_assets'] = {'query': QUERY_NETWORK_ASSETS}

APPEND_NETWORK_ASSETS = '''
mutation (
                    $timestamp: DateTime!,
                    $asset_id: UUID!,
                    $asset_type: String!,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    append_network_assets (
            timestamp: $timestamp,
            asset_id: $asset_id,
            asset_type: $asset_type,
            locale: $locale,
            creator: $creator,
            created: $created,
            content_warnings: $content_warnings,
            copyright_years: $copyright_years,
            publisher: $publisher,
            title: $title,
            subject: $subject,
            contents: $contents,
            keywords: $keywords,
            forum: $forum,
            response_to: $response_to,
    ) {
            timestamp
            asset_id
            asset_type
            locale
            creator
            created
            content_warnings
            copyright_years
            publisher
            title
            subject
            contents
            keywords
            forum
            response_to
    }
}
'''

GRAPHQL_STATEMENTS['network_assets']['append'] = APPEND_NETWORK_ASSETS

UPDATE_NETWORK_ASSETS = '''
mutation (
    $filters: assetInputFilter!,
                    $timestamp: DateTime,
                    $asset_id: UUID,
                    $asset_type: String,
                    $locale: String,
                    $creator: String,
                    $created: DateTime,
                    $content_warnings: [String!],
                    $copyright_years: [Int!],
                    $publisher: String,
                    $title: String,
                    $subject: String,
                    $contents: String,
                    $keywords: [String!],
                    $forum: String,
                    $response_to: UUID,
) {
    update_network_assets(
        filters: $filters,
        timestamp: $timestamp,
        asset_id: $asset_id,
        asset_type: $asset_type,
        locale: $locale,
        creator: $creator,
        created: $created,
        content_warnings: $content_warnings,
        copyright_years: $copyright_years,
        publisher: $publisher,
        title: $title,
        subject: $subject,
        contents: $contents,
        keywords: $keywords,
        forum: $forum,
        response_to: $response_to,
    ) {
        timestamp
        asset_id
        asset_type
        locale
        creator
        created
        content_warnings
        copyright_years
        publisher
        title
        subject
        contents
        keywords
        forum
        response_to
    }
}
'''

GRAPHQL_STATEMENTS['network_assets']['update'] = UPDATE_NETWORK_ASSETS

DELETE_FROM_NETWORK_ASSETS = '''
mutation ($filters: assetInputFilter!) {
    delete_from_network_assets(filters: $filters) {
        timestamp
        asset_id
        asset_type
        locale
        creator
        created
        content_warnings
        copyright_years
        publisher
        title
        subject
        contents
        keywords
        forum
        response_to
    }
}
'''

GRAPHQL_STATEMENTS['network_assets']['delete'] = DELETE_FROM_NETWORK_ASSETS
