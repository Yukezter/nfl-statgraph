from itertools import chain
from datetime import datetime

from utilities import is_number, get_pct_increase

class Team:
    def __init__(self, team, conference, division, roster, stats, logo):
        self.team = team
        self.conference = conference
        self.division = division
        self.roster = roster
        self.stats = stats
        self.logo = logo

    def __repr__(self):
        roster_list = [name for name in self.roster]
        stats_table = ('\n'.join([''.join(['{:8}'.format(str(item)) for item in row]) for row in self.stats]))
        output_team = ('\n'
                        'Team: {}\n'
                        'Conference: {}\n'
                        'Division: {}\n'
                        'Roster: {}\n'
                        'Stats: \n{}\n'
                        'Logo: {}\n'.format(self.team, self.conference, 
                        self.division, roster_list, stats_table, self.logo))
        return output_team
            

class Player(Team):
    def __init__(self, name, height, weight, college, age, born_on, 
    born_in, team, position, number,  experience, drafted, stats, headshot):

        self.name = name
        self.height = height
        self.weight = weight
        self.college = college
        self.age = age
        self.born_on = born_on
        self.born_in = born_in
        self.team = team
        self.position = position
        self.number = number
        self.experience = experience
        self.drafted = drafted
        self.stats = stats
        self.headshot = headshot

    def __repr__(self):
        stats_tables = ''
        for header, stat in self.stats.items():
                    stats_tables += (header.upper() + '\n')
                    stats_tables += ('\n'.join([''.join(['{:10}'.format(str(item)) for item in row]) for row in stat]))
                    stats_tables += ('\n\n')
        
        output_player = ('\n'
                        'Name: {}\n'
                        'Height: {}\n'
                        'Weight: {}\n'
                        'College: {}\n'
                        'Age: {}\n'
                        'DOB: {}\n'
                        'Born in: {}\n'
                        'Team: {}\n'
                        'Position: {}\n'
                        'Number: {}\n'
                        'Experience: {}\n'
                        'Drafted: {}\n'
                        'Stats: \n\n{}'
                        'Headshot: {}\n'.format(self.name, self.height, 
                        self.weight, self.college, self.age, self.born_on, 
                        self.born_in, self.team.team, self.position, self.number, 
                        self.experience, self.drafted, stats_tables, self.headshot))
        
        return output_player

    def get_stat_by_year(self, stat_table, stat_header, year):
        for k, v in self.stats.keys():
            if k.replace(u'\xa0', u'') == stat_table and year <= datetime.year:
                column_headers = v[0]
                if stat_header in column_headers:
                    i = column_headers.index(stat_header)
                    for row in self.stats[stat_table]:
                        if row[0] == year:
                            rv = row[i]
                            if is_number(rv):
                                return rv
        return 0

    
    def get_stat_by_season(self, stat_table, stat_header, season):
        for k,v in self.stats.items():
            if k.replace(u'\xa0', u'') == stat_table:
                table = v
                if len(table) - 2 >= season:
                    column_headers = table[0]
                    if stat_header in column_headers:
                        i = column_headers.index(stat_header)
                        if season == 0:
                            rv = table[-1][i]
                            if is_number(rv):
                                return rv
                        else:
                            rv = table[season][i]
                            if is_number(rv):
                                return rv
        return 0
    
    def get_stat_pct_increase(self, stat_header, stat, season):
        prior_season =  self.get_stat_by_season(stat_header, stat, season-1)
        this_season =  self.get_stat_by_season(stat_header, stat, season)
        return get_pct_increase(prior_season, this_season)
        
def print_teams(teams):
    for team in teams:
        print('--------------------TEAM--------------------')
        print(str(team))
        for player in team.roster:
            print('\n')
            print('----------PLAYER----------')
            print(str(player))

def get_all_players(teams):
    players = []
    for team in teams:
        team_players = []
        for player in team.roster:
            team_players.append(player)
        players.append(team_players) 
    players = list(chain.from_iterable(players))
    return players

def filter_players_by_position(players, position):
    filtered_players = []
    for player in players:
            if player.position == position:
                filtered_players.append(player)
    return filtered_players

def filter_players_by_experience(players, years_of_exp):
    filtered_players = []
    for player in players:
        # parse 'experience' attribute value
        nth_season = player.experience.split()[0]
        # check if number is single or double digits
        if is_number(nth_season[:2]):
            exp = int(nth_season[:2])
        else:
            if is_number(nth_season[0]):
                exp = int(nth_season[0])
            else:
                # rookie
                exp = 0
        if exp >= years_of_exp:
            filtered_players.append(player)
    return filtered_players