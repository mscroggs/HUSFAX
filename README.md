# HUSFAX
This repository contains pages for the [CEEFAX](https://github.com/mscroggs/CEEFAX) screen in my house.

Before running HUSFAX, install the dependencies with:

```shell
pip install -r requirements.txt
```

And install [CEEFAX](https://github.com/mscroggs/CEEFAX):
```shell
pip3 install git+https://github.com/mscroggs/CEEFAX.git --upgrade
```

HUSFAX is launched in a linux or mac terminal with:

```shell
./run.py
```

or

```shell
python3 run.py
```

## Contributing to HUSFAX
### Adding a Page
The pages are stored in the `pages/` folder. A page file should have the following structure:

```python
from page import Page

class NameOfNewPage(Page):
    def __init__(self, args):
        super(NameOfNewPage, self).__init__(PAGENUMBER)
        pass

    def background(self);
        pass

    def generate_content(self);
        pass

page = NameOfNewPage(args)
```

The function `__init__` will the run when the page if first built. `background` will be run in the background every so often,
and should be used for code that takes a while to run. `generate_content` is run every time the page is loaded.

For a list of current pages, see `PAGES.md`.
