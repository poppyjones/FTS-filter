from datetime import datetime
from bs4 import BeautifulSoup
import requests
import team_page_scraper as tps

# uncomment to fetch new data rather than using the saved html
url = "http://flattrackstats.com/rankings/women/women_europe"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# uncomment to use the saved html rather than fetching new data
# with open("ranking page.html", encoding="utf8") as page:
#     soup = BeautifulSoup(page, 'html.parser')

# There are two tables, with the class rankingscontainer,
# only the one on the right - the newest one - is styled with "rightflush"
table_rows = soup.find("td", class_="rightflush").find("tbody").find_all("tr")

name = input("What is the name of the file?\n")
filename = f"output/{name}.txt"

recent_games = input("Print with recent games? (y/n)\n") == "y"
only_wftda = input("Remove non-WFTDA teams? (y/n)\n") == "y"

with open(filename, "w", encoding="utf-8") as file:
    for row in table_rows:
        cols = row.find_all("td")

        ranking = cols[0].text
        team_path = cols[2].find("a")["href"]

        # handle long team names
        team_name = cols[2].text if len(cols[2].find_all("span")) == 0 else cols[2].find("span")["title"]

        rating = cols[3].text
        
        team = tps.get_team(team_path)
        if(team.games):
            if(not (only_wftda and not team.wftda)):
                wftda_string = "" if only_wftda else ("(non-WFTDA)" if not team.wftda else "(WFTDA!)")
                file.write(f"{ranking} {team_name} {wftda_string}, {rating}\n")
                if(recent_games):
                    year = datetime.now().year
                    file.write(f"  {year}\n")         

                    for g in team.games:
                        if(g[3].year != year):
                            year = g[3].year
                            file.write(f"  {year}\n")         
                        
                        winning_string = "won " if g[1] > g[2] else "lost"
                        file.write(f"    {winning_string} against {g[0]} with {g[1]} to {g[2]} ({round(g[1]/g[2], 3)} ratio)\n")
            else:
                print(team_name, "is not WFTDA associated")
        else:
            print(team_name, "hasn't played any games since the panini")
