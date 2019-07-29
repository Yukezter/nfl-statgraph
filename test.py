 # list1 = []

# for qb in qbs_svn_seasons_or_more:
#     # szn1 = qb.get_data_by_player_season('Passing Stats', 'RAT', 1)
#     szn2 = qb.get_data_by_player_season('Passing Stats', 'RAT', 2)
#     szn3 = qb.get_data_by_player_season('Passing Stats', 'RAT', 3)
#     pct_increase = get_pct_increase(szn2, szn3)
#     print(pct_increase, qb.name, qb.team.team)
#     list1.append(pct_increase)

# avg1 = sum(list1)/len(list1)

# print(avg1)


# qbs_by_rat = sorted(qbs_svn_seasons_or_more, key=lambda x: x.get_data_by_player_season('Passing Stats', 'RAT', 2), reverse=True)