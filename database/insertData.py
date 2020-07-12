import sqlite3
import pandas as pd
import random

fifa = pd.read_csv('FIFA Player Info.csv', keep_default_na = False).drop(columns = 'Unnamed: 0')

country = fifa[['Country', 'Continent']].sort_values('Country').drop_duplicates().reset_index(drop=True)
clubs = fifa[['Club', 'League', 'League Country']].sort_values('Club').drop_duplicates().reset_index(drop=True)
players = fifa[['Name', 'Club', 'Country', 'Position', 'Overall Rating', 'Skill', 'Weak Foot', 'Work Rate', 'Pace',
       'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality',
       'Height']].drop_duplicates().reset_index(drop=True)
positions = fifa[['Position','Position Group']].sort_values('Position Group').drop_duplicates().reset_index(drop=True)

positions['Description'] = ['Right Winger', 'Striker', 'Left Winger', 'Centre Forward', 'Right Forward',
                                 'Left Forward', 'Left Wing Back', 'Right Back', 'Centre Back', 'Left Back',
                                  'Right Wing Back', 'Goal Keeper', 'Right Midfielder', 'Centre Midfielder', 
                                 'Left Midfielder', 'Centre Defensive Midfielder', 'Centre Attacking Midfielder']

# Create a connection to the database.
conn = sqlite3.connect('fifa.db')

# Create a cursor. 
cursor = conn.cursor()

# Country
countrysql = '''INSERT INTO country 
         (country_name, continent) 
         values 
         (:country_name, :continent)'''

for index, row in country.iterrows():
    cursor.execute(countrysql, {'country_name':row['Country'], 'continent':row['Continent']})

# Clubs
clubssql = '''INSERT INTO club
         values 
         (:club_name, :league_name)'''

# Club Country
clubcountryssql = '''INSERT INTO club_country 
         values 
         (:club_name, :country_name)'''

for index, row in clubs.iterrows():
    cursor.execute(clubssql, {'club_name':row['Club'], 'league_name':row['League']})

    cursor.execute(clubcountryssql, {'club_name':row['Club'], 'country_name':row['League Country']})

# Positions
positionssql = '''INSERT INTO position
         values 
         (:position, :description, :position_group)'''

for index, row in positions.iterrows():
    cursor.execute(positionssql, {'position':row['Position'], 'description':row['Description'], 
                                  'position_group':row['Position Group']})    
    
# Players
playerssql = '''INSERT INTO player 
         values 
         (:player_id, :player_name, :country_name)'''

# Stats
statssql = '''INSERT INTO stat 
         values 
         (:player_id, :overall_rating, :skill, :weak_foot, :work_rate, :pace, 
         :shooting, :passing, :dribbling, :defending, :physicality, :height)'''

# Player Club
playerclub = '''INSERT INTO player_club 
         values 
         (:player_id, :club_name, :salary, :contract_length)'''

# Player Position
playerpositionsql = '''INSERT INTO player_position
                values
                (:player_id, :position)'''


for index, row in players.iterrows():
    cursor.execute(playerssql, {'player_id':index + 1, 'player_name':row['Name'],  
                                'country_name':row['Country']})

    cursor.execute(statssql, {'player_id':index + 1, 'overall_rating':row['Overall Rating'],
                              'skill':row['Skill'], 'weak_foot':row['Weak Foot'],
                              'work_rate':row['Work Rate'], 'pace':row['Pace'],
                              'shooting':row['Shooting'], 'passing':row['Passing'], 
                              'dribbling':row['Dribbling'], 'defending':row['Defending'], 
                              'physicality':row['Physicality'], 'height':row['Height']
                             })
    
    fakesalary = round((30000000)*(1 - 1*(index/len(players))), 2)
    cursor.execute(playerclub, {'player_id':index + 1, 'club_name':row['Club'],
                                'salary':fakesalary, 
                                'contract_length':round(random.uniform(1,5), 1)})
    
    cursor.execute(playerpositionsql, {'player_id':index + 1, 'position':row['Position']})

    conn.commit()
cursor.close()