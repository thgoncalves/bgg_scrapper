"""Main boardgame script file"""

import pickle
import pandas as pd

import bgg_api_pull
import games_to_df

num_pages = 250

if __name__ == "__main__":
    ## Get boardgame names and IDs for the top xxx games (100 * num_pages)
    all_games = bgg_api_pull.list_to_boardgame_class(num_pages)
    pickle.dump(all_games, open("./data/Raw/all_games_50000.pkl", "wb"))
    print("Scraping complete")
    
    ## Cast `all_games` list to data frame, then save as a SQL database
    games_df = games_to_df.all_games_to_pd_DF(all_games)
    games_database = games_to_df.Database('./data/boardgames_sql.db')
    games_df.to_sql("games", games_database.connection, if_exists='replace')
    
    ## Validation
    print("--- SQL Query - Validation ---")
    print(pd.read_sql_query("SELECT COUNT(*) Num_Games_in_DB FROM games;",
                            games_database.connection))
    games_database.connection.commit()
    games_database.connection.close()
