def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_pct_increase(a, b):
    try:
        pct_increase = ((b - a)/a)*100
    except:
        pct_increase = 0
    return pct_increase

def write_to_text_file(teams):
    f_path = r'C:\\Users\Bryan\Documents\\Python-Scripts\\random\\teams\\'
    for team in teams:
        team_file = f_path + str(team.team).replace(' ', '-').lower() + '.txt'
        with open(team_file, 'a') as f:
            f.write('--------------------TEAM--------------------')
            f.write(str(team))
            for player in team.roster:
                f.write('\n')
                f.write('----------PLAYER----------')
                f.write(str(player))