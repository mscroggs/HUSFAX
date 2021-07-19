from ceefax.page import Page
from datetime import datetime
import http.client
import json
import config


class FootballData:
    def __init__(self):
        self.groups = {
            "A": ["Italy", "Switzerland", "Turkey", "Wales"],
            "B": ["Belgium", "Denmark", "Finland", "Russia"],
            "C": ["Austria", "Netherlands", "North Macedonia", "Ukraine"],
            "D": ["Croatia", "Czech Republic", "England", "Scotland"],
            "E": ["Poland", "Slovakia", "Spain", "Sweden"],
            "F": ["France", "Germany", "Hungary", "Portugal"]
        }

        self.colours = {
            "England": "GREEN",
            "Scotland": "GREEN",
            "Wales": "GREEN",
            "Poland": "GREEN",
            "North Macedonia": "GREEN",
            "Germany": "MAGENTA",
            "Switzerland": "MAGENTA",
            "???": "GREY"
        }

    def load(self):
        self.points = {
            i: [{"name": k, "P": 0, "W": 0, "D": 0, "L": 0, "Pts": 0, "GF": 0, "GA": 0, "GD": 0}
                for k in j]
            for i, j in self.groups.items()
        }
        self.matches = [
            {
                "day": "??", "month": "Juny", "hour": "00", "minute": "00",
                "home": "???", "away": "???", "group": None,
                "homegoals": None, "awaygoals": None
            } for i in range(51)]

        if config.football_data_token is not None:
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': config.football_data_token}
            connection.request('GET', '/v2/competitions/EC/matches?season=2021', None, headers)
            response = json.loads(connection.getresponse().read().decode())

            for m in response["matches"]:
                if m["group"] is not None:
                    g = m["group"][-1]
                    home = m["homeTeam"]["name"]
                    away = m["awayTeam"]["name"]
                    home_n = None
                    away_n = None
                    for i, j in enumerate(self.points[g]):
                        if j["name"] == home:
                            home_n = i
                        if j["name"] == away:
                            away_n = i
                    winner = m["score"]["winner"]
                    if winner is not None:
                        self.points[g][home_n]["P"] += 1
                        self.points[g][away_n]["P"] += 1
                        self.points[g][home_n]["GF"] += m["score"]["fullTime"]["homeTeam"]
                        self.points[g][home_n]["GD"] += m["score"]["fullTime"]["homeTeam"]
                        self.points[g][home_n]["GA"] += m["score"]["fullTime"]["awayTeam"]
                        self.points[g][home_n]["GD"] -= m["score"]["fullTime"]["awayTeam"]
                        self.points[g][away_n]["GF"] += m["score"]["fullTime"]["awayTeam"]
                        self.points[g][away_n]["GD"] += m["score"]["fullTime"]["awayTeam"]
                        self.points[g][away_n]["GA"] += m["score"]["fullTime"]["homeTeam"]
                        self.points[g][away_n]["GD"] -= m["score"]["fullTime"]["homeTeam"]
                        if winner == "HOME_TEAM":
                            self.points[g][home_n]["W"] += 1
                            self.points[g][home_n]["Pts"] += 3
                            self.points[g][away_n]["L"] += 1
                        elif winner == "AWAY_TEAM":
                            self.points[g][away_n]["W"] += 1
                            self.points[g][away_n]["Pts"] += 3
                            self.points[g][home_n]["L"] += 1
                        else:
                            self.points[g][away_n]["D"] += 1
                            self.points[g][away_n]["Pts"] += 1
                            self.points[g][home_n]["D"] += 1
                            self.points[g][home_n]["Pts"] += 1

            for i, m in enumerate(response["matches"]):
                date = m["utcDate"].split("T")[0]
                year, month, day = date.split("-")
                if month == "06":
                    month = "June"
                if month == "07":
                    month = "July"
                hour, minute = m["utcDate"].split("T")[1][:-4].split(":")
                hour = str(int(hour) + 1)
                home = m["homeTeam"]["name"]
                away = m["awayTeam"]["name"]
                if home is None:
                    home = "???"
                if away is None:
                    away = "???"
                self.matches[i] = {
                    "day": day, "month": month, "hour": hour, "minute": minute,
                    "home": home, "away": away, "group": m['group'],
                    "homegoals": m["score"]["fullTime"]["homeTeam"],
                    "awaygoals": m["score"]["fullTime"]["awayTeam"]
                }

            for group in self.points:
                self.points[group].sort(key=lambda x: (-x["Pts"], -x["GD"], -x["GF"]))


class EuroPage(Page):
    def __init__(self, data):
        super().__init__("200")
        self.data = data
        self.title = "Euro 2020"
        self.tagline = "It's coming home"
        self.index_num = "200-204"

    def background(self):
        self.data.load()

    def generate_content(self):
        self.add_title("Euro 2020")
        self.add_newline()
        for n, name in [
            ("201", "Groups"),
            ("202", "Knockout"),
            ("203", "Results"),
            ("204", "Fixtures"),
        ]:
            self.add_text(n + " ", fg="YELLOW")
            self.add_text(name)
            self.add_newline()


class EuroGroups(Page):
    def __init__(self, data):
        super().__init__("201")
        self.data = data
        self.title = "Euro 2020 Groups"
        self.tagline = "It's coming home"

    def generate_content(self):
        self.add_title("Euro 2020 Groups", font="size4")
        for n, group in enumerate(self.data.points):
            if n % 3 == 0:
                self.move_cursor(y=5)
            if n >= 3:
                st = 40
            else:
                st = 0
            self.move_cursor(x=st)
            self.add_text(f"Group {group}", fg="YELLOW")
            self.move_cursor(x=st + 16)
            self.add_text("P", fg="BLUE")
            self.move_cursor(x=st + 18)
            self.add_text("W", fg="BLUE")
            self.move_cursor(x=st + 20)
            self.add_text("D", fg="BLUE")
            self.move_cursor(x=st + 22)
            self.add_text("L", fg="BLUE")
            self.move_cursor(x=st + 24)
            self.add_text("GD", fg="BLUE")
            self.move_cursor(x=st + 28)
            self.add_text("Pts", fg="BLUE")
            self.add_newline()
            for team in self.data.points[group]:
                self.move_cursor(x=st)
                if team["name"] in self.data.colours:
                    self.add_text(team["name"], fg=self.data.colours[team["name"]])
                else:
                    self.add_text(team["name"])
                self.move_cursor(x=st + 16)
                self.add_text(str(team["P"]))
                self.move_cursor(x=st + 18)
                self.add_text(str(team["W"]))
                self.move_cursor(x=st + 20)
                self.add_text(str(team["D"]))
                self.move_cursor(x=st + 22)
                self.add_text(str(team["L"]))
                self.move_cursor(x=st + 24)
                self.add_text(str(team["GD"]))
                self.move_cursor(x=st + 28)
                self.add_text(str(team["Pts"]))
                self.add_newline()
            self.add_newline()
            self.add_newline()


class EuroKnockout(Page):
    def __init__(self, data):
        super().__init__("202")
        self.data = data
        self.title = "Euro 2020 Knockout"
        self.tagline = "It's coming home"

    def add_team_name(self, name, align="left", bg=None):
        if name is None:
            name = "???"
        if align == "right":
            self.add_text(" " * (16 - len(name)), bg=bg)
        if align == "center":
            self.add_text(" " * (8 - len(name) // 2), bg=bg)
        if name in self.data.colours:
            self.add_text(name, fg=self.data.colours[name], bg=bg)
        else:
            self.add_text(name, bg=bg)
        if align == "left":
            self.add_text(" " * (16 - len(name)), bg=bg)
        if align == "center":
            self.add_text(" " * (8 - len(name) + len(name) // 2), bg=bg)

    def add_match_right(self, n, x=0, y=0, bg="PINK"):
        m = self.data.matches[n]
        self.move_cursor(x=x, y=y)
        self.add_team_name(m["home"], "right", bg=bg)
        if m["homegoals"] is None:
            self.add_text("  ", bg=bg)
        else:
            self.add_text(f" {m['homegoals']}", bg=bg)
        self.move_cursor(x=x, y=y + 1)
        self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']}", fg=bg)
        self.add_text(" vs  ", bg=bg)
        self.move_cursor(x=x, y=y + 2)
        self.add_team_name(m["away"], "right", bg=bg)
        if m["awaygoals"] is None:
            self.add_text("  ", bg=bg)
        else:
            self.add_text(f" {m['awaygoals']}", bg=bg)

    def add_match_left(self, n, x=0, y=0, bg="PINK"):
        m = self.data.matches[n]
        self.move_cursor(x=x, y=y)
        if m["homegoals"] is None:
            self.add_text("  ", bg=bg)
        else:
            self.add_text(f"{m['homegoals']} ", bg=bg)
        self.add_team_name(m["home"], "left", bg=bg)
        self.move_cursor(x=x, y=y + 1)
        self.add_text("  vs ", bg=bg)
        self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']}", fg=bg)
        self.move_cursor(x=x, y=y + 2)
        if m["awaygoals"] is None:
            self.add_text("  ", bg=bg)
        else:
            self.add_text(f"{m['awaygoals']} ", bg=bg)
        self.add_team_name(m["away"], "left", bg=bg)

    def add_match_bottom(self, n, x=0, y=0, bg="PINK"):
        m = self.data.matches[n]
        self.move_cursor(x=x, y=y)
        self.add_team_name(m["home"], "right", bg=bg)
        if m["homegoals"] is None:
            self.add_text("  vs  ", bg=bg)
        else:
            self.add_text(f" {m['homegoals']}  {m['awaygoals']} ", bg=bg)
        self.add_team_name(m["away"], "left", bg=bg)
        self.move_cursor(x=x + 12, y=y + 1)
        self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']}", fg=bg)

    def add_match_top(self, n, x=0, y=0, bg="PINK"):
        m = self.data.matches[n]
        self.move_cursor(x=x + 12, y=y)
        self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']}", fg=bg)
        self.move_cursor(x=x, y=y + 1)
        self.add_team_name(m["home"], "right", bg=bg)
        if m["homegoals"] is None:
            self.add_text("  vs  ", bg=bg)
        else:
            self.add_text(f" {m['homegoals']}  {m['awaygoals']} ", bg=bg)
        self.add_team_name(m["away"], "left", bg=bg)

    def add_match_final(self, n, x=0, y=0, bg="PINK"):
        m = self.data.matches[n]
        self.move_cursor(x=x, y=y)
        self.add_team_name(m["home"], "center", bg=bg)
        self.move_cursor(x=x, y=y + 1)
        self.add_text(" " * 16, bg=bg)
        if m["homegoals"] is not None:
            self.move_cursor(x=x + 7, y=y + 1)
            self.add_text(m['homegoals'], bg=bg)
        self.move_cursor(x=x, y=y + 2)
        self.add_text(" ", bg=bg)
        self.move_cursor(x=x + 1, y=y + 2)
        self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']}", fg=bg)
        self.move_cursor(x=x + 15, y=y + 2)
        self.add_text(" ", bg=bg)
        self.move_cursor(x=x, y=y + 3)
        self.add_text(" " * 16, bg=bg)
        if m["awaygoals"] is not None:
            self.move_cursor(x=x + 8, y=y + 1)
            self.add_text(m['awaygoals'], bg=bg)
        self.move_cursor(x=x, y=y + 4)
        self.add_team_name(m["away"], "center", bg=bg)

    def generate_content(self):
        self.add_title("Euro 2020 Knockout", font="size4")
        self.add_match_right(39, x=0, y=5)
        self.add_match_right(37, x=0, y=11)
        self.add_match_right(43, x=0, y=17)
        self.add_match_right(42, x=0, y=23)
        self.add_match_left(41, x=62, y=5)
        self.add_match_left(40, x=62, y=11)
        self.add_match_left(38, x=62, y=17)
        self.add_match_left(36, x=62, y=23)

        self.add_match_right(45, x=20, y=6, bg="CYAN")
        self.add_match_left(44, x=42, y=6, bg="CYAN")
        self.add_match_right(47, x=20, y=22, bg="CYAN")
        self.add_match_left(46, x=42, y=22, bg="CYAN")

        self.add_match_top(48, x=21, y=10, bg="ORANGE")
        self.add_match_bottom(49, x=21, y=19, bg="ORANGE")

        self.add_match_final(50, x=32, y=13, bg="GREY")

        ar = chr(8594)
        al = chr(8592)
        au = chr(8593)
        ad = chr(8595)
        self.move_cursor(x=18, y=6)
        self.add_text(f"{ar}{ar}")
        self.move_cursor(x=18, y=24)
        self.add_text(f"{ar}{ar}")
        self.move_cursor(x=60, y=6)
        self.add_text(f"{al}{al}")
        self.move_cursor(x=60, y=24)
        self.add_text(f"{al}{al}")

        self.move_cursor(x=17, y=10)
        self.add_text(f"{au}")
        self.move_cursor(x=17, y=9)
        self.add_text(f"{ar}{ar}{au}")
        self.move_cursor(x=19, y=8)
        self.add_text(f"{ar}")

        self.move_cursor(x=62, y=10)
        self.add_text(f"{au}")
        self.move_cursor(x=60, y=9)
        self.add_text(f"{au}{al}{al}")
        self.move_cursor(x=60, y=8)
        self.add_text(f"{al}")

        self.move_cursor(x=17, y=20)
        self.add_text(f"{ad}")
        self.move_cursor(x=17, y=21)
        self.add_text(f"{ar}{ar}{ad}")
        self.move_cursor(x=19, y=22)
        self.add_text(f"{ar}")

        self.move_cursor(x=62, y=20)
        self.add_text(f"{ad}")
        self.move_cursor(x=60, y=21)
        self.add_text(f"{ad}{al}{al}")
        self.move_cursor(x=60, y=22)
        self.add_text(f"{al}")

        self.move_cursor(x=26, y=9)
        self.add_text(f"{ad}")
        self.move_cursor(x=26, y=10)
        self.add_text(f"{ad}")

        self.move_cursor(x=53, y=9)
        self.add_text(f"{ad}")
        self.move_cursor(x=53, y=10)
        self.add_text(f"{ad}")

        self.move_cursor(x=26, y=21)
        self.add_text(f"{au}")
        self.move_cursor(x=26, y=20)
        self.add_text(f"{au}")

        self.move_cursor(x=53, y=21)
        self.add_text(f"{au}")
        self.move_cursor(x=53, y=20)
        self.add_text(f"{au}")

        self.move_cursor(x=38, y=18)
        self.add_text(f"{au}{au}{au}{au}")

        self.move_cursor(x=38, y=12)
        self.add_text(f"{ad}{ad}{ad}{ad}")

        return

        for m in self.data.matches:
            if m["group"] is None:
                if m["homegoals"] is None:
                    self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']} ")
                    self.add_text(" " * (15 - len(m['home'])))
                    if m["home"] in self.data.colours:
                        self.add_text(m['home'], fg=self.data.colours[m["home"]])
                    else:
                        self.add_text(m['home'])
                    self.add_text(" vs ")
                    if m["away"] in self.data.colours:
                        self.add_text(m['away'], fg=self.data.colours[m["away"]])
                    else:
                        self.add_text(m['away'])
                    self.add_newline()
                else:
                    self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']} ")
                    self.add_text(" " * (15 - len(m['home'])))
                    if m["home"] in self.data.colours:
                        self.add_text(m['home'], fg=self.data.colours[m["home"]])
                    else:
                        self.add_text(m['home'])
                    self.add_text(" " + str(m['homegoals']))
                    self.add_text(" - ")
                    self.add_text(str(m['awaygoals']) + " ")
                    if m["away"] in self.data.colours:
                        self.add_text(m['away'], fg=self.data.colours[m["away"]])
                    else:
                        self.add_text(m['away'])
                    self.add_newline()


class EuroResults(Page):
    def __init__(self, data):
        super().__init__("203")
        self.data = data
        self.title = "Euro 2020 Results"
        self.tagline = "It's coming home"

    def generate_content(self):
        self.add_title("Euro 2020 Results", font="size4")
        self.add_newline()
        for m in self.data.matches[::-1]:
            if m["homegoals"] is not None:
                self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']} ")
                self.add_text(" " * (15 - len(m['home'])))
                if m["home"] in self.data.colours:
                    self.add_text(m['home'], fg=self.data.colours[m["home"]])
                else:
                    self.add_text(m['home'])
                self.add_text(f" {m['homegoals']} - {m['awaygoals']} ")
                if m["away"] in self.data.colours:
                    self.add_text(m['away'], fg=self.data.colours[m["away"]])
                else:
                    self.add_text(m['away'])
                self.add_newline()


class EuroFixtures(Page):
    def __init__(self, data):
        super().__init__("204")
        self.data = data
        self.title = "Euro 2020 Fixtures"
        self.tagline = "It's coming home"

    def generate_content(self):
        self.add_title("Euro 2020 Fixtures", font="size4")
        self.add_newline()
        for m in self.data.matches:
            if m["homegoals"] is None:
                self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']} ")
                self.add_text(" " * (15 - len(m['home'])))
                if m["home"] in self.data.colours:
                    self.add_text(m['home'], fg=self.data.colours[m["home"]])
                else:
                    self.add_text(m['home'])
                self.add_text(" vs ")
                if m["away"] in self.data.colours:
                    self.add_text(m['away'], fg=self.data.colours[m["away"]])
                else:
                    self.add_text(m['away'])
                self.add_newline()


d = FootballData()
page0 = EuroPage(d)
page1 = EuroGroups(d)
page2 = EuroKnockout(d)
page3 = EuroResults(d)
page4 = EuroFixtures(d)
