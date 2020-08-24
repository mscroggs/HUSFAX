from ceefax.page import Page
from ceefax.helpers.url_handler import load_csv
import datetime


class LottoPage(Page):
    def __init__(self, page_num):
        super(LottoPage, self).__init__(page_num)
        self.importance = 3
        self.title = "Lotto results"
        self.index_num = str(page_num)
        self.tagline = "Don't win a little..."

    def background(self):
        data = load_csv("https://www.national-lottery.co.uk/"
                        "results/lotto/draw-history/csv")
        res = data[1]
        self.date = datetime.datetime.strptime(res[0], "%m-%b-%Y")
        self.numbers = [str(j) for j in sorted([int(i) for i in res[1:7]])]
        self.bonus = res[7]
        self.set_of_balls = res[8]
        self.machine = res[9]

    def generate_content(self):
        self.add_title("Lotto Results")

        self.move_cursor(y=8)
        self.add_title(self.date.strftime("%a %-d %b"),
                       font='size4', fg="BLACK", bg="WHITE")

        col = "CYAN"
        for i, n in enumerate(self.numbers):
            self.move_cursor(y=12)
            self.add_title(n, pre=11 * i, fg="BLACK",
                           bg=col, fill=False, font='size4')
            if col == "CYAN":
                col = "YELLOW"
            else:
                col = "CYAN"
        self.move_cursor(y=12)
        self.add_title(self.bonus, pre=68, fg="BLACK",
                       bg="RED", fill=False, font='size4')

        self.move_cursor(y=17)
        self.add_title(self.machine, font='size4', fg="BLACK", bg="YELLOW")
        self.add_title("Set of balls number " + self.set_of_balls,
                       font='size4', fg="BLACK", bg="YELLOW")


lotto_page = LottoPage(555)
