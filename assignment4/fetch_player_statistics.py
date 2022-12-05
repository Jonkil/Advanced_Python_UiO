import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html
import pandas as pd
import seaborn as sns

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {}
    for team in teams: 
        all_players[team['name']] = get_players(team['url'])

    # get player statistics for each player,
    # using get_player_stats
    all_stats = {}
    for team, players in all_players.items():
        team_stats = []
        
        for player in players:
            stats = get_player_stats(player['url'], team)
            team_stats.append({'name':player['name'], **stats})
            
        all_stats[team] = team_stats
    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }

    # Select top 3 for each team by points:
    best = {}
    top_stat = 'points'
    for team, players in all_stats.items():
        # Sort and extract top 3 based on points
        top_3 = sorted(players, key=lambda d: d['points'], reverse=True)[:3]
        best[team] = top_3
        
    stats_to_plot = ['points', 'assists', 'rebounds']
    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    
    stats_dir = 'NBA_player_statistics'
    
    # create a dataframe from given input    
    df = pd.DataFrame([],
                      columns=['team', 'name', stat],
                      index=range(24))
    
    idx = 0
    for team, players in best.items():
        for player in players:
            df.loc[idx, 'team']= team
            df.loc[idx, 'name']= player['name']
            df.loc[idx, stat]= player[stat]
            idx += 1
    df[stat] = df[stat].astype(float)
    
    # sorted dataframe with new column - rank
    df1 = df.sort_values(['team',stat],ascending=False).groupby('team').head()
    df1 = df1.reset_index(drop=True)
    df1['rank']= ['Best', 'Second', 'Third']*8

    # plot vertical barplot
    sns.set(rc={'figure.figsize':(12,8)})
    ax = sns.barplot(x='team', y=stat,
                    data=df1, hue='rank')
    
    # label each bar in barplot
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(x = p.get_x()+(p.get_width()/2), 
        y = height+0.2, 
        s = df1['name'][i], 
        ha = 'center',
        rotation='vertical') 

    ax.set_ylabel(stat)
    ax.set_xlabel("")
    ax.legend(loc='upper right',
            title='Player ranking within team based on '+stat,
            bbox_to_anchor=(1.25, 1.25))
    
    plt.savefig(stats_dir+'/'+stat+'.png', bbox_inches='tight', format='png')
    del ax
 
def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    roster = soup.find(id="Roster")
    table = roster.find_next("table", {"class": "sortable"})

    players = []
    # Loop over every row and get the names from roster
    rows = rows = table.find_all(["tr"])
    
    for row in rows[1:]:
        cols = row.find_all(["a"])
        name = cols[1].get_text()
        url = urljoin(base_url, cols[1]["href"])
        players.append({'name':name, 'url':url})

    # return list of players

    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find(id="Regular_season")
    
    stats = {'rebounds': 0, 
            'assists': 0, 
            'points': 0}
        
    if not heading:
        print(f'Regular season table not found in URL:{player_url}.')
        print('Returned zeros in stats.')
        return stats
    
    table = heading.find_next("table")
    
    # names of columns
    _keys = [s.get_text(strip=True) for s in table.find_all('th')]
    


    rows = table.find_all(["tr"])
    
    def make_float(str_num: str) -> float:
        """Converts string to float.
            Removes possible '*' characters.

        Args:
            str_num (_type_): number as string

        Returns:
            float: number as float
        """
        return float(''.join([x for x in str_num if not x=='*']))
    
    # Loop over rows and extract the stats
    for row in rows[1:]:
        cols = row.find_all('td')
        # get values written in the current row
        _vals = [rec.get_text(strip=True) for rec in cols]
        vals = dict(zip(_keys, _vals))
        if vals['Year'].startswith('2021') and team in vals['Team']:
            stats['rebounds'] = make_float(vals['RPG'])
            stats['assists'] = make_float(vals['APG'])
            stats['points'] = make_float(vals['PPG'])
            
    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
