from ceefax.page import Page
from scholarly import scholarly


class BarGraphPage(Page):
    def __init__(self, page_num):
        super().__init__(page_num)
        self.title = "Google Scholar Citations"
        self.tagline = "Data from Google Scholar"
        self.index_num = page_num
        self.data = [0, 0]

    def background(self):
        self.data = []

        if self.test:
            self.data = [25, 30]
            return

        # Matthew, Jorgen, Igor
        for id in ["wxM0Gh8AAAAJ", "hfeXoYMAAAAJ", "rSVxxwsAAAAJ"]:
            self.data.append(scholarly.search_author_id(id).get("citedby"))

    def generate_content(self):
        ymax = max(self.data)
        per_pixel = 1 + ymax // 44
        self.add_title("Citation Counts", font="size4")
        graph = []
        for i in range(44):
            line = ""
            for d, c in zip(self.data, ["r", "w", "b"]):
                if d > i * per_pixel:
                    line += c * 20
                else:
                    line += "-" * 20
                line += "-" * 5
            graph.append(line)
        self.print_image("\n".join(graph[::-1]), 4, 5)

        self.move_cursor(y=26, x=7)
        self.add_text("Matthew W Scroggs", fg="RED")
        self.move_cursor(y=26, x=32)
        self.add_text("J" + u"\u00F8" + "rgen S Dokken")
        self.move_cursor(y=26, x=58)
        self.add_text("Igor A Baratta", fg="BLUE")

        for x in [3, 76]:
            self.move_cursor(y=25, x=x)
            self.add_text("0")

        for d in self.data:
            for x in [3 - len(str(d)), 76]:
                self.move_cursor(y=25 - d // (per_pixel * 2), x=x)
                self.add_text(str(d))


b_page = BarGraphPage("450")
b_page.importance = 5
