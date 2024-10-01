---
id: 1588
title: 'Python object as kwargs'
date: '2024-05-22T11:43:35+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1588'
permalink: '/?p=1588'
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

```
>>> b=bob(1,2)
>>> fun(**b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __main__.fun() argument after ** must be a mapping, not bob</module></stdin>
```

  
My class is not good enough a mapping.

Doing some duck-typing based on <https://docs.python.org/3/library/collections.abc.html#module-collections.abc> , I need to implement `__getitem__`, `__iter__` and `__len__`.

```
from collections.abc import Mapping
class bob2(Mapping):
  def __init__ (self, a, b):
    self.a = a
    self.b = b
bob2.__getitem__ = lambda self, k: getattr(self, k)
bob2.__len__ = lambda self: 2
def iter(self):
  yield 'a'
  yield 'b'
bob2.__iter__=iter
bob2.__abstractmethods__ = frozenset({})  # we implemented all the abstract methods
```

And boom.

```
>>> fun(**b2)
a 1
b 2
```