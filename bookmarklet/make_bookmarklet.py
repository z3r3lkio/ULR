#!/usr/bin/env python3
"""Build a javascript: URL from the readable ULR bookmarklet source."""
from pathlib import Path
from urllib.parse import quote
import re
src=Path(__file__).with_name("ulr.js").read_text(encoding="utf-8")
src=re.sub(r"/\*.*?\*/","",src,flags=re.S)
src=re.sub(r"\n\s*"," ",src)
print("javascript:"+quote(src,safe="()!~*'.,;:/?@&=+$#-_%"))
