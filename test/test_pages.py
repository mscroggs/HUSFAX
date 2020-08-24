import pytest

from ceefax.page import PageManager
from ceefax.cupt import DummyScreen
from ceefax import config

import config as _c
for i, j in _c.__dict__.items():
    setattr(config, i, j)

page_manager = PageManager(DummyScreen())


@pytest.mark.parametrize("pnum", page_manager.pages.keys())
def test_all_pages(pnum):
    page = page_manager.pages[pnum]

    if page.background is not None:
        page.background()
    page.reload()
    page.generate_content()
