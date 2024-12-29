#!/usr/bin/env python

import html
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
# * [ ] Add newline after each paragraph
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
        patt = "<br></br>"
        src = element.children[0].content
        if patt in src:
            repl = src.replace(patt, "\n")  # this is what export-to-jekyll
            element.children[0].content = repl
            logger.info(
                "replaced newline markups in %(element)s)", {"element": element}
            )
        logger.warning("need to add {% raw %} around CodeFence if missing")
    elif isinstance(element, mistletoe.block_token.Paragraph):
        # add a newline after each paragraph
        element.children.append(mistletoe.span_token.RawText("\n"))
    else:
        logger.debug(element)
    if cc := element.children:
        for child in cc:
            reformat(child)
    return element


if __name__ == "__main__":
    # needs to be initialised before the first call to mistletoe.Document [0]
    # [0] https://github.com/miyuchina/mistletoe/issues/211
    renderer = MarkdownRenderer(max_line_length=80)

    f = sys.stdin
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
    (_, meta, md) = f.read().split("---\n")
    f.close()

    meta = html.unescape(meta)
    doc = reformat(mistletoe.Document(md))

    logger.debug(doc)

    md = renderer.render(doc)

    f = sys.stdout
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "w")
    f.write("---\n")
    f.write(meta)
    f.write("---\n")
    f.write(md)
    f.close()
