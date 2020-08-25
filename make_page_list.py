#!/usr/bin/env python3
from ceefax import config
from ceefax.page import PageManager
from ceefax.cupt import DummyScreen
import os
import config as _c

config.ceefax_path = os.path.dirname(os.path.realpath(__file__))
config.pages_dir = os.path.join(config.ceefax_path, "pages")
config.NAME = "HUSFAX"

for i, j in _c.__dict__.items():
    setattr(config, i, j)

page_manager = PageManager(DummyScreen())
with open("PAGES.md", "w") as f:
    for n, page in page_manager.sorted_pages():
        f.write(f"{n} {page.title}\n")
