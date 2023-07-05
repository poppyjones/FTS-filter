from bs4 import BeautifulSoup
import requests

# uncomment to fetch new data rather than using the save html
#url = "http://flattrackstats.com/rankings/women/women_europe"
#page = requests.get(url)
#soup = BeautifulSoup(page.content, "html.parser")

with open("ranking page.html", encoding="utf8") as page:
    soup = BeautifulSoup(page, 'html.parser')

# There are two tables, with the class rankingscontainer,
# only the one on the right - the newest one - is styled with "rightflush"
table_rows = soup.find("td", class_="rightflush").find("tbody").find_all("tr")

name = input("What is the name of the file?\n")
filename = f"output/{name}.html"

with open(filename, "w", encoding="utf-8") as file:
    for row in table_rows:
        cols = row.find_all("td")

        ranking = cols[0].text
        team_url = cols[2].find("a")["href"]

        # handle long team names
        team = cols[2].text if len(cols[2].find_all("span")) == 0 else cols[2].find("span")["title"]

        rating = cols[3].text

        file.write(f"{ranking} {team}, {rating}\n")

        # Get most recent games

        exit()

        
# each table is in a .rankingscontainer

exit()

soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
print(soup.prettify())