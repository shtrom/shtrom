---
id: 956
title: 'Parsing A CRL With OpenSSL'
date: '2023-08-04T09:23:22+10:00'
author: 'Olivier Mehani'
excerpt: 'https://langui.sh/2010/01/10/parsing-a-crl-with-openssl/'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=956'
permalink: '/?p=956'
---

Just a shameless copy of [this post](https://langui.sh/2010/01/10/parsing-a-crl-with-openssl/) for my own records. Thanks Paul!

<div class="col-sm-9 col-sm-offset-3"><article><div class="col-sm-10"><div class="article_body"><div class="language-bash highlighter-rouge"><div class="highlight">```
<code>openssl crl <span class="nt">-inform</span> PEM <span class="nt">-text</span> <span class="nt">-noout</span> <span class="nt">-in</span> mycrl.crl</code>
```

</div></div></div></div></article></div>As to the `-inform`, `PEM` is for text data, or `DER` for binary data.