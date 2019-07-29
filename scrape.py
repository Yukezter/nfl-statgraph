import bs4 as bs
import requests
import string
import time
import re
import pickle

from models import Team, Player
from models import is_number

def scrape():
    teams = {}

    teams_logos = []
    teams_links = []
    teams_stats = []
    divisions = []

    # team standings page
    req = requests.get('http://www.espn.com/nfl/standings').text
    soup = bs.BeautifulSoup(req, 'html.parser')

    # useful dom objects
    standings = soup.find('div', {'class': 'tabs__content'})
    conferences = standings.find('section').find('section').next_sibling.contents

    for i in range(2):
        # get group of teams for that conference
        conference_data = conferences[i].find('section', {'class': 'standings-subgroups'}).find('table')
        teams_col = conference_data.find('tr').contents[0]
        data_col = conference_data.find('tr').contents[1]
        conference = conference_data.parent.previous_sibling.text

        # get team logo, links, and stats

        # can't loop through logos/links and team stats
        # within same loop cause it's broken into two columns.
        # used two separate loops
        teams_row = teams_col.find('table').find_all('tr')
        for team in teams_row:
            if 'subgroup-headers' in team['class']:
                division = team.text
                divisions.extend((division, division, division, division))
            else:
                logo_and_name = team.find_all('a')

                team_logo = logo_and_name[0].find('img')['src']
                team_link = logo_and_name[2]['href']

                teams_logos.append(team_logo)
                teams_links.append(team_link)

        # now loop through data table
        data_rows = data_col.find('table').find('table').find('tbody').find_all('tr')
        col_headers = data_rows[0].find_all('td')
        stat_headers = [col.text for col in col_headers]
        # stat_headers = [col.find('span')['title'] for col in col_headers]
        for data_row in data_rows:
            if 'subgroup-headers' not in data_row['class']:
                data = [float(d.text) if is_number(d.text) else d.text for d in data_row.find_all('td')]
                teams_stats.append(data)

    team_stats = []

    for stats in teams_stats:
        add_headers = [stat_headers, stats]
        team_stats.append(add_headers)

    # loop through teams links
    for i, team_link in enumerate(teams_links):
        team = team_link.rsplit('/')[-1].replace('-', ' ').title()

        # initialize roster in order to create Team object before Player
        roster = {}

        # convert link to roster
        index = team_link.find('_')
        player_roster_url = 'http://www.espn.com' + team_link[:index] + 'roster/' + team_link[index:]

        req = requests.get(player_roster_url).text
        soup = bs.BeautifulSoup(req, 'html.parser')

        # find roster content
        roster_sections = soup.find_all('tbody', {'class': 'Table2__tbody'})

        player_page_links = []

        for section in roster_sections:
            player_name_anchors = section.find_all('a')
            for anchor in player_name_anchors:
                player_page_links.append(anchor['href'])



        # Team instance
        team_object = Team(team, conference, divisions[i], roster, team_stats[i], teams_logos[i])

        # loop through player links
        for player_link in player_page_links:
            # add stats to url
            i = player_link.find('_')
            player_stats_url = player_link[:i] + 'stats/' + player_link[i:]

            req = requests.get(player_stats_url).text
            soup = bs.BeautifulSoup(req, 'html.parser')

            print(player_link)

            # set useful dom objects
            player_content = soup.find('div', {'class': 'mod-content'})
            player_bio = soup.find('div', {'class': 'player-bio'})
            general_info = player_bio.find('ul', {'class': 'general-info'})

            # player info

            # some players might not have headshot image
            try:
                headshot_img = soup.find('div', {'class': 'main-headshot'}).find('img')['src']
            except:
                headshot_img = None

            name = player_content.find('h1').text
            number, position = general_info.contents[0].text.split()
            height, weight = general_info.contents[1].text.split(', ')
            team = general_info.contents[2].text

            born_string = player_bio.find('span', text='Born').next_sibling
            age_re = re.compile(r' \(Age: ([0-9]{2})\)$')
            age = int(age_re.search(born_string).group(1))

            # check if born date AND city of birth are given
            if 'in' in born_string:
                born_on, born_in = born_string.strip().split(' in ')
                born_in = re.sub(r' \(Age: [0-9]{2}\)$', '', born_in)
            else:
                born_on, born_in = born_string.replace('Born', ''), 'N/A'
                born_on = re.sub(r' \(Age: [0-9]{2}\)$', '', born_on)
            
            # some players might not have 'drafted'
            try:
                drafted = player_bio.find('span', text='Drafted').next_sibling.strip()
            except:
                drafted = 'N/A'
            
             # some players might not have 'experience'
            try:
                experience = player_bio.find('span', text='Experience').next_sibling.strip()
            except:
                experience = 'N/A'

            college = player_bio.find('span', text='College').next_sibling.strip()

            # player stats
            stats_tables = soup.find('div', {'class': 'mod-player-stats'}).find_all('div', {'class': 'mod-player-stats'})

            player_stats = {}

            for table in stats_tables:
                
                # just in case there is more than one stat header
                # this workaround is really ugly
                headers = table.find('tr', {'class': 'stathead'}).contents
                if len(headers) > 2:
                    data_table_punts = []
                    data_table_kickoffs = []

                    header_punts = headers[1].text.strip()
                    header_kickoffs = headers[2].text.strip()

                    # column headers for data table (first row of the 2D array)
                    col_headers_html = table.find('tr', {'class': 'colhead'}).contents
                    col_headers_row = [col.text.title() for col in col_headers_html[:2]] + [col.text.strip('\t') for col in col_headers_html[2:8]]
                    # col_headers = [col.text.title() for col in col_headers_html[:2]] + [col['title'] for col in col_headers_html[2:]]

                    data_table_punts.append(col_headers_row)
                    data_table_kickoffs.append(col_headers_row)

                    stat_rows = table.find_all('tr', {'class': re.compile('oddrow|evenrow')})

                    for row in stat_rows:
                        contents = row.contents
                        row_data_punts = [int(contents[0].text), contents[1].text] + [float(col.text.replace(',', '')) 
                                                                                        if is_number(col.text.replace(',', '')) 
                                                                                        else col.text for col 
                                                                                        in contents[2:8]]
                        row_data_kickoffs = [int(contents[0].text), contents[1].text, float(contents[2].text)] + [float(col.text.replace(',', '')) 
                                                                                                                if is_number(col.text.replace(',', '')) 
                                                                                                                else col.text for col 
                                                                                                                in contents[8:]]
                        data_table_punts.append(row_data_punts)
                        data_table_kickoffs.append(row_data_kickoffs)

                    total_row = table.find('tr', {'class': 'total'}).contents
                    career_total_punts = [total_row[0].text, ''] + [float(total.text.replace(',', '')) 
                                                                    if is_number(total.text.replace(',', '')) 
                                                                    else total.text for total 
                                                                    in total_row[1:7]]
                    career_total_kickoffs = [total_row[0].text, '', float(total_row[1].text)] + [float(total.text.replace(',', '')) 
                                                                                                if is_number(total.text.replace(',', '')) 
                                                                                                else total.text for total 
                                                                                                in total_row[7:]]

                    data_table_punts.append(career_total_punts)
                    data_table_kickoffs.append(career_total_kickoffs)

                    player_stats[header_punts] = data_table_punts
                    player_stats[header_kickoffs] = data_table_kickoffs

                else:
                    stat_header = table.find('tr', {'class': 'stathead'}).text.strip()

                    data_table = []

                    # column headers for data table (first row of the 2D array)
                    col_headers_html = table.find('tr', {'class': 'colhead'}).contents
                    col_headers_row = [col.text.title() for col in col_headers_html[:2]] + [col.text.strip('\t') for col in col_headers_html[2:]]
                    # col_headers = [col.text.title() for col in col_headers_html[:2]] + [col['title'] for col in col_headers_html[2:]]
                    data_table.append(col_headers_row)

                    rows = table.find_all('tr', {'class': re.compile('oddrow|evenrow')})
                    for row in rows:
                        contents = row.contents
                        row_data = [int(contents[0].text), contents[1].text] + [float(col.text.replace(',', '')) 
                                                                                if is_number(col.text.replace(',', '')) 
                                                                                else col.text for col 
                                                                                in contents[2:]]
                        data_table.append(row_data)

                    total_row = table.find('tr', {'class': 'total'})
                    career_total = [float(total.text.replace(',', '')) 
                                    if is_number(total.text.replace(',', '')) 
                                    else total.text for total 
                                    in total_row.find_all('td')]
                    # insert empty string in 2nd column for the total row
                    career_total.insert(1, '')
                    data_table.append(career_total)

                    player_stats[stat_header] = data_table
                
            # instantiate Player and append to Team.roster
            roster[name] = Player(name, height, weight, college, age, born_on, born_in, 
            team_object, position, number, experience, drafted, player_stats, headshot_img)
        
        team_object.roster = roster
        teams[team_object.team] = team_object

        time.sleep(1)

    return teams