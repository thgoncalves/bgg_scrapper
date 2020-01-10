"""Uses BGG XMLAPI2 to get information about games on BGG"""

from urllib.request import urlopen
import requests
import re
from bs4 import BeautifulSoup as BS

import xmltodict
import time
import pickle

from boardgame import BoardGame # pylint: disable=E0401

def pull_game_names(page):
    """Get all game names and IDs from a page of BGG website.
    
    Description:
        Scrapes Board Game Geek website games in order of rank.
        Returns a dictionary of games titles:BGG ID, given a page number
        Games are listed in increments of 50
        
    inputs:
        page (int): Page number (starts at 1)
        
    returns:
        game_list (dict): {Name:ID}
    """
    url = 'https://boardgamegeek.com/browse/boardgame/page/{}'.format(page)
    bgg_page = urlopen(url)
    my_bytes = bgg_page.read()
    url_text = my_bytes.decode("utf8")
    bgg_page.close()
    url_text = BS(url_text, 'html.parser')
    
    games = url_text.find_all("td", class_="collection_objectname")
    
    def get_game_name(item):
        game_name = item.findNext('a').text
        return(game_name)
        
    def get_game_ID(item):
        game_link_id = str(item.findNext('a'))
        game_link_id = re.search('[0-9]{1,7}', game_link_id).group(0)
        return(int(game_link_id))
    
    game_list = {get_game_name(ii):get_game_ID(ii) for ii in games}
    return(game_list)

def boardgame_info(ID):
    """Access BGG API and return information
    
    Description:
        Uses BoardGameGeek's XML API 2 to retrieve information
        and statistics about a given boardgame using its BGG
        item number.
        
    input:
        ID (int): A BGG boardgame ID number (scraped with pull_game_names())
        
    returns:
        bg_dict (dict): A big dictionary containing lots of game information
    """
    
    if not type(ID) is int:
        raise('ID must be an integer')
    else:
        url = 'https://boardgamegeek.com/xmlapi2/thing?id=%d&stats=1' % ID
        page = requests.get(url)
        try:
            bg_dict = xmltodict.parse(page.content)
            return(bg_dict)
        except:
            return(None)

def list_to_boardgame_class(num_pages):
    """Return list of Boardgame Objects
    
    Description:
        Calls pull_game_names() and boardgame_info(), passing information to 
        Boardgame() class, and returns a list of all class objects.
     
    Input:
        num_pages (int): Number of pages of games (100 per page)
    
    Returns:
        all_games (list): List of each game as a Boardgame object
    
    """
    ## Get boardgame names and IDs for the top 1000 games (10 pages)
    game_list = [pull_game_names(ii) for ii in range(1, num_pages + 1)]
    game_IDs = [x for y in list([ii.values() for ii in game_list]) for x in y]
    
    ## Connect IDs with BGG API, get game information
    all_games = []
    
    def id_to_boardgame(ID):
        game_info = boardgame_info(ID)
        game = BoardGame(game_info)
	  
        time.sleep(2)
        
        try:
            if 'error' in game.data():
                time.sleep(5)
                id_to_boardgame(ID)
            else:
                return(game)
        except:
            return(None)
    
    for ID in game_IDs:
	    all_games.append(id_to_boardgame(ID))
    
    return(all_games)

# if __name__ == "__main__":
#     ## Get boardgame names and IDs for the top 25,000 games (250 pages)
#     all_games = list_to_boardgame_class(1)
#     pickle.dump(all_games, open("./data/Raw/all_games_100.pkl", "wb"))