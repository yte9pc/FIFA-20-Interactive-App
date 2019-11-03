# Yihnew Eshetu
# yte9pc

from bs4 import BeautifulSoup
import requests
import pandas as pd
import pycountry
import pycountry_convert


def connection():
   playersData = pd.DataFrame()
   for page in range(1,560):
       # Url address 
       print(page)
       if page < 71:
           url = 'https://www.futbin.com/20/players?page='+str(page)+'&sort=Player_Rating&order=desc&version=gold'
       elif page >= 71 and page < 352:
           url = 'https://www.futbin.com/20/players?page='+str(page-70)+'&sort=Player_Rating&order=desc&version=silver'
       else:
            url = 'https://www.futbin.com/20/players?page='+str(page-351)+'&sort=Player_Rating&order=desc&version=bronze'
            
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
   
   playersData.insert(6, "Position Group", playersData['Position'].apply(position), True)
   playersData.insert(4, "Continent", playersData['Country'].apply(continent) , True)
   playersData.drop_duplicates(subset = ['Name', 'Overall Rating', 'Position'], keep = 'last', inplace = True) 
    
   playersData.to_csv('FIFA Player Info.csv')
   return(pd.read_csv('FIFA Player Info.csv'))
        
def NoneTypeCheck(data, listname, item = None, iterator = None, get = None):
    if data is not None and get is not None:
        data = data.findAll(item)[iterator]
        data = data.get(get)
        listname.append(data)
    elif data is not None:
        listname.append(data.text)

def position(DFColumn):
    positions = {
            'Attacker' : ['CF', 'ST', 'RW', 'RF', 'LW', 'LF'], 
            'Midfieder' : ['RM', 'LM', 'CAM', 'CM', 'CDM'],
            'Defender' : ['LB', 'LWB', 'RB', 'RWB', 'CB'],
            'Goal Keeper' : ['GK']}
    for position in positions.keys():
        if DFColumn in positions.get(position):
            return(position)
        
def continent(DFColumn):
  countries = {}
  for country in pycountry.countries:
    countries[country.name] = country.alpha_2

  if countries.get(DFColumn) is not None:
      return(pycountry_convert.country_alpha2_to_continent_code(countries.get(DFColumn)))
  elif DFColumn == 'Korea Republic':
      return(pycountry_convert.country_alpha2_to_continent_code('KR'))
  elif DFColumn == 'Korea DPR':
      return(pycountry_convert.country_alpha2_to_continent_code('KP'))
  elif DFColumn == 'Congo DR':
      return(pycountry_convert.country_alpha2_to_continent_code('CD'))
  elif DFColumn == 'Cape Verde Islands':
      return(pycountry_convert.country_alpha2_to_continent_code('CV'))
  elif DFColumn == 'China PR':
      return(pycountry_convert.country_alpha2_to_continent_code('CN'))
  elif DFColumn == 'Republic of Ireland':
      return(pycountry_convert.country_alpha2_to_continent_code('IE'))
  elif DFColumn == 'FYR Macedonia':
      return(pycountry_convert.country_alpha2_to_continent_code('MK'))
  elif DFColumn == 'St. Kitts and Nevis':
      return(pycountry_convert.country_alpha2_to_continent_code('KN'))
  elif DFColumn == 'São Tomé e Príncipe':
      return(pycountry_convert.country_alpha2_to_continent_code('ST'))
  elif DFColumn == 'Chinese Taipei':
      return(pycountry_convert.country_alpha2_to_continent_code('TW'))
  elif DFColumn == 'St. Lucia':
      return(pycountry_convert.country_alpha2_to_continent_code('LC'))
  else:
      return(pycountry_convert.country_alpha2_to_continent_code(pycountry.countries.search_fuzzy(DFColumn)[0].alpha_2))
                   
if __name__ == '__main__':
    DF = connection()
