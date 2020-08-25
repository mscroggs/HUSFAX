import pytest

from ceefax.page import PageManager
from ceefax.cupt import DummyScreen
from ceefax import config

import config as _c
for i, j in _c.__dict__.items():
    setattr(config, i, j)


def test_all_pages():
    c = Ceefax()
    c.start_page_manager()
    pages = ""
    for n, page in c.page_manager.sorted_pages():
        pages += f"{n} {page.title}\n"

    with open("../PAGES.md", "w") as f:
        assert f.read() == pages
