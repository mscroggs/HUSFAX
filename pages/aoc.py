from ceefax.page import Page
from ceefax.helpers import url_handler
import config
from datetime import datetime


class AOCPage(Page):
    def __init__(self, page_num):
        super().__init__(page_num)
        self.importance = 2
        self.title = "Advent of Code Leaderboard"
        self.in_index = True

    def background(self):
        if datetime.now().month == 12:
            self.importance = 5
        else:
            self.importance = 2
        self.data = url_handler.load_json(
            ("https://adventofcode.com/2020/leaderboard/"
             "private/view/442442.json"),
            cookies={"session": config.aoc_session})

    def generate_content(self):
        self.add_title("Advent of Code", font='size4bold',
                       fg="YELLOW", bg="WHITE")
        people = [i for i in self.data["members"].values()
                  if len(i["completion_day_level"]) > 0]
        people.sort(key=lambda i: -i["local_score"])

        self.add_newline()

        for person in people:
            self.add_text(person["name"])
            self.move_cursor(x=20)
            self.add_text(str(person["local_score"]))
            self.move_cursor(x=25)
            stars = person["completion_day_level"]
            for i in range(1, 26):
                if str(i) in stars:
                    if "2" in stars[str(i)]:
                        self.add_text("*", fg="YELLOW")
                    else:
                        assert "1" in stars[str(i)]
                        self.add_text("*", fg="WHITE")
                else:
                    self.add_text(" ")
            self.add_newline()


page = AOCPage("510")
