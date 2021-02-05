from ceefax.page import Page
from ceefax import config
from ceefax.helpers.time import datetime


class CountdownPage(Page):
    def __init__(self, page_num, who, when, numb=None):
        super().__init__(page_num)
        self.title = "Countdowns"
        self.who = who
        self.when = when
        if numb is not None:
            self.index_num = numb

    def generate_content(self):
        delta = self.when - config.now()
        hs = delta.seconds // 3600
        ds = delta.days
        days = "DAY"
        hours = "hr"

        if ds >= 0:
            if ds != 1:
                days += "S"
            if hs != 1:
                hours += "s"
            self.add_title("Countdown to...", font="size4", fg="ORANGE",
                           bg="BRIGHTWHITE")
            color = "RED"
        else:
            delta = config.now() - self.when
            hs = delta.seconds // 3600
            ds = delta.days
            if ds != 1:
                days += "S"
            if hs != 1:
                hours += "s"
            self.add_title("Time since...", font="size4", fg="ORANGE",
                           bg="BRIGHTWHITE")
            color = "BLUE"

        book_width = 30
        book_height = 34
        top_margin = 7
        left_margin = 49

        book = "x" * book_width + "\n"
        book += ("x" + "-" * (book_width - 2) + "x" + "\n") * (book_height - 2)
        book += "x" * book_width + "\n"
        book = book.replace(" ", "-").replace("x", "w")
        self.print_image(book, top_margin, left_margin)

        left_margin = 1
        self.move_cursor(y=8)
        self.add_title_wrapped(self.who, font="size4", fg="BLACK", bg="YELLOW",
                               pre=left_margin + 2, fill=False,
                               max_width=44, center=True)

        left_margin = 49
        self.move_cursor(y=8)

        self.add_title_wrapped(str(ds), font="size7", fg=color,
                               bg="BRIGHTWHITE", pre=left_margin + 2,
                               fill=False, max_width=26, center=True)
        self.add_title_wrapped(days, font="size4", fg="BLACK",
                               bg="BRIGHTWHITE", pre=left_margin + 2,
                               fill=False, max_width=26, center=True)
        self.add_title_wrapped(str(hs) + "|" + hours, font="size4",
                               fg="BRIGHTWHITE", bg="BLACK",
                               pre=left_margin + 2,
                               fill=False, max_width=26, center=True)


def next(month, day, hour, min):
    diff = None
    year = config.now().year
    while diff is None or diff.days < 0:
        out = datetime(year, month, day, hour, min)
        diff = out - config.now()
        year += 1
    return out


page1 = CountdownPage("110", "Christmas", next(12, 25, 0, 0), "110-121")
page2 = CountdownPage("111", "Lockdown 1", datetime(2020, 3, 23, 20, 30))
page3 = CountdownPage("112", "Lockdown 2", datetime(2020, 11, 5, 0, 1))
page4 = CountdownPage("113", "EMF2022", datetime(2022, 8, 21, 11, 0))
page5 = CountdownPage("114", "Pi Day", next(3, 14, 0, 0))
page6 = CountdownPage("115", "May Day", next(5, 1, 0, 0))
page7 = CountdownPage("116", "Ed Balls Day", next(4, 28, 0, 0))
page8 = CountdownPage("117", "Next year", next(1, 1, 0, 0))
page9 = CountdownPage("118", "US Election", datetime(2020, 11, 3, 0, 0))
page10 = CountdownPage("119", "UK left the EU", datetime(2020, 1, 31, 23, 0))
page11 = CountdownPage("120", "MathsJam", datetime(2020, 11, 21, 12, 0))
page12 = CountdownPage("121", "FEniCS 2021", datetime(2021, 3, 22, 12, 0))
page12.importance = 5
