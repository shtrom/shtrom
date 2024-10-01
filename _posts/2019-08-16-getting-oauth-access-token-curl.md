---
id: 447
title: 'Getting an OAuth access token with cURL'
date: '2019-08-16T12:37:55+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=447'
permalink: /2019/08/16/getting-oauth-access-token-curl/
iawp_total_views:
    - '10'
categories:
    - code
    - oneliner
    - tip
tags:
    - cURL
    - JMESPath
    - jp
    - jq
    - JSON
    - OAuth
    - standard
---

<div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow"><div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow">Sometimes, one just needs an OAuth access token (for the [client credential authentication flow](https://tools.ietf.org/html/rfc6749#section-4.4)).

</div></div></div></div><div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow">```
export ACCESS_TOKEN=$(curl -X POST \
 --user "${CLIENT_ID}:${CLIENT_SECRET}" \
 --data-urlencode "grant_type=client_credentials" \
 --data-urlencode "scope=${SCOPE}" \
 ${TOKEN_URL} \
 | jp -u access_token)
```

</div></div>Note: [`jp` is a handy CLI tool which allows to query JSON data](https://github.com/jmespath/jp) using the [JMESPath language](http://jmespath.org/) (the same that [awscli](https://docs.aws.amazon.com/cli/latest/reference/) uses in its `--query` parameter). It’s kinda like [`jq`](https://stedolan.github.io/jq/) but with a standardised language but, sadly, not colours.

The token can then be used in subsequent requests by adding it to an `Authorization: Bearer` header.

```
```
curl --header "Authorization: Bearer ${ACCESS_TOKEN}" ${ENDPOINT_URL} 
```...
```

<div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow"><div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow">**EDIT 2021-01-06**: The original version of this post suggested to put the `client_id` and `client_secret` in the POST data, [but this is NOT RECOMMENDED](https://tools.ietf.org/html/rfc6749#section-2.3.1). The recommended version is now presented at the top, and the previous one is kept below for reference. An example of how to use the token has also been added.

</div></div></div></div>```
export ACCESS_TOKEN=$(curl -X POST \
 --data-urlencode "grant_type=client_credentials" \
 --data-urlencode "client_id=${CLIENT_ID}" \
 --data-urlencode "client_secret=${CLIENT_SECRET}" \
 --data-urlencode "scope=${SCOPE}" \
 ${TOKEN_URL} \
 | jp -u access_token)
```