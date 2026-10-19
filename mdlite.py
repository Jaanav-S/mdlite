"""A small Markdown to HTML converter."""

import html
import re
import sys

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
UL_ITEM = re.compile(r"^\s*[-*+]\s+(.*)$")
OL_ITEM = re.compile(r"^\s*\d+[.)]\s+(.*)$")
FENCE = re.compile(r"^```\s*([\w+-]*)\s*$")
HR = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
