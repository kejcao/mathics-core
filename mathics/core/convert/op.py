"""
Conversions from the ASCII representation of Mathics operators to their Unicode equivalent
"""

import os.path as osp
import pkg_resources

from functools import lru_cache

try:
    import ujson
except ImportError:
    import json as ujson

ROOT_DIR = pkg_resources.resource_filename("mathics", "")

# Load the conversion tables from disk
characters_path = osp.join(ROOT_DIR, "data", "op-tables.json")
assert osp.exists(characters_path), "ASCII operator to Unicode tables are missing"
with open(characters_path, "r") as f:
    op_data = ujson.load(f)


@lru_cache(maxsize=1024)
def ascii_op_to_unicode(ascii_op: str, encoding: str) -> str:
    """
    Convert an ASCII representation of a Mathics operator into its
    Unicode equivalent based on encoding (in Mathics, $CharacterEncoding).
    If we can't come up with a unicode equivalent, just return "ascii_op".
    """
    if encoding in ("UTF-8", "utf-8", "Unicode"):
        return op_data["ascii-operator-to-unicode"].get(ascii_op, ascii_op)
    if encoding in ("WMA",):
        return op_data["ascii-operator-to-wl-unicode"].get(ascii_op, ascii_op)
    return ascii_op
