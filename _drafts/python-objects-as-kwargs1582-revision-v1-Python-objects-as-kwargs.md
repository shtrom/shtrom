---
id: 1602
title: 'Python objects as kwargs'
date: '2024-05-22T20:13:38+10:00'
author: 'Olivier Mehani'
excerpt: 'I have a Python class which I want to use as kwargs in a function. It doesn''t work by default: `argument after ** must be a mapping`. The fix is to inherit from `collections.abc.Mapping`, and implement the missing abstract classes.'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1602'
permalink: '/?p=1602'
---

So, I have a class which, for some reason (some call it Pythonicity, other call it laziness), I want to use as `kwargs` in a function.

```
class bob:
  def __init__ (self, a, b):
    self.a = a
    self.b = b


def fun(a, b):
  print('a', a)
  print('b', b)
```

but

<div class="wp-block-image"><figure class="aligncenter size-full">![Screenshot from a Python REPL. >>> b=bob(1,2) >>> fun(**b) Traceback (most recent call last): File "", line 1, in TypeError: __main__.fun() argument after ** must be a mapping, not bob](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/Screenshot-2024-05-22-at-12.28.02.png)</figure></div>My class is not good enough a mapping.

tl;dr: Duck typing to the rescue!

- Inherit from [collections.abc.Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "collections.abc.Mapping"), and
- implement `__getitem__`, `__iter__` and `__len__`.

```
from collections.abc import Mapping


class bob2(Mapping):
  def __init__ (self, a, b):
    self.a = a
    self.b = b

  def __getitem__(self, k):
    return getattr(self, k)

  def __len__(self):
    return 2

  def __iter__(self):
    yield 'a'
    yield 'b'
```

And boom.

```
>>> b2 = bob2(1, 2)
>>> fun(**b2)
a 1
b 2
```

This is very written-for-purpose code. A real implementation would probably need a list of fields as a class variable, that can then be measured, looped, and iterated over.

# Addendum

[Cameron Simpson](https://aus.social/@cs "Cameron Simpson") pointed out, in the comments, that every object in Python has a `__dict__` attribute which would have worked out of the box for my purpose.

```
>>> b=bob(3,4)
>>> b.__dict__
{'a': 3, 'b': 4}
```