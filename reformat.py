#!/usr/bin/env python

import logging
from pathlib import Path
import sys

import mistletoe
from mistletoe.markdown_renderer import MarkdownRenderer
import urllib.request

OLD_PREFIX = "https://blog.narf.ssji.net/"
NEW_PREFIX = "/"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO
#
# * [ ] FencedCode
#   * [ ] replace BR
#   * [ ] wrap in raw/endraw
# * [x] Image
#   * [x] download asset to wp-content
#   * [x] rewrite


def reformat(element):
    if isinstance(element, mistletoe.span_token.Link):
        if element.target.startswith(OLD_PREFIX):
            element.target = NEW_PREFIX + element.target.removeprefix(OLD_PREFIX)
            logger.info("rewrote link to %(target)s", {"target": element.target})
    elif isinstance(element, mistletoe.span_token.Image):
        if element.src.startswith(OLD_PREFIX):
            path = Path(element.src.removeprefix(OLD_PREFIX))
            path.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(element.src, path)
            logger.info("downloaded image: %(path)s", {"path": path})
            element.src = NEW_PREFIX + str(path)
    elif isinstance(element, mistletoe.block_token.CodeFence):
        logger.warning("need to add {% raw %} around CodeFence if missing")
    else:
        logger.debug(type(element))
    if cc := element.children:
        for child in cc:
            reformat(child)
    return element


if __name__ == "__main__":
    f = sys.stdin
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")

    doc = reformat(mistletoe.Document(f.read()))
    f.close()

    f = sys.stdout
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "w")

    renderer = MarkdownRenderer()
    md = renderer.render(doc)
    f.write(md)
    f.close()
