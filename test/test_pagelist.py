import os

from ceefax.page import PageManager
from ceefax.cupt import DummyScreen
from ceefax import config

import config as _c
for i, j in _c.__dict__.items():
    setattr(config, i, j)


def test_pagelist():
    page_manager = PageManager(DummyScreen())
    pages = ""
    pages += "| No. | Page title |\n"
    pages += "| --- | ---------- |\n"
    for n, page in page_manager.sorted_pages():
        pages += f"| {n} | {page.title} |\n"

    with open(os.path.join(_c.ceefax_path, "PAGES.md")) as f:
        assert f.read() == pages
