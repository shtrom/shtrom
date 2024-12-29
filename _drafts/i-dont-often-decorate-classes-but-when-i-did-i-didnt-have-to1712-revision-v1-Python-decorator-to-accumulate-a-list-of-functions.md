---
id: 1715
title: 'Python decorator to accumulate a list of functions'
date: '2024-11-21T12:55:30+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1715'
permalink: '/?p=1715'
---

“`  
a = \[\]  
  
def add\_element(fn):  
a.append(fn)  
return fn  
  
@add\_element  
def fn1():  
print(“fn1”)  
  
@add\_element  
def fn2():  
print(“fn2”)  
  
print(a)  
“`  
  
$ python ./test.py 0s 126 ↵ \[lando\] ✹ ✭ bug1895523/git-landing-worker-vcs-agility   
\[&lt;function fn1 at 0x7f8bfb21cc20&gt;, &lt;function fn2 at 0x7f8bfb21d760&gt;\]

> > > class A:  
> > > … pass  
> > > …  
> > > class B(A):  
> > > … pass  
> > > …  
> > > dir(A)  
> > > \[‘**class**‘, ‘**delattr**‘, ‘**dict**‘, ‘**dir**‘, ‘**doc**‘, ‘**eq**‘, ‘**format**‘, ‘**ge**‘, ‘**getattribute**‘, ‘**getstate**‘, ‘**gt**‘, ‘**hash**‘, ‘**init**‘, ‘**init\_subclass**‘, ‘**le**‘, ‘**lt**‘, ‘**module**‘, ‘**ne**‘, ‘**new**  
> > > ‘, ‘**reduce**‘, ‘**reduce\_ex**‘, ‘**repr**‘, ‘**setattr**‘, ‘**sizeof**‘, ‘**str**‘, ‘**subclasshook**‘, ‘**weakref**‘\]  
> > > A.**subclass A.\_\_subclasscheck**( A.**subclasses**() A.**subclasshook**(  
> > > A.**subclasses**()  
> > > \[\]  
> > > A.**subclasshook**(  
> > > …  
> > > KeyboardInterrupt  
> > > A.**subclasshook**()  
> > > NotImplemented  
> > > for e in A.**subclasses**():  
> > > … print(e)  
> > > …