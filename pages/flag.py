# -*- coding: utf-8 -*-
from ceefax.page import Page
from ceefax.helpers import file_handler


class FlagPage(Page):
    def __init__(self, page_num):
        super().__init__(page_num)
        self.title = "Norwegian Flag"
        self.index_num = page_num

    def generate_content(self):
        self.print_image(file_handler.load_file("norway"))


flag01 = FlagPage("182")
flag01.importance = 5
