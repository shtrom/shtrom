---
id: 1711
title: 'Fun with Python decorators'
date: '2024-11-14T13:10:49+11:00'
author: 'Olivier Mehani'
excerpt: "In Python, with Click, we wanted to transform any Exception to a `click.ClickException`, and\ncatch one particular exception, to retry the function that raised it with a different parameter value as a fallback. We got the first behaviour quickly into a decorator. We then realised that the second could also be done nicely with a decorator, too."
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1711'
permalink: '/?p=1711'
---

We’ve been having some fun with [Click](https://click.palletsprojects.com) and [Python decorators](https://realpython.com/primer-on-python-decorators/) at work.

We had a situation where we wanted to

1. transform any `Exception` to a `click.ClickException`, so they would be rendered nicely, and
2. catch one particular exception, and retry the function that raised it with a different parameter value as a fallback.

We got the first behaviour quickly into a decorator. We then realised that the second could also be done nicely with a decorator, too.

# The fun begins

Here’s a picky test function, decorated as a Click command with one argument, `value`.

```
@click.command
@click.argument('value', type=int)
def hello(value):
    if value == 1:
        raise ValueError("I don't like one")
    if value < 0:
        raise IndexError("Don't know negatives")
    click.secho(f"hello, I like {value}!")
```

# Error handling

First, we want a decorator that `try`es the function, and raises a `click.ClickException` for any other exception. This is nice, as Click formats those exceptions properly as an error message to the user, without an ugly stack trace. Using a decorator nonetheless allows to not use `click` deep into the code, and limit it to the entry points, all the while capturing everything that bubbles up.

A decorator takes a function as a parameter, and returns an enhanced (decorated) function. Our decorated function here just needs to be called in a `try ... except` block.

```
def error_handler(fun):

  def wrapped(*args, **kwargs):
    try:
      return fun(*args, **kwargs)
    except Exception as e:
      raise click.ClickException(f"{e.__class__}: {e}") from e

  # retain the name of the function so click can use it as the command name
  wrapped.__name__ = fun.__name__
  return wrapped
```

## Naming shenanigans

Click decorators automatically guess the name to use as a command based on the name of the decorated function. Unfortunately, with other generic decorators down the stack, Click renamed the `hello` command to… `wrapped`, as this was the name of the function returned by the `error_handler`.

To work around this, I had a quick introspective look and noticed that every function object has a `__name__` attribute, so I just copied its value to the `__name__` of the wrapped function,

```
wrapped.__name__ = fun.__name__
```

and hoped for the best. It did work well.

Shortly after this, while reading the code of some other decorators, I found that the [`functools.wraps` decorator](https://docs.python.org/3/library/functools.html#functools.wraps) does exactly that, too.

# Retries

Our second decorator is a bit more complex. It needs to know which `Exception` we want to retry on, and what value to retry with.

We’re entering decorator-ception here. A [decorator with parameters needs to return a decorator function without parameters](https://realpython.com/primer-on-python-decorators/#decorators-with-arguments) (a closure over the parameters), which then will be applied to our function. The logic itself is simple: `try ... catch`, using the passed `exception`, and retrying with the passed `value`.

```
def retry_on_exception(exception, value):

    def inner_decorator(fun, *args, **kwargs):

        def wrapped(*args, **kwargs):
            try:
                click.secho(f"Trying with {args} {kwargs} ...")
                return fun(*args, **kwargs)
            except exception as e:
                kwargs['value'] = value
                click.secho(f"Retrying with {args} {kwargs} after {e.__class__}...")
                return fun(*args, **kwargs)

        # retain the name of the function so click can use it as the command name
        wrapped.__name__ = fun.__name__
        return wrapped

    return inner_decorator
```

# Putting it all together

All that is left is to decorate our function.

```
@main.command()
@click.argument('value', type=int)
@error_handler
@retry_on_exception(ValueError, 2)
def hello(value):
  ...
```

And bingalingo!

<figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2022/11/Screen-Shot-2022-11-22-at-12.21.19-1024x191.png)</figure>## Full code

```
#!/usr/bin/env python3

import click

def error_handler(fun, *args, **kwargs):
    def wrapped(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            raise click.ClickException(f"{e.__class__}: {e}") from e
    # retain the name of the function so click can use it as the command name
    wrapped.__name__ = fun.__name__
    return wrapped

def retry_on_exception(exception, value):
    def inner_decorator(fun, *args, **kwargs):
        def wrapped(*args, **kwargs):
            try:
                click.secho(f"Trying with {args} {kwargs} ...")
                return fun(*args, **kwargs)
            except exception as e:
                kwargs['value'] = value
                click.secho(f"Retrying with {args} {kwargs} ...")
                return fun(*args, **kwargs)
        # retain the name of the function so click can use it as the command name
        wrapped.__name__ = fun.__name__
        return wrapped
    return inner_decorator

@click.group
def main():
    pass

@main.command()
@click.argument('value', type=int)
@retry_on_exception(ValueError, 2)
@error_handler
def hello(value):
    if value == 1:
        raise ValueError("I don't like one")
    if value < 0:
        raise IndexError("Don't know negatives")
    click.secho(f"hello, I like {value}!")

if __name__ == '__main__':
    main()
```

# Conclusion

Decorators are really `fun` (gettit? gettit?). They also allow to DRY code, and add bits of runtime logic separately from the business logic of the function getting written.

That said, a couple of things could have been done for a more generic retry logic. First, Click only passes arguments via `kwargs`. In our example above, we forcibly overwrote `kwargs["value"]`, but we might as well have just done a `kwargs.update(value)`, passing a full `Dict` (or `kwargs`) of arguments to use as replacements to the original.

Another thing would be to support retrying on more than one exception. Fortunately, Python’s `except` statement can accept a sequence of multiple exceptions, so I suspect (but haven’t tried) that it’s only a matter of passing a tuple of all the exceptions to retry.