#!/usr/bin/env python3
from ceefax import config, Ceefax
import sys
import os
import config as _c

config.ceefax_path = os.path.dirname(os.path.realpath(__file__))
config.pages_dir = os.path.join(config.ceefax_path, "pages")
config.NAME = "HUSFAX"

for i, j in _c.__dict__.items():
    setattr(config, i, j)

c = Ceefax()
c.start_page_manager()
with open("PAGES.md", "w") as f:
    for n, page in c.page_manager.sorted_pages():
        f.write(f"{n} {page.title}\n")
