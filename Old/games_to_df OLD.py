"""Games to Pandas DF"""

import re, time, pickle
import pandas as pd
import numpy as np
import sqlite3

from boardgame import BoardGame # pylint: disable=E0401

class Database():
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.db = self.connection.cursor()

def all_games_to_pd_DF(lst):
    """Moves list to Pandas DF
    
    Description:
        Converts object returned by list_to_boardgame_class() to a
        Pandas DataFrame.
    
    Input:
    lst (list): List object from list_to_boardgame_class()
    
    Returns:
    bg_df (pd.DataFrame): DataFrame with all information. Also saves as a CSV
    """
    all_games = lst[:]
    bg_df = pd.DataFrame()
    
    ## Basic Info
    bg_df['Name'] = [i.name for i in all_games]
    bg_df['ID'] = [i.id for i in all_games]
    bg_df['Year'] = [i.year_published for i in all_games]
    
    ## Rating
    bg_df['Num_Ratings'] = [i.users_rated for i in all_games]
    bg_df['Avg_Rating'] = [i.avg_rating for i in all_games]
    bg_df['Bayes_Avg_Rating'] = [i.bayes_avg_rating for i in all_games]
    bg_df['Avg_Weight'] = [i.avg_weight for i in all_games]
    bg_df['StDev_Rating'] = [i.stdev_rating for i in all_games]
    
    ## Players
    bg_df['Pub_Min_Age'] = [i.min_age for i in all_games]
    
    BGG_Min_Age = []
    for i in all_games:
        try:
            BGG_Min_Age.append(i.suggested_player_age)
        except:
            BGG_Min_Age.append(np.nan)
    
    bg_df['BGG_Min_Age'] = BGG_Min_Age
    bg_df['Pub_Min_Players'] = [i.min_players for i in all_games]
    bg_df['Pub_Max_Players'] = [i.max_players for i in all_games]
    
    BGG_Num_Players = []
    for i in all_games:
        try:
            BGG_Num_Players.append(i.suggested_players)
        except:
            BGG_Num_Players.append(np.nan)
    
    bg_df['BGG_Num_Players'] = BGG_Num_Players
    bg_df['Play_Time'] = [i.playing_time for i in all_games]
    
    ## Ownership & Community Engagement
    bg_df['Num_Owned'] = [i.num_owned for i in all_games]
    bg_df['Num_Comments'] = [i.num_comments for i in all_games]
    bg_df['Num_Trading'] = [i.num_trading for i in all_games]
    bg_df['Num_Wanting'] = [i.num_wanting for i in all_games]
    bg_df['Num_Wishing'] = [i.num_wishing for i in all_games]
    bg_df['Num_Weights'] = [i.num_weights for i in all_games]
    
    ### Ranks
    rank_categories = []
    for i in all_games:
        rank_categories.append(list(i.rank.keys()))
    
    unique_rank_categories = list(set([i for j in rank_categories for i in j]))
    rank_columns = ['Name', 'ID'] + unique_rank_categories
    major_rank_df = pd.DataFrame(columns = rank_columns)
    
    for game in all_games:
        rank_data = game.rank
        rank_data['Name'] = game.name
        rank_data['ID'] = game.id
        minor_rank_df = pd.DataFrame(rank_data, index=[0], columns = rank_columns)
        major_rank_df = major_rank_df.append(minor_rank_df)
    
    bg_df = bg_df.merge(major_rank_df, on = ['Name', 'ID'])
    
    ### Category Function
    def cast_merge_by_class(grouping, fill_term, lst, df):
        all_terms_grouping = [getattr(i, grouping) for i in lst]
        unique_terms_grouping = list(set([i for j in all_terms_grouping for i in j]))
        grouping_term_columns = ['Name', 'ID'] + [fill_term + s for s in unique_terms_grouping]
        grouping_term_columns = [re.sub(' ', '_', x) for x in grouping_term_columns]
        
        major_grouping_df = pd.DataFrame(columns = grouping_term_columns)
        
        for game in lst:
            minor_grouping_df = pd.DataFrame(columns = grouping_term_columns, index=[0])
            minor_grouping_df = minor_grouping_df.fillna(False)
            minor_grouping_df['Name'] = game.name
            minor_grouping_df['ID'] = game.id
            for entry in getattr(game, grouping):
                term = fill_term + re.sub(' ', '_', entry)
                minor_grouping_df[term] = True
            
            major_grouping_df = major_grouping_df.append(minor_grouping_df)
        
        # global bg_df
        df_out = pd.merge(df, major_grouping_df, on = ['Name', 'ID'])
        return(df_out)
    
    merge_pairs = {'mechanics':'Mechanic_', 'categories':'Category_'}
    
    for key in merge_pairs.keys():
        bg_df = cast_merge_by_class(key, merge_pairs[key], all_games, bg_df)
    
    return(bg_df)

# if __name__ == "__main__":
#     all_games = pickle.load(open("./data/Raw/all_games_100.pkl", "rb"))
#     games_df = all_games_to_pd_DF(all_games)

#     games_database = Database('./data/boardgames_sql.db')
#     games_df.to_sql("games", games_database.connection, if_exists='replace')

#     print("--- SQL Query - Validation ---")
#     print(pd.read_sql_query("SELECT COUNT(*) Num_Games_in_DB FROM games;",
#                             games_database.connection))
#     games_database.connection.commit()
#     games_database.connection.close()
