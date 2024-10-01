---
id: 924
title: 'Python CLI backward compatibility decorator'
date: '2024-06-30T23:44:04+10:00'
author: 'Olivier Mehani'
excerpt: 'Click sometimes introduces too much coupling between the CLI and the underlying Python functions. It is possible to break this coupling using dedicated decorators, so we can refactor the Python code as needed withouth breaking the existing CLI usage.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=924'
permalink: /2024/06/30/python-cli-backward-compatibility-decorator/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '5'
image: /wp-content/uploads/sites/3/2024/06/image.png
categories:
    - code
    - tip
tags:
    - Click
    - decorator
    - Python
---

[Click is a Python module to make a native function into a command line tool](https://click.palletsprojects.com/). It is very useful to quickly expose functionality from a set of Python functions to a wider context such as shell users or automation scripts.

However, this also creates coupling between the prototype of the Python function, and the interface exposed to the CLI. This means that both now need to be changed together, or never changed ever again. If automation depends on the command, it is likely that the latter choice will be made.

There is a better way. We can interleave logic to adjust the parameters passed to the function without changing those that the command accepts. Click makes extensive use of Python decorators and, [as we did in the past, we can leverage decorators](https://blog.narf.ssji.net/2022/11/22/fun-with-python-decorators/ "Fun with Python decorators") for this, too.

tl;dr:

- Taking the example of extending one `--option` to a list of `argument`s,
- we can write a `map_option_to_argument(option: str, argument: str)` decorator, which
- reads the `kwargs` passed to the decorated function,
- removes the `option`(s), and
- inserts the value(s) into the `argument`.
- The refactored Python function doesn’t need to know anything about the `option` anymore.

```
@click.command
@click.option("--option", required=False)       # will be remapped
@click.argument("arguments", nargs=-1)
@map_option_to_argument('option', 'arguments')  # remap and remove option
def cli(arguments=[]):                          # knows nothing about option
    print(f"{arguments=}")
```

One key distinction in parameters is in *options* vs. *arguments.*[ Options (`click.option`) are introduced on the command line with a flag (e.g., `--opt` or `-o`) and can be passed in any order](https://click.palletsprojects.com/en/8.1.x/options/), while [arguments (`click.arguments`) are not, and their order matters](https://click.palletsprojects.com/en/8.1.x/arguments/) if there are arguments of different types. Here is a simple example:

```
import click

@click.command
@click.option("--option", type=int, required=False, multiple=False)
@click.argument("arguments", type=int, nargs=-1)
@map_option_to_argument("option", "arguments")
def cli(option = None, arguments = ()):
    print(f"{option=}")
    print(f"{arguments=}")

if __name__ == "__main__":
    cli()
```

```
$ command --option 1 2 3
options=(1, )
arguments=(2, 3)
```

Sometimes, when evolving the behaviour of a CLI tool, it may become necessary to expand from accepting a single option value, to more than one. Click supports this natively, with “[multiple options](https://click.palletsprojects.com/en/8.1.x/options/#multiple-options)”, which allows to repeat the option flag as many times as values are needed. This can be done simply by changing the `multiple` parameter to `True` in the `@click.option` in the code above. I however find it quickly makes command lines unwieldy, and too verbose.

```
$ command --option 1 --option 2 --option 3 --option 4 5 6
options=(1, 2, 3, 4)
arguments=(5, 6)
```

My preferred solution is to use arguments instead, which can be unlimited with `nargs=-1`. But we need to maintain backward compatibility in the CLI, so the `--option` style is not disabled when introducing the `arguments` style.

We can write a decorator that plucks the old option value(s) from the `kwargs`, and inserts them into the parameter instead. When applied at the end of the decorator list for the function, this allows us to completely deprecate and move on from the old single argument in the Python function, while retaining a backward-compatible behaviour in the CLI.

```
from functools import wraps  # needed to retain the name of the wrapped function as the command name

def map_option_to_argument(option: str, argument: str):
    """
    Decorator to remap a single-value option to a tuple of narg=-1 arguments.
    Useful for backward compatibility, when extending the option to accept a
    variable number of values (i.e., arguments).

        @click.command
        @click.option("--option", required=False)
        @click.argument("arguments", nargs=-1)
        @map_option_to_argument('option', 'arguments')
        def cli(arguments=[]):
            ...

    """
    def decorator(function):

        @wraps(function)
        def wrapped(*args, **kwargs):
            if optval := kwargs.get(option):
                if not isinstance(optval, tuple):
                    optval=(optval,)             
                                                                                                                   
                argval = kwargs.get(argument, [])
                argval = optval + argval
                kwargs[argument] = argval

            del kwargs[option]

            function(*args, **kwargs)

        return wrapped
    return decorator
```

The decorator accepts the names of the `option` to be remapped, and the `argument` to remap it to (line 2). It extracts the value(s) of the option from the `kwargs`, and wraps it in a tuple if it’s a non-multiple value (ll. 22-23). After having inserted the options tuple into the argument list, it then completely removes the `option` parameter (l. 29), so the decorated function doesn’t receive it in its own `kwargs`.

<div class="wp-block-image"><figure class="aligncenter size-full">![Screenshot of a terminal running a Python script. ./cmd.py --option 1 --option 2 3 option=None arguments=(1, 2, 3)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/06/image.png)</figure></div>We can now refactor our function to a more sensible prototype as needed, and even expose an extended CLI, while avoiding broken scripts or confused users.

A similar approach can be taken to break other aspects of the coupling that Click introduces. This is a nice way to continue leveraging the power of Click without preventing refactors of the underlying Python code in the name of CLI backward compatibility.