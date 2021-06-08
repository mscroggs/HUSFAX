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

        self.load()

    def load(self):
        self.points = {
            i: [{"name": k, "P": 0, "W": 0, "D": 0, "L": 0, "Pts": 0, "GF": 0, "GA": 0, "GD": 0}
                for k in j]
            for i, j in self.groups.items()
        }
        self.matches = []

        try:
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': config.football_data_token}
            connection.request('GET', '/v2/competitions/EC/matches?season=2021', None, headers)
            response = json.loads(connection.getresponse().read().decode())

            for m in response["matches"]:
                if m["group"] is not None:
                    g = m["group"][-1]
                    home = m["homeTeam"]["name"]
                    away = m["awayTeam"]["name"]
                    winner = m["score"]["winner"]
                    if winner is not None:
                        self.points[g][home]["P"] += 1
                        self.points[g][away]["P"] += 1
                        self.points[g][home]["GF"] += m["score"]["fullTime"]["homeTeam"]
                        self.points[g][home]["GD"] += m["score"]["fullTime"]["homeTeam"]
                        self.points[g][home]["GA"] += m["score"]["fullTime"]["awayTeam"]
                        self.points[g][home]["GD"] -= m["score"]["fullTime"]["awayTeam"]
                        self.points[g][away]["GF"] += m["score"]["fullTime"]["awayTeam"]
                        self.points[g][away]["GD"] += m["score"]["fullTime"]["awayTeam"]
                        self.points[g][away]["GA"] += m["score"]["fullTime"]["homeTeam"]
                        self.points[g][away]["GD"] -= m["score"]["fullTime"]["homeTeam"]
                        if winner == "HOME_TEAM":
                            self.points[g][home]["W"] += 1
                            self.points[g][home]["Pts"] += 3
                            self.points[g][away]["L"] += 1
                        elif winner == "AWAY_TEAM":
                            self.points[g][away]["W"] += 1
                            self.points[g][away]["Pts"] += 3
                            self.points[g][home]["L"] += 1
                        else:
                            self.points[g][away]["D"] += 1
                            self.points[g][away]["Pts"] += 1
                            self.points[g][home]["D"] += 1
                            self.points[g][home]["Pts"] += 1

            for m in response["matches"]:
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
                self.matches.append({
                    "day": day, "month": month, "hour": hour, "minute": minute,
                    "home": home, "away": away, "group": m['group'],
                    "homegoals": m["score"]["fullTime"]["homeTeam"],
                    "awaygoals": m["score"]["fullTime"]["awayTeam"]
                })

            for group in self.points:
                self.points[group].sort(key=lambda x: (x["Pts"], x["GD"], x["GF"]))
        except:
            pass

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

    def generate_content(self):
        self.add_title("Euro 2020 Knockout", font="size4")
        self.add_newline()
        for m in self.data.matches:
            if m["group"] is None:
                if m["homegoals"] is None:
                    self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']} ")
                    self.add_text(" " * (15 - len(m['home'])))
                    self.add_text(m['home'] + " vs " + m['away'])
                    self.add_newline()
                else:
                    self.add_text(f"{m['day']} {m['month']} {m['hour']}:{m['minute']} ")
                    self.add_text(" " * (15 - len(m['home'])))
                    self.add_text(m['home'] + " " + str(m['homegoals']))
                    self.add_text(" - ")
                    self.add_text(str(m['awaygoals']) + " " + m['away'])
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
                self.add_text(m['home'] + " " + str(m['homegoals']))
                self.add_text(" - ")
                self.add_text(str(m['awaygoals']) + " " + m['away'])
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
                self.add_text(m['home'] + " vs " + m['away'])
                self.add_newline()


d = FootballData()
page0 = EuroPage(d)
page1 = EuroGroups(d)
page2 = EuroKnockout(d)
page3 = EuroResults(d)
page4 = EuroFixtures(d)

if datetime.now().year == 2021 and datetime.now().month in [6, 7]:
    page1.importance = 5
    page2.importance = 5
    page3.importance = 5
    page4.importance = 5
