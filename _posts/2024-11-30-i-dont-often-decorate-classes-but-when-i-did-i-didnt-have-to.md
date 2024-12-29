---
id: 1712
title: 'I don&#8217;t often decorate classes, but when I did, I didn&#8217;t have to'
date: '2024-11-30T23:58:06+11:00'
author: 'Olivier Mehani'
excerpt: "I have a few different classes implementing a specific behaviour, and want to find a specific one. What do I do?\n\nClasses can be decorated in the same way as functions, and a decorated can be written to add each class to a list, for later searching. \n\nHowever, for this stated purpose, it's not necessary, as class inheritance is better suited, and parent classes have a __subclasses__ method returning a similar list."
layout: post
guid: 'https://blog.narf.ssji.net/?p=1712'
permalink: /2024/11/30/i-dont-often-decorate-classes-but-when-i-did-i-didnt-have-to/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '1'
categories:
    - code
tags:
    - decorator
    - Python
---

I have played with [Python](https://blog.narf.ssji.net/2022/11/22/fun-with-python-decorators/ "Fun with Python decorators") [decorators](https://blog.narf.ssji.net/2024/06/30/python-cli-backward-compatibility-decorator/ "Python CLI backward compatibility decorator") before. They are useful to extend the behaviour of a function by composition, without having to change the function itself. But functions aren’t the only object that can be decorated: classes can, too.

I started investigating this when I had a number of different classes implementing a specific behaviour, and wanted to be able to find a specific one. A simple decorator can be written which will add each decorated class into a list. Finding the desired class is then a simple `for` loop away.

tl;dr:

- Classes can be decorated in the same way as functions: the decorator takes the class as an argument, does something to or with it, and returns a class.
- For the stated purpose, it’s not necessary, as class inheritance is better suited, and parent classes natively have a `__subclasses__` method returning a list of their descendents.

For a more concrete example, let’s say we want to have a system that support multiple markup languages (e.g, HTML and Markdown). We want independent classes to support each of the languages, and the ability to find the right class for a given language.

# A handful of markups

Here’s our simple classes.

```
class HtmlSupport:
    @classmethod
    def support(cls, lang):
        return lang == "html"


class MarkdownSupport:
    @classmethod
    def support(cls, lang):
        return lang == "markdown"
```

Thanks to the `support` method, each class can be interrogated about their support for the given `lang`.

```
>>> MarkdownSupport.support('markdown')
True
>>> MarkdownSupport.support('html')
False
```

But how to find the right support class out of all the existing implementations? We don’t even know what all the implementations are! Now… If we had a list, it would be neater

```
implementations = [
  HtmlSupport,
  MarkdownSupport,
]


def find_class(lang):
    for imp in implementations:
        if imp.support(lang):
            return imp    
```

This is a good start.

```
>>> find_class('html')
<class 'decorate.HtmlSupport'>
>>> find_class('json')
>>>
```

# A few markups more

One issue with this approach is that it needs the `implementations` list to be explicitely maintained: every new implementation needs to be added to that list, wherever it might be (other source file, other module, …). This is not very nice. Instead, we could offer a function to add new implementations to the list dynamically.

```
implementations = []

def add_to_implementation(klass):                                                                                                                                            
    implementations.append(klass)                                                                                                                                     
                                                                                                                                                                                                                                                                                                                     
    return klass 
```

We can then use this function when we declare new classes.

```
class RestructuredTextSupport:
    @classmethod
    def support(cls, lang):
        return lang == "restructuredtext"

add_to_implementation(RestructuredTextSupport)
```

And each class added in this way will be present in the `implementations` list.

```
>>> implementations
[<class '__main__.RestructuredTextSupport'>]
```

# Decorators (at last)!

But hold on. We are calling a method within a file which declare a class? Mixing declaration and instructions is not very nice. Could we do better? This is where decorators come into play. Like [M. Jourdain](https://en.wikipedia.org/wiki/Le_Bourgeois_gentilhomme), it turns out we already had one, but we didn’t know about it.

```
@add_to_implementation
class DokuWikiSupport:
    @classmethod
    def support(cls, lang):
        return lang == "dokuwiki"
```

We called it more declaratively, but the outcome is the same.

```
>>> implementations
[<class '__main__.RestructuredTextSupport'>, <class '__main__.DokuWikiSupport'>]
```

One important point of note is that our `add_to_implementations` function returns a class. If it didn’t, the class would still be added correctly to our list of implementations, but it would not be available in local namespace.

```
>>> def half_decorate(cls):
...   implementations.append(cls)
... 
>>> @half_decorate
... class Bob:
...   pass
... 
>>> implementations
[<class '__main__.RestructuredTextSupport'>, <class '__main__.DokuWikiSupport'>, <class '__main__.Bob'>]
>>> Bob()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'NoneType' object is not callable
```

In any case, we are now able to declare all our implementations via our decorator. I renamed it to simply `implementation` for legibility. I’ve also expanded the decorator a bit so it would actually modify the returned class, by adding a `decorated` method, as a way to demonstrate that the main purpose of decorating still works.

```
# decorate.py

implementations = []

def implementation(klass):
    implementations.append(klass)

    def decorated():
       return True

    klass.decorated = decorated
    return klass


@implementation
class DokuWikiSupport:
    @classmethod
    def support(cls, lang):
        return lang == "dokuwiki"


@implementation
class HtmlSupport:
   @classmethod
   def support(cls, lang):
     return lang == "html"


@implementation
class MarkdownSupport:
    @classmethod
    def support(cls, lang):
       return lang == "markdown"


class RestructuredTextSupport:
    @classmethod
    def support(cls, lang):
        return lang == "restructuredtext"


def find_class(lang):
    for imp in implementations:
          if imp.support(lang):
              return imp      
```

And we can finally find our the right class for the right purpose.

```
>>> <class 'decorate.DokuWikiSupport'>
>>> find_class('html')
<class 'decorate.HtmlSupport'>
>>> find_class('txt')
>>> >>> find_class('markdown').decorated()
True
```

# With better design, none of this is necessary

So, at this point I was pretty happy with myself, and I had solved my problem. But something was bothering me. All those classes implement the same method, so this is screaming for some object orientation, with a nice abstract class.

```
# subclasses.py

from abc import abstractmethod

class AbstractSupport():
  @classmethod
  @abstractmethod
  def support(cls, lang):
      """Return True if this class supports lang"""

class HtmlSupport(AbstractSupport):
  # same body as before

class MarkdownSupport(AbstractSupport):
  # same body as before

class RestructuredTextSupport(AbstractSupport):
  # same body as before

class DokuWikiTextSupport(AbstractSupport):
  # same body as before
```

This is nicer design, but this doesn’t help us find the right implementation just yet. We still need a list to search through. Fortunately, as part of the class hierarchy, Python maintains a list of all the subclasses of each class. It is available from the `__subclasses__` method.

```
>>> AbstractSupport.__subclasses__()
[<class 'subclasses.HtmlSupport'>, <class 'subclasses.MarkdownSupport'>, <class 'subclasses.RestructuredTextSupport'>, <class 'subclasses.DokuWikiSupport'>]
```

So we can do the same dance as before, without having to do anything to maintain the list!

```
def find_class(lang): 
    for imp in AbstractSupport.__subclasses__():
        if imp.support(lang):
            return imp 
```

And it all works as needed.

```
>>> find_class("markdown")
<class 'subclasses.MarkdownSupport'>
>>> find_class("html")
<class 'subclasses.HtmlSupport'>
>>> find_class("json")
>>> 
```

We have lost the silly addition of the `decorated` method along the way, but it was never a requirement in the first place.

So, here we are. Perhaps I now reach too readily for decorators when simpler and more straightforward solutions exist. They are still useful tools, including on classes, but when dealing with classes, it is probably best to start with what the normal class system offers before trying to reimplement the wheel (albeit a decorated wheel).