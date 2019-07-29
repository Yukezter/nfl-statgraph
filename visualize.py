import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import chain
import time
import datetime

from decorators import timer
from utilities import is_number, get_pct_increase, write_to_text_file
from scrape import scrape
from models import (Team, Player, print_teams, get_all_players, 
filter_players_by_position, filter_players_by_experience)

if __name__ == '__main__':
    try:
        pickle_in = open('teams.pickle', 'rb')
        teams = pickle.load(pickle_in)
        # write_to_text_file(teams)
    except:
        teams = scrape()
        pickle_out = open('teams.pickle', 'wb')
        pickle.dump(teams, pickle_out)
        pickle_out.close()

    players = []
    for team in teams:
        for player in team.roster:
            players.append(player)
            print(player)

    # matplotlib custom font sizes
    SMALL_SIZE = 10
    MEDIUM_SIZE = 12
    BIGGER_SIZE = 14

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the x tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)   # fontsize of the y tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    
    # offense
    qbs = filter_players_by_position(players, 'QB')
    # rbs = filter_players_by_position(players, 'RB')
    # wrs = filter_players_by_position(players, 'WR')
    # tes = filter_players_by_position(players, 'TE')
    # cs = filter_players_by_position(players, 'C')
    # gs = filter_players_by_position(players, 'G')
    # ots = filter_players_by_position(players, 'OT')
    # # defense
    # des = filter_players_by_position(players, 'DE')
    # dts = filter_players_by_position(players, 'DT')
    # lbs = filter_players_by_position(players, 'LB')
    # cbs = filter_players_by_position(players, 'CB')
    # ss = filter_players_by_position(players, 'S')
    # # special teams
    # pks = filter_players_by_position(players, 'PK')
    # ps = filter_players_by_position(players, 'P')
    # lss = filter_players_by_position(players, 'LS')

    @timer
    def plot_top_players(players, stat_type, headers):
        ordered_lists = []
        for header in headers:
            ordered_lists.append(sorted(players, key=lambda x: x.get_stat_by_season(stat_type, header, 0), reverse=True)[:15])

        plots = []
        for i, l in enumerate(ordered_lists):
            names, data = [], []
            for qb in l:
                names.append(qb.name)
                data.append(qb.get_stat_by_season(stat_type, headers[i], 0))
            plots.append((names, data))

        for i, plot in enumerate(plots):
            plt.figure(num=i+1, figsize=(14, 8))
            plt.bar(plot[0], plot[1])
            plt.title('Top ' + players[0].position + ' based on career ' + headers[i], size=BIGGER_SIZE)

            plt.xlabel('Names')
            plt.ylabel(headers[i])
            
            plt.xticks(rotation=18)
    
    qb_headers = ['ATT', 'YDS', 'AVG', 'LNG', 'TD', 'RAT']
    plot_top_players(qbs, 'Passing Stats', qb_headers)

    # rb_headers = ['ATT', 'YDS', 'AVG', 'LNG', 'TD', 'FD']
    # plot_top_players(rbs, 'Rushing Stats', rb_headers)

    # wr_headers = ['REC', 'YDS', 'AVG', 'LNG', 'TD', 'FD']
    # plot_top_players(wrs, 'Receiving Stats', wr_headers)

    plt.show()
    
    