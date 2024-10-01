---
id: 567
title: 'Resolve escapes in Python strings'
date: '2022-10-28T13:21:33+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=567'
permalink: /2022/10/28/resolve-escapes-in-python-strings/
iawp_total_views:
    - '6'
categories:
    - code
    - tip
tags:
    - Python
---

If you have a Python string that contains the representation of escaped characters (say, a backslash `\`, an `x`, and two hexadecimal digits), and you want to decode those escapes back to the actual character they represent, [you can use `codecs.escape_decode`](https://stackoverflow.com/questions/63218987/convert-x-escaped-string-into-readable-string-in-python/63219333#63219333).

Python3 has an abstract concept of a string (`str`), which is not actually a series of bytes. It is nice because it allows you to decorrelate the string processing from the final representation. Generally, you (or your tools) would end up representing the string as a series of bytes with `s.encode(encoding)`, and you’ll get different results based on the chosen encoding.

```
>>> a='é'
>>> len(a)
1
>>> a.encode('latin-1')
b'\xe9'
>>> a.encode('utf-8')
b'\xc3\xa9'
```

One problem that I have been battling with is what if your string contains escapes that you would like to honour? Let’s say I have the previous two UTF-8 bytes encoding `é`. I can can convert it back to a Python string with `b.decode(encoding)`.

```
>>> b=b'\xc3\xa9'  # note: `b` before the quote to declare a series of bytes
>>> len(b)
2
>>> b.decode('utf-8')
'é'
```

Now, what if I happen to have a Python string (not a series of bytes), that contains those escapes? I can’t decode it, because it’s already a string.

```
>>> ub=r'\xc3\xa9'  # note: `r`before the quote to preserve the escapes (raw)
>>> len(ub)
8
>>> ub.decode('utf-8')
Traceback (most recent call last):
  File "", line 1, in 
AttributeError: 'str' object has no attribute 'decode'
```

But encoding the string separately encodes each character to bytes. There is a `unicode_escapes encoding` function, but it seems to do the exact opposite of what I want.

```
>>> ub.encode('utf-8')
b'\\xc3\\xa9'
>>> ub.encode('unicode_escape')
b'\\\\xc3\\\\xa9'
```

The goal is to convert our Python string containing escapes-looking multi-byte sequences, and resolve those to the actual byte value (or string representation, as we know how to encode/decode from one to another). I finally found the [`codecs` module](https://docs.python.org/3/library/codecs.html) with its (undocumented) `escape_decode` function (it returns a tuple of the byte string and the length of input consumed).

```
>>> bb=codecs.escape_decode(ub)[0]
>>> len(bb)
2
>>> uu=bb.decode('utf-8')
>>> len(uu)
1
>>> uu
'é'
```

Success!