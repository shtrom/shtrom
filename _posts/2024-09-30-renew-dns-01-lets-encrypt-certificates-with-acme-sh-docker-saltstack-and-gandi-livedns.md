---
id: 590
title: 'Renew DNS-01 Let&#8217;s Encrypt certificates with Acme.sh, Docker, SaltStack and Gandi LiveDNS'
date: '2024-09-30T22:37:39+10:00'
author: 'Olivier Mehani'
excerpt: 'The HTTP-based challenge to issue LetsEncrypt certificates can''t be used for internal or non-HTTP servers. This post describes the use of acme.sh in Docker to issue and renew certificates over DNS via SaltStack.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=590'
permalink: /2024/09/30/renew-dns-01-lets-encrypt-certificates-with-acme-sh-docker-saltstack-and-gandi-livedns/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '3'
categories:
    - engineering
    - security
    - sysadmin
    - tip
tags:
    - Acme.sh
    - Docker
    - 'Gandi LiveDNS'
    - 'Let''s Encrypt'
    - PGP
    - SaltStack
---

After hearing about [the LinkedIn incident (on DarkNet Diaries)](https://darknetdiaries.com/episode/86/), I decided to be a bit more mindful about the traffic to and within my home network, where I self-host a bunch of services. As this limited outside traffic coming in, I was faced with the problem of maintaining valid TLS certificates on internal servers.

Up to then I had been using [HTTP-01 challenge ](https://letsencrypt.org/docs/challenge-types/#http-01-challenge)with [Let’s Encrypt](https://letsencrypt.org/) to automatically renew the certificates ([including on the FRITZ!Box](https://blog.narf.ssji.net/2017/07/17/using-lets-encrypt-certificates-with-a-fritzbox/ "Using Let’s Encrypt certificates with a FRITZ!Box")). However this requires the server to validate to be reachable publicly, so I was out of luck. The other method is the [DNS-01 challenge](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge), which instead relies on the presence of an `_acme-challenge` `TXT` record in the target DNS zone for validation.

This generally requires some interaction with a remote DNS server or their APIs. The default ACME client, [Certbot](https://certbot.eff.org/), supports a number of registrars and DNS hosts but, crucially, not Gandi, which is what I am (still) using. So I had to find a different client, and rope it into my setup so the certificates would get renewed in a timely fashion.

tl;dr:

- I used [acme.sh](https://github.com/acmesh-official/acme.sh), a POSIX shell implementation of the ACME protocol, with support for Gandi LiveDNS API;
- I included the setup in my [SaltStack](https://saltproject.io/) states, with the use of the [`onfail` requisite](https://docs.saltproject.io/en/latest/ref/states/requisites.html#onfail), to only renew certificates about to expire;
- For good measure, I did the whole thing in containers, because why not?

# Accepting challenges for all domains

While [Certbot supports some DNS APIs](https://github.com/certbot/certbot), [acme.sh supports substantially more](https://github.com/acmesh-official/acme.sh/tree/master/dnsapi). It has a relatively straight-forward CLI interface. To issue a certificate with Gandi LiveDNS, the command would essentially look as follows.

```
GANDI_LIVEDNS_KEY=xxx acme.sh --issue -m <email> \
                              --server letsencrypt \
                              --dns dns_gandi_livedns \
                              -d '<domain>' [...]
```

## DNS aliasing

One additional problem I had is that some of the domains for which I wanted to issue certificates are sub-domains in zones I don’t control. Fortunately, `acme.sh` also supports the use of [DNS aliases](https://github.com/acmesh-official/acme.sh/wiki/DNS-alias-mode). The target subdomain can set a static CNAME for the `_acme-challenge` to point to the same record of another domain, which can be used as the challenge instead. This information can be passed via the client with the `--challenge-alias` option.

```
-d 'example.com' --challenge-alias 'exampleCom.example.net'
```

# Configuration automation

As [previously hinted](https://blog.narf.ssji.net/2023/12/28/saltstack-maps-as-objects/ "SaltStack maps as objects"), I use [SaltStack](https://saltproject.io/) to manage the configuration of my systems. It seemed natural to add support for certificate issuance to the existing states. Based on declarative configuration in the pillar, I can finely control the final state of the system.

{% raw %}
```
#!jinja|yaml|gpg

{% import_text "secrets/gandi_api_key.gpg" as gandi_api_key %}

acme:
  certificates:
    example.com:
      email: 'root@example.com'
      acmesh_server: letsencrypt
      acmesh_dns01_dns: dns_gandi_livedns
      acmesh_dns01_env:
        GANDI_LIVEDNS_KEY: {{ gandi_api_key|yaml_encode }}
      dns01_domains:
        - domain: example.com
          alias: exampleCom.example.net
```
{% endraw %}

With a pillar structured this way, it becomes easy to generate new certificates on a whim, simply by adding additional entries in the `certificates` dict. As an added bonus, note how the API key is imported from an encrypted file using the [GPG renderer](https://docs.saltproject.io/en/latest/ref/renderers/all/salt.renderers.gpg.html); the `yaml_encode` seems necessary for proper rendering of the file.

To process this, a state file is in charge of executing the command for each of the defined domain. As [a docker image for `acme.sh` is available](https://hub.docker.com/r/neilpang/acme.sh), I decided to use it for simplicity, rather than having to manually install the script locally.

{% raw %}
```
 
{% for main_domain, cert_params in acme['certificates'].items() %}
{% set cert=acme['basedir'] + '/' + main_domain + '/fullchain.cer' %}
run-acme.sh-dns01-{{ main_domain }}:
  file.directory:
    - name: {{ acme['basedir'] }}
    - makedirs: true
    - user: root
    - group: root
    - dir_mode: 700
    - file_mode: 600
    - recurse:
      - user
      - group
      - mode
  cmd.run:                                                                                                                                                              
    - name: >
        docker run --rm -v "{{ acme['basedir'] }}":/acme.sh
        {%- for env in cert_params.acmesh_dns01_env.keys() %} -e {{ env }} {% endfor %}
        {{ acmesh_image }}
        --issue -m {{ cert_params.email }}
        --server {{ cert_params.acmesh_server }}
        --dns {{ cert_params.acmesh_dns01_dns }}
        {%- for d in cert_params.dns01_domains %} -d '{{ d.domain }}'
        {%- if d.get('alias') %} --challenge-alias {{ d.alias }} {% endif %}
        {%- endfor %}
    - env: {{ cert_params.acmesh_dns01_env }}
{% endfor %}
```
{% endraw %}

All this state does is build the command line arguments as shown before, for every domain and alias defined in the pillar. The `acme` object comes from a [`map.jinja` containing default values overridabl, by pillar entries](https://blog.narf.ssji.net/2023/12/28/saltstack-maps-as-objects/ "SaltStack maps as objects").

## Renewing certificates

Once issued, the last task is to renew the certificates in a timely manner. I also use Salt for various downstream tasks (moving certificates to other locations, restarting services) when certificates are issued. For this reason, I preferred to keep the renewal under Salt’s control too, rather than, e.g., via a crontab leveraging `acme.sh`‘s auto-renewal.

This means the certificate-issuance state needs to be run whenever the current certificate, is about to expire (or missing). Conveniently, [there is a Salt module to do just that, `tls.valid_certificate`](https://docs.saltproject.io/en/latest/ref/states/all/salt.states.tls.html#salt.states.tls.valid_certificate). But how to trigger the certificat issuance process when the certificate is *not* valid?

[Requisites in Salt](https://docs.saltproject.io/en/latest/ref/states/requisites.html) states allow to control the execution of states. They can be used to conditionnally apply states, or reorder them as needed. While most requisites are use to trigger dependent states on success or on changes, one of them [does the same on failure: `onfail`](https://docs.saltproject.io/en/latest/ref/states/requisites.html#onfail).

This is handy with states that only check an invariant, but cannot fix it if it is incorrect, such as `file.exists`, or `tls.valid_certificat`e!The state with the `onfail` requisite should be the one in charge of restoring the desired state (e.g., creating a complex file base, or updating a certificate).

This was the last piece of my puzzle. The certificate-issuing state is now setup to run whenever there isn’t a valid certificate, or if it expires too soon in the future.

{% raw %}
```
run-acme.sh-dns01-{{ main_domain }}:
  cmd.run:
  ...
  - onfail:
      - tls: cert-valid-{{ main_domain }}

cert-valid-{{ main_domain }}:
  tls.valid_certificate:
    - name: {{ cert }}
    - days: 21
```
{% endraw %}

# Conclusion

With this setup, my configuration manager is in full control of the certificate issuance and renewal. Using Docker and not relying on native certificate upgrades is perhaps choosing a harder way to maintain the certificates. However, I think the initial added work in setting this up as described above pays out whenever I need to add or update certificate on any of the boxes managed with Salt, rather than having to do it in a more ad hoc fashion. It is also useful for hosts other than web servers.
