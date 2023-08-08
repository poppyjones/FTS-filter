from bs4 import BeautifulSoup
import requests
import datetime
from team import Team

def get_team(team_path):

    if(team_path):
        url = "http://flattrackstats.com" + team_path
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        print("team found")
    else:
        with open("CRD A.html", encoding="utf8") as page:
            soup = BeautifulSoup(page, 'html.parser')

    # There are two tables, with the class rankingscontainer,
    # only the one on the right - the newest one - is styled with "rightflush"
    table_rows = soup.find(
        "div", id="quicktabs_tabpage_teams-rankings-drilldown_simple").find("tbody").find_all("tr")

    team = Team()
    team.name = soup.find("title").text.split(" | ")[0]
    # if a team is wftda associated there is a tab button to switch between fts and wftda rnakings
    # by searching for WFTDA we can check that the button exists on the page.
    team.wftda = bool(soup.find(string="WFTDA"))

    for row in table_rows:

        td_cols = row.find_all("td")

        # has format dd/mm/yy
        date_string = td_cols[0].text.strip(" \n")
        date_date = datetime.datetime.strptime(date_string, "%m/%d/%y")
        if date_date <= datetime.datetime(2021, 1, 1):
            break

        opponent = " ".join(td_cols[2].find("a").text.split())

        opponent_points = int(td_cols[2].find_all("span")[1].text[1:-1])
        team_points = int(td_cols[1].find_all("span")[1].text[1:-1])

        team.games.append([opponent,team_points,opponent_points, date_date])

        ## Unsure if this is necessary on team page
        ## # handle long team names
        ## team = cols[2].text if len(cols[2].find_all(
        ##     "span")) == 0 else cols[2].find("span")["title"]
    return team

if __name__ == "__main__":
    get_team(None)