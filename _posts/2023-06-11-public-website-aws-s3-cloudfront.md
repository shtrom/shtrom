---
id: 853
title: 'Public website with S3 and CloudFront'
date: '2023-06-11T01:25:10+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=853'
permalink: /2023/06/11/public-website-aws-s3-cloudfront/
iawp_total_views:
    - '6'
image: /wp-content/uploads/sites/3/2023/04/Screenshot-from-2023-04-25-18-47-34.png
categories:
    - sysadmin
    - tip
tags:
    - AWS
    - CloudFormation
    - CloudFront
    - S3
---

As I [mentioned in a previous post](https://blog.narf.ssji.net/2023/04/24/render-apache-server-side-includes-docker/), I am migrating a number of static websites from Apache on bare metal to an object store and a CDN in the cloud. Namely, this is AWS S3 and CloudFront. To avoid too much manual grooming of pet yaks, I also went directly for Infrastructure-as-Code with CloudFormation, with the objective of creating a relatively simple reusable web+CDN template.

This is not a new topic, and a number of resources already exist around the web. I, for example, started with [this one, which does a fairly decent job](https://blog.canopas.com/deploy-a-website-with-aws-s3-cloudfront-using-cloudformation-c2199dc6c435). There are, however, a number of fine details which I have found were tricky to get right, could lead into incompatibilities, and for which accurate documentation was hard to find (even ChatGPT failed to provide a correct answer, though [this is not entirely surprising](https://blog.narf.ssji.net/2023/05/15/ai-chatbot-undeserved-authority/)).

<div class="wp-block-image is-style-default"><figure class="aligncenter size-full is-resized">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/04/chatgpt-s3-website-oac-oai.png "This is not true.")<figcaption class="wp-element-caption">ChatGPT confidently states things that aren’t true.</figcaption></figure></div>The goal of this post is to call those out, and provide the CloudFormation template mentioned above for those looking for a base. The template will:

1. create an S3 bucket for use as a website endpoint
2. create a CloudFront distribution using that bucket as an Origin
3. create a few DNS entries
4. create a TLS certificate for the service

tl;dr:

- The [S3 website endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html) behaves like a website, returning directory index documents, or HTML errors documents.
- The [bucket needs to be public for this to work](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html#WebsiteRestEndpointDiff), and it is [not possible to use either OAI nor OAC to limit access to the CloudFront distribution only](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html). The solution is to [control access based on the `Referer` header](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html#example-bucket-policies-HTTP-HTTPS)
- Generating TLS certificates with CertificateManager will fail with no clear explanation if the CAA policy for the domain forbids it.

<div class="wp-block-image is-style-default"><figure class="aligncenter size-full is-resized">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/04/Screenshot-from-2023-04-25-18-47-34.png)</figure></div>We first create an S3 bucket. Using the [S3 website endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html) (with `s3-website` in the domain name) allows to implicitly look for the `IndexDocument` on naked directory requests, and return the HTML `ErrorDocument` on error. Without this, the REST endpoint responds, which returns permission errors, and XML document, respectively. This however requires some of the bucket’s content to be publicly accessible.

```
Parameters:
  DomainName:
    Description: The base domain name to serve
    Type: String
    Default: example.net
  DefaultRootObject:
    Description: The name of the index object to return
    Type: String
    Default: index.html

Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref DomainName
      AccessControl: Private
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: false      # don't disallow public access policies
        IgnorePublicAcls: true
        RestrictPublicBuckets: false  # allow public access
      WebsiteConfiguration:
        IndexDocument: !Ref DefaultRootObject
        ErrorDocument: www/error.html
```

Time to set up the CDN. To use HTTP 2 and 3 on the CDN, we’ll need a TLS certificate. The first thing we need to do so is to create a DNS zone, in Route53 to validate the domain against.

```
Resources:
  ...
  DnsZone:
    Type: AWS::Route53::HostedZone
    Properties:
      Name: !Ref DomainName
      HostedZoneConfig:
        Comment: !Sub
          - "${DomainName} zone"
          - { DomainName: !Ref DomainName }
```

The certificate can now be requested, to be automatically validated via DNS. It is important, however, that the [CAA record](https://en.wikipedia.org/wiki/DNS_Certification_Authority_Authorization) for the zone allows CertificateManager to issue a certificate for the domain.

```
Resources:
  ...
  DnsRecordCAA:
    Type: AWS::Route53::RecordSet
    Properties:                                                                                                                                                         
      Name: !Ref DomainName
      TTL: 21600
      ResourceRecords:
        - !Sub
          - 0 iodef "mailto:admin@${DomainName}"
          - DomainName: !Ref DomainName
        - 0 issue "amazonaws.com"
      HostedZoneId: !GetAtt
        - DnsZone
        - Id
      Type: CAA
  TlsCertificate:
    Type: AWS::CertificateManager::Certificate
    DependsOn: DnsRecordCAA
    Properties:
      DomainName: !Sub
          - "*.${DomainName}"
          - { DomainName: !Ref DomainName }                                                                                                                             
      SubjectAlternativeNames:
        - !Ref DomainName
      ValidationMethod: DNS
```

We can now create the CloudFront CDN in front of the bucket. As this is a Website Endpoint, we need to use `CustomOriginConfig` (and use it to specify HTTP-only access to the bucket), rather than `S3Origin`, which would target the REST endpoint. Some gymnastic is needed to determine a functional URL for the S3 Website endpoint, due to [differences in endpoint domain name depending on the region](https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints).

```
Resources:
  ...
  CloudFront:     
    Type: AWS::CloudFront::Distribution
    Properties: 
      DistributionConfig:
        Aliases:  
          - !Ref DomainName
        Comment: "S3 CDN"
        DefaultCacheBehavior:
          CachePolicyId: b2884449-e4de-46a7-ac36-70bc7f1ddd6d  # CachingOptimizedForUncompressedObjects
          TargetOriginId: !Ref DomainName
        DefaultRootObject: !Ref DefaultRootObject
        Enabled: true
        HttpVersion: http2and3
        IPV6Enabled: true
        ViewerCertificate:
          AcmCertificateArn: !Ref TlsCertificate
          SslSupportMethod: sni-only
          MinimumProtocolVersion: TLSv1.2_2021
        Origins:
          # CloudFront is only in us-east-1, so that's where we are creating
          # the bucket. The website endpoint in VA use hyphens, e.g.,
          # example.net.s3-website-us-east-1.amazonaws.com.
          #
          # In the spirit of forward-compatibility, however, let's extract the
          # string from an authoritative source, thanks to [0]
          #
          # [0] https://schlarp.com/posts/cloudformation-string-replace/
          - DomainName: !Join
            - ''
            - !Split
              - "http://"
              - !GetAtt
                - Bucket
                - WebsiteURL
            Id: !Ref DomainName
            CustomOriginConfig:
              # Needed for S3 website endpoints, as they don't support TLS
              OriginProtocolPolicy: http-only
```

As we can’t [use OAC or OAI for access control to the bucket](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), we need another way to prevent unfettered public access to the bucket’s data (i.e., make sure that only the CloudFront distribution can directly access it). This can be done by [placing a secret string in the `Referer` header, and making the S3 bucket require it for access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html#example-bucket-policies-HTTP-HTTPS).

```
Resources:
  ...
  BucketPolicy:                                                                                                                                                         
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref Bucket
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Sid: AllowCloudFrontRefereReadOnly
            Action: 's3:GetObject'
            Effect: Allow
            Principal: '*'
            Resource: !Join
              - '/'
              - - !GetAtt
                  - Bucket
                  - Arn
                - '*'
            Condition:
              StringLike:
                  AWS:Referer: VerySecretString

  CloudFront:
    ...
    Origins:
      - DomainName: ...
        OriginCustomHeaders:
          - HeaderName: Referer
            HeaderValue: VerySecretString
```

We can now add DNS records pointing to the created CloudFront distribution.

```
Resources:
  ...
  DnsRecordRootA:
    Type: AWS::Route53::RecordSet
    Properties:
      Name: !Ref DomainName
      AliasTarget:
        DNSName: !GetAtt
          - CloudFront
          - DomainName
        HostedZoneId: Z2FDTNDATAQYW2  # CloudFront zone to point to
      HostedZoneId: !GetAtt
        - DnsZone
        - Id
      Type: A
  DnsRecordRootAAAA:
    Type: AWS::Route53::RecordSet
    Properties:
      Name: !Ref DomainName
      AliasTarget:
        DNSName: !GetAtt
          - CloudFront
          - DomainName
        HostedZoneId: Z2FDTNDATAQYW2  # CloudFront zone to point to
      HostedZoneId: !GetAtt
        - DnsZone
        - Id
      Type: AAAA
```

With all this in place, we can verify that the template is valid, with

```
aws cloudformation validate-template --template-body file://s3-cdn.yaml
```

and deploy it (in `us-east-1` , where CloudFront lives, otherwise we’d have to deploy multiple stacks)

```
aws --region us-east-1 cloudformation deploy --template-file s3-cdn.yaml --stack-name S3Cdn

```

This should be sufficient to

1. create a DNS entry that
2. points to the CloudFront distribution which,
3. on an TLS-encrypted HTTP 2 or 3 request,
4. forwards (using HTTP) it to the S3 bucket 
    - with a secret `Referer` header which
5. the S3 website endpoint will check before responding with the requested data.