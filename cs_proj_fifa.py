# Yihnew Eshetu
# yte9pc

from bs4 import BeautifulSoup
import requests
import pandas as pd


def connection():
    playersData = pd.DataFrame()
    for page in range(1,71):
        # Url address 
        url = 'https://www.futbin.com/20/players?page='+str(page)+'&sort=Player_Rating&order=desc&version=gold'

        # Retrieve data from url
        response = requests.get(url)
        # BeautifulSoup parser
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
         
        playersInfo = []
        for row in range(len(rows)):
            
            if row not in range (0, 2):
                cols = rows[row].find_all('td')
                playerInfo = []
                
                for col in range(0,len(cols)):
                    if col == 0:
                        playersName = cols[col].text.strip()
                        playerInfo.append(playersName)
                        playerClubCountryLeague = cols[col].find('span', {'class' : 'players_club_nation'})
                        NoneTypeCheck(playerClubCountryLeague, playerInfo, 'a', 0, 'data-original-title')
                        NoneTypeCheck(playerClubCountryLeague, playerInfo, 'a', 1, 'data-original-title')
                        NoneTypeCheck(playerClubCountryLeague, playerInfo, 'a', 2, 'data-original-title')
                    elif col == 7:
                        playerInfo.append(cols[col].text.replace('\\', '/'))
                    elif col == 14:
                        playerInfo.append(cols[col].text.strip().split('cm')[0])
                    elif col not in range(3,5) and col != 15:
                        playerInfo.append(cols[col].text.strip())
                playersInfo.append(playerInfo)
                
        playersData = playersData.append(playersInfo, ignore_index = True)
        
    playersData.columns =  ['Name', 'Club', 'Country', 'League', 'Overall Rating', 'Position',
                            'Skill' , 'Weak Foot', 'Work Rate', 'Pace', 'Shooting', 'Passing',
                            'Dribbling' , 'Defending', 'Physicality', 'Height', 'Base Stats',
                            'In Game Stats']
    playersData.to_csv('FIFA Player Info.csv')
        
        
def NoneTypeCheck(data, listname, item = None, iterator = None, get = None):
    if data is not None and get is not None:
        data = data.findAll(item)[iterator]
        data = data.get(get)
        listname.append(data)
    elif data is not None:
        listname.append(data.text)
        
        
#=====================================
# Block added by Travis Vitello / tjv9qh


import csv 


with open("./FIFA Player Info.csv",encoding="utf8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    Name = []
    Club = []
    Country = []
    League = []
    Overall_Rating = []
    Position = []
    Skill = []
    Weak_Foot = []
    Work_Rate = []
    Pace = []
    Shooting = []
    Passing = []
    Dribbling = []
    Defending = []
    Physicality = []
    Height = []
    Base_Stats = []
    In_Game_Stats = []
    
    for row in readCSV:
        Name_val  = row[1]
        Club_val = row[2]
        Country_val  = row[3]
        League_val  = row[4]
        Overall_Rating_val  = row[5]
        Position_val  = row[6]
        Skill_val  = row[7]
        Weak_Foot_val  = row[8]
        Work_Rate_val  = row[9]
        Pace_val  = row[10]
        Shooting_val = row[11]
        Passing_val = row[12]
        Dribbling_val = row[13]
        Defending_val = row[14]
        Physicality_val = row[15]
        Height_val = row[16]
        Base_Stats_val = row[17]
        In_Game_Stats_val = row[18]
        
        Name.append(Name_val)
        Club.append(Club_val)
        Country.append(Country_val)
        League.append(League_val)
        Overall_Rating.append(Overall_Rating_val)
        Position.append(Position_val)
        Skill.append(Skill_val)
        Weak_Foot.append(Weak_Foot_val)
        Work_Rate.append(Work_Rate_val)
        Pace.append(Pace_val)
        Shooting.append(Shooting_val)
        Passing.append(Passing_val)
        Dribbling.append(Dribbling_val)
        Defending.append(Defending_val)
        Physicality.append(Physicality_val)
        Height.append(Height_val)
        Base_Stats.append(Base_Stats_val)
        In_Game_Stats.append(In_Game_Stats_val)
            

   
if __name__ == '__main__':
    connection()