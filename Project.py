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
    return(pd.read_csv('FIFA Player Info.csv'))
        
        
def NoneTypeCheck(data, listname, item = None, iterator = None, get = None):
    if data is not None and get is not None:
        data = data.findAll(item)[iterator]
        data = data.get(get)
        listname.append(data)
    elif data is not None:
        listname.append(data.text)

   
if __name__ == '__main__':
    connection()