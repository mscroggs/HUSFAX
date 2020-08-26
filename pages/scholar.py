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
        # Matthew, Jorgen
        for id in ["wxM0Gh8AAAAJ", "hfeXoYMAAAAJ"]:
            author = scholarly.search_author_id(id).fill()
            count = sum(int(paper.bib["cites"])
                        for paper in author.publications)
            self.data.append(count)

    def generate_content(self):
        ymax = max(self.data)
        per_pixel = max(1, ymax // 44)
        self.add_title("Citation Counts", font="size4")
        graph = []
        for i in range(44):
            line = ""
            if self.data[0] > i:
                line += "w" * 30
            else:
                line += "-" * 30
            line += "-" * 10
            if self.data[1] > i:
                line += "w" * 30
            else:
                line += "-" * 30
            graph.append(line)
        self.print_image("\n".join(graph[::-1]), 4, 5)

        self.move_cursor(y=26, x=11)
        self.add_text("Matthew W Scroggs")
        self.move_cursor(y=26, x=53)
        self.add_text("J" + u"\u00F8" + "rgen S Dokken")

        for x in [3, 76]:
            self.move_cursor(y=25, x=x)
            self.add_text("0")

        for x in [3 - len(str(self.data[0])), 76]:
            self.move_cursor(y=25 - self.data[0] // (per_pixel * 2), x=x)
            self.add_text(str(self.data[0]))
        for x in [3 - len(str(self.data[1])), 76]:
            self.move_cursor(y=25 - self.data[1] // (per_pixel * 2), x=x)
            self.add_text(str(self.data[1]))


b_page = BarGraphPage("450")
b_page.importance = 5
