#!/usr/bin/env python3

"""
This is a script that replaces image links in an SVG documents
with embedded images.

This is to work around the strict content security policy at
https://raw.githubusercontent.com/ .
"""

import base64
import copy
import pathlib
import sys
import xml.etree.ElementTree

_SVG_NS = "http://www.w3.org/2000/svg"
_XLINK_NS = "http://www.w3.org/1999/xlink"

_HREF_ATTR = f"{{{_XLINK_NS}}}href"
_IMAGE_TAG = f"{{{_SVG_NS}}}image"

_SUFFIX2TYPE = {
    "jpeg": "jpg",
    "svg": "svg+xml",
}


def register_namespaces(file_name: pathlib.Path):
    for _, (name, ns) in xml.etree.ElementTree.iterparse(
        input_file_name,
        events=["start-ns"],
    ):
        xml.etree.ElementTree.register_namespace(name, ns)


def embed_images(root: xml.etree.ElementTree, directory: pathlib.Path):
    for image in root.findall(f".//{_IMAGE_TAG}"):
        image_file_name = directory / image.get(_HREF_ATTR)
        encoded = base64.b64encode(image_file_name.read_bytes()).decode()
        suffix = image_file_name.suffix[1:]
        fmt = _SUFFIX2TYPE.get(suffix, suffix)
        data_url = f"data:image/{fmt};base64,{encoded}"
        image.attrib[_HREF_ATTR] = data_url


def main(input_file_name: pathlib.Path):
    register_namespaces(input_file_name)
    tree = xml.etree.ElementTree.parse(input_file_name)
    embed_images(tree, input_file_name.parent)
    tree.write(sys.stdout.buffer, encoding="utf-8")


if __name__ == "__main__":
    (input_file_name,) = sys.argv[1:]
    main(pathlib.Path(input_file_name))
