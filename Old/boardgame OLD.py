"""Boardgame class"""

class BoardGame(object):
    """Object containing information about a boardgame"""
    
    def __init__(self, data):
        self._data = data
    
    def __repr__(self):
        return("Boardgame(" + self.name + ")")
    
    def data(self):
        """Internal data dictionary"""
        return self._data
    
    @property
    def item(self):
        """Internal dictionary of 'item'"""
        print('teste')
        return self._data['items']['item']
        
    @property
    def statistics(self):
        """Internal dictionary of 'statistics'"""
        return self.item['statistics']
    
    @property
    def name(self):
        """object name"""
        try:
            return self.item['name'][0]['@value']
        except:
            return self.item['name']['@value']
            
    @property
    def id(self):
        """BGG ID"""
        return self.item['@id']
        
    @property
    def description(self):
        """Game description"""
        return self.item['description']
        
    @property
    def year_published(self):
        """Year of publication"""
        return int(self.item['yearpublished']['@value'])
        
    @property
    def min_players(self):
        """Minimum number of players, according to publisher"""
        return int(self.item['minplayers']['@value'])
        
    @property
    def max_players(self):
        """Maximum number of players, according to publisher"""
        return int(self.item['maxplayers']['@value'])
        
    @property
    def suggested_players(self):
        """BGG users suggested best player count"""
        poll = self.item['poll']
        poll_names = [ii['@name'] for ii in poll]
        poll = poll[poll_names.index('suggested_numplayers')]['results']
        
        best_player_cnt = {}
        def _get_best_num_players(index):
            numplay = poll[index]['@numplayers']
            best_votes = poll[index]['result'][0]['@numvotes']
            best_player_cnt[numplay] = int(best_votes)
        
        for x in range(len(poll)):
            _get_best_num_players(x) 
        max_votes = max(list(best_player_cnt.values()))
        
        suggested_players = [count for count, votes in best_player_cnt.items() if votes == max_votes][0]
                
        return suggested_players
    
    @property
    def min_age(self):
        """Publisher defined minimum age"""
        return int(self.item['minage']['@value'])
    
    @property
    def suggested_player_age(self):
        """BGG users suggested minimum age"""
        poll = self.item['poll']
        poll_names = [ii['@name'] for ii in poll]
        poll = poll[poll_names.index('suggested_playerage')]['results']['result']
        
        best_player_age = {}
        def _get_best_age_players(index):
            age = poll[index]['@value']
            num_votes = poll[index]['@numvotes']
            best_player_age[age] = int(num_votes)
        
        for x in range(len(poll)):
            _get_best_age_players(x)
        
        max_votes = max(list(best_player_age.values()))
        
        suggested_age = [count for count, votes in best_player_age.items() if votes == max_votes][0]
        
        return int(suggested_age)
    
    @property
    def language_dependence(self):
        """BGG users suggested language dependence"""
        poll = self.item['poll']
        poll_names = [ii['@name'] for ii in poll]
        poll = poll[poll_names.index('language_dependence')]['results']['result']
        
        voted_language_dependence = {}
        def _get_language_requirements(index):
            language_level = poll[index]['@value']
            num_votes = poll[index]['@numvotes']
            voted_language_dependence[language_level] = int(num_votes)
        
        for x in range(len(poll)):
            _get_language_requirements(x)
            
        max_votes = max(list(voted_language_dependence.values()))
        language_requirement = [count for count, votes in voted_language_dependence.items() if votes == max_votes][0]
        
        return language_requirement
        
    @property
    def playing_time(self):
        """BGG suggested playing time"""
        return int(self.item['playingtime']['@value'])
        
    @property
    def min_play_time(self):
        """Publisher defined minimum play time"""
        return int(self.item['minplaytime']['@value'])
        
    @property
    def max_play_time(self):
        """Publisher defined maximum play time"""
        return int(self.item['maxplaytime']['@value'])
        
    @property
    def categories(self):
        """List of game categories (i.e. theme)"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgamecategory']
        categories = [link[ii]['@value'] for ii in names_index]
        
        return categories
        
    @property
    def mechanics(self):
        """List of game categories (i.e. tile-laying, set collection)"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgamemechanic']
        mechanics = [link[ii]['@value'] for ii in names_index]
        
        return mechanics
        
    @property
    def game_family(self):
        """List of game families (i.e. Kickstarter, Made in Canda)"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgamefamily']
        family = [link[ii]['@value'] for ii in names_index]
        
        return family
        
    @property
    def implementations(self):
        """Does game implement another? (e.g. Pandemic: Legacy re-implements Pandemic)"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgameimplementation']
        implements = [link[ii]['@value'] for ii in names_index]
        
        return implements
        
    @property
    def designers(self):
        """List of game's designers"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgamedesigner']
        designers = [link[ii]['@value'] for ii in names_index]
        
        return designers
        
    @property
    def artists(self):
        """List of game's artists"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgameartist']
        artists = [link[ii]['@value'] for ii in names_index]
        
        return artists
        
    @property
    def publishers(self):
        """List of game's designers"""
        link = self.item['link']
        link_names = [ii['@type'] for ii in link]
        names_index = [i for i, x in enumerate(link_names) if x == 'boardgamepublisher']
        publishers = [link[ii]['@value'] for ii in names_index]
        
        return publishers
        
    @property
    def rank(self):
        """Dictionary of games various ranks (e.g. Overall, Strategy Games, Family, etc.)"""

        rankings = self.statistics['ratings']['ranks']['rank']
        
        num_rank_names = sum([i == '@name'for i in rankings])
        
        if num_rank_names == 1:
            if type(rankings) is int:
                ranks = {'boardgame':float(rankings['@value'])}
            else:
                ranks = {'boardgame': 0}
        else:
            rank_names = [ii['@name'] for ii in rankings]
            
            ranks = {}
            def _get_ranking(name):
                name_rank = rank_names.index(name)
                ranks[name] = int(rankings[name_rank]['@value'])
            
            for ii in rank_names:
                _get_ranking(ii)
        
        return ranks
    
    @property
    def ranks_bayes(self):
        """Dictionary of games various bayesian ranks (e.g. Overall, Strategy Games, Family, etc.)"""
        rankings = self.statistics['ratings']['ranks']['rank']
        num_rank_names = sum([i == '@name' for i in rankings])
        
        if num_rank_names == 1:
            ranks = {'boardgame':float(rankings['@bayesaverage'])}
        
        else:
            rank_names = [ii['@name'] for ii in rankings]
            
            ranks = {}
            def _get_bayes_ranking(name):
                name_rank = rank_names.index(name)
                ranks[name] = float(rankings[name_rank]['@bayesaverage'])
            
            for ii in rank_names:
                _get_bayes_ranking(ii)
        
        return ranks
    
    @property
    def users_rated(self):
        """Number of BGG users who've rated game"""
        return int(self.statistics['ratings']['usersrated']['@value'])
        
    @property
    def avg_rating(self):
        """Average BGG user rating (10-point scale)"""
        return float(self.statistics['ratings']['average']['@value'])
        
    @property
    def bayes_avg_rating(self):
        """Average BGG user's bayesian rating (10-point scale)"""
        return float(self.statistics['ratings']['bayesaverage']['@value'])
    
    @property
    def stdev_rating(self):
        """Standard deviation of BGG user rating (10-point scale)"""
        return float(self.statistics['ratings']['stddev']['@value'])
    
    @property
    def median_rating(self):
        """Median BGG user rating (10-point scale)"""
        return float(self.statistics['ratings']['median']['@value'])
        
    @property
    def num_owned(self):
        """Number of BGG users who own this game"""
        return  int(self.statistics['ratings']['owned']['@value'])
        
    @property
    def num_trading(self):
        """Number of copies being traded on BGG marketplace"""
        return int(self.statistics['ratings']['trading']['@value'])
        
    @property
    def num_wanting(self):
        """Number of BGG users who want to buy this game"""
        return int(self.statistics['ratings']['wanting']['@value'])
        
    @property
    def num_wishing(self):
        """Number of BGG users who wish they had this game"""
        return int(self.statistics['ratings']['wishing']['@value'])
        
    @property
    def num_comments(self):
        """Number of comments about the game"""
        return int(self.statistics['ratings']['numcomments']['@value'])
        
    @property
    def num_weights(self):
        """Number of BGG users who have assigned the game a weight (5-point scale)"""
        return int(self.statistics['ratings']['numweights']['@value'])
        
    @property
    def avg_weight(self):
        """Average weight assigned by BGG users (5-point scale)"""
        return float(self.statistics['ratings']['averageweight']['@value'])
