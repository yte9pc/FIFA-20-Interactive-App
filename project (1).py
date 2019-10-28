#!/usr/bin/env python
# coding: utf-8

# As a user, I want to know overall reating so that I can undertand current FIFA progress

# In[1]:


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

   
if __name__ == '__main__':
    connection()


# Start to do plots and analyze data

# In[2]:


sample=pd.read_csv('FIFA Player Info.csv')
df=sample


# In[3]:


import folium
import pycountry
df['Countryfullname'] = df['Country']
countries= df['Country'].unique().tolist()
print(countries)


# In[4]:


import pycountry

input_countries = df['Country']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]


# In[5]:


df['Country'] = codes
df.head(5)


# In[6]:


country_geo = 'world-countries.json'


# In[7]:


stage = df
data_to_plot = stage[['Country','Overall Rating']]


# In[8]:


import seaborn as sns, numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt 
plt.rcParams["figure.figsize"] = (12,5)
sns.pairplot(df);


# In[9]:


stage = df
data_to_plot = stage[['Country','Overall Rating']]


# In[10]:


hist_indicator =  'Overall Rating'


# In[11]:


data_to_plot.head()


# In[12]:


import os
os.getcwd()


# In[13]:


import json-
country_geo = json.load(open("world-countries.json")) 
#country_geo = 'world-countries.json'
map = folium.Map(location=[100, 0], zoom_start=1.5)
map.choropleth(geo_data=country_geo, data=data_to_plot,
             columns=['Country', 'Overall Rating'],
             key_on='feature.id',
             fill_color='YlOrRd', fill_opacity=0.5, line_opacity=0.2,
             legend_name=hist_indicator)


# In[14]:


# Create Folium plot
map.save('plot_data.html')


# In[15]:


# Create Folium plot
map.save('plot_data.html')
# Import the Folium interactive html file
from IPython.display import HTML
HTML('<iframe src=plot_data.html width=700 height=450></iframe>')


# In[16]:


df1=df
stage = df1
data_to_plot = stage[['Country','Skill']]


# In[17]:


hist_indicator =  'Skill'


# In[18]:


data_to_plot.head()


# In[19]:


import json
country_geo = json.load(open("world-countries.json")) 
#country_geo = 'world-countries.json'
map = folium.Map(location=[100, 0], zoom_start=1.5)
map.choropleth(geo_data=country_geo, data=data_to_plot,
             columns=['Country', 'Skill'],
             key_on='feature.id',
             fill_color='YlOrRd', fill_opacity=0.5, line_opacity=0.2,
             legend_name=hist_indicator)


# In[20]:


# Create Folium plot
map.save('plot_data1.html')
# Import the Folium interactive html file
from IPython.display import HTML
HTML('<iframe src=plot_data1.html width=700 height=450></iframe>')


# In[21]:


df= sns.PairGrid(sample)
df.map_diag(sns.kdeplot)
df.map_offdiag(sns.kdeplot, n_levels=6);


# In[51]:


import seaborn as sns; 
# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Physicality', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[52]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Dribbling', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[53]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Defending', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[54]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Height', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[55]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Skill', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[56]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Base Stats', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[57]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='In Game Stats', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[58]:


plt.figure(figsize=(15,6))
sns.countplot(x="Overall Rating",data=sample)  


# In[59]:


df = sns.jointplot(x="Overall Rating", y="Physicality", data=sample, kind="kde", color="m")
df.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
df.ax_joint.collections[0].set_alpha(0)
df.set_axis_labels("Overall Rating", "Physically");


# In[60]:


df = sns.jointplot(x="Overall Rating", y="Shooting", data=sample, kind="kde", color="m")
df.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
df.ax_joint.collections[0].set_alpha(0)
df.set_axis_labels("Overall Rating", "Shooting");


# In[61]:


# Generate sequential data and plot
plt.figure(figsize=(15,6))
sd = sample.sort_values('Overall Rating', ascending=False)[:8]
x1 = np.array(list(sd['Name']))
y1 = np.array(list(sd['Overall Rating']))
sns.barplot(x1, y1, palette= "colorblind")
plt.ylabel("Overall Rating")


# In[62]:


# Generate sequential data and plot
plt.figure(figsize=(15,6))
sd = sample.sort_values('Overall Rating', ascending=False)[:10]
x1 = np.array(list(sd['Country']))
y1 = np.array(list(sd['Overall Rating']))
sns.barplot(x1, y1, palette= "colorblind")
plt.ylabel("Overall Rating")


# In[63]:


# Generate sequential data and plot
plt.figure(figsize=(15,6))
sd = sample.sort_values('Overall Rating', ascending=False)[:10]
x1 = np.array(list(sd['Countryfullname']))
y1 = np.array(list(sd['Overall Rating']))
sns.barplot(x1, y1, palette= "colorblind")
plt.ylabel("Overall Rating")


# In[64]:


f_fuko = sample.loc[sample['Position']=='RW']['Overall Rating']
m_fuko = sample.loc[sample['Position']=='ST']['Overall Rating']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='RW')
sns.distplot(m_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='ST')
plt.legend()


# In[65]:


g = sns.pairplot(sample, hue="Position")


# In[66]:


x = sample['Overall Rating']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()


# In[84]:


from matplotlib.pyplot import figure
figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
ax = sns.scatterplot(x="Shooting", y='Overall Rating',  size="Position", data=sample)
sns.regplot(x="Shooting", y="Overall Rating", data=sample)


# In[71]:


g = sns.pairplot(sample, vars=["Overall Rating", "Skill"], hue="Position")


# In[76]:


g = sns.pairplot(sample, vars=["Overall Rating", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality" ])


# In[80]:


g = sns.pairplot(sample, vars=["Overall Rating", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"], hue="Position")


# In[81]:


g = sns.pairplot(sample, vars=["Overall Rating", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"], hue="Position")


# In[82]:


g = sns.pairplot(sample, vars=["Overall Rating", "Height", "Base Stats", "In Game Stats"], hue="Position")


# In[ ]:




