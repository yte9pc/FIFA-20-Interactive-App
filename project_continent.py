#!/usr/bin/env python
# coding: utf-8

# As a user, I want to know overall reating so that I can undertand current FIFA progress

# In[123]:


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

# In[124]:


sample=pd.read_csv('FIFA Player Info.csv')
df=sample


# In[125]:


#convert country names which are recongized by python
df['Country'] = pd.np.where(df['Country'] == "Holland", "Netherlands", df['Country'])
df['Country'] = pd.np.where(df['Country'] == "England", "United Kingdom", df['Country'])


# In[126]:


#import modules for convert contry name to contry codes
import folium
import pycountry
df['Countryfullname'] = df['Country']
df['Countryfullname_cont'] = df['Country']
countries= df['Country'].unique().tolist()
print(countries)


# In[127]:


#convert country to country code to three digits
import pycountry

input_countries = df['Country']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]


# In[128]:


#convert country to country code to two digits then continent
import pycountry
import pycountry_convert as pc
input_countries = df['Countryfullname_cont']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2

codes_cont = [countries.get(country, 'Unknown code') for country in input_countries]


# In[129]:


df['Country'] = codes
df.head(5)


# In[130]:


import pycountry_convert as pc
df['Countryfullname_cont1'] = codes_cont
df.head(5)


# In[131]:


df.drop(df.loc[df['Countryfullname_cont1']=='Unknown code'].index, inplace=True)


# In[132]:


#Convery contry code to continent
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
cont1s=df['Countryfullname_cont1'].tolist()
change_cont1s = []
for cont1 in cont1s:
    continent_name = country_alpha2_to_continent_code(cont1)
    change_cont1s.append(continent_name)
df['Countryfullname_cont']=change_cont1s
df.tail(10)


# In[158]:


# >>> import seaborn as sns
# >>> sns.set(style="whitegrid")
# >>> tips = sns.load_dataset("tips")
# >>> ax = sns.barplot(x="day", y="total_bill", data=tips)


# In[157]:


import seaborn as sns
ax = sns.barplot(x="Overall Rating", y="Countryfullname_cont", data=sample)


# continents, NA = "North America", SA = "South Amierica", AS = "Asia", OC = "Australia", AF = "Africa"

# In[135]:


# Sort players based on their countries
plt.figure(figsize=(15,6))
sns.countplot(x="Countryfullname_cont", data=sample)


# In[136]:


df2=df.head(100)
df.describe()


# In[137]:


#As a user, I want to know players from which continents
df.groupby('Countryfullname_cont')['Name'].count()


# In[138]:


df.groupby('Countryfullname')['Name'].count()


# In[139]:


#As a user, I want to know player from which countries
#df.groupby('Countryfullname')['Name'].count()
df.groupby('Name', as_index=False).agg({"Countryfullname_cont": "sum"})


# In[140]:


# grouped = df.groupby('Countryfullname_cont').agg("Overall Rating": [min, max, mean]) 
# # Using ravel, and a string join, we can create better names for the columns:
# grouped.columns = ["_".join(x) for x in grouped.columns.ravel()]
df.groupby('Countryfullname_cont', as_index=False).agg({"Overall Rating": "sum"})


# In[141]:


df.groupby('Countryfullname', as_index=False).agg({"Overall Rating": "sum"})


# In[142]:


grouped_continent = df.groupby('Countryfullname_cont').agg({'Overall Rating': ['mean', 'min', 'max']})
print(grouped_continent)


# In[143]:


grouped_continent = df.groupby('Countryfullname').agg({'Overall Rating': ['mean', 'min', 'max']})
print(grouped_continent)


# In[144]:


df[df['Position'] == 'LW'].groupby('Countryfullname_cont').agg(
    # Get max of the duration column for each group
    max_Overall_Rating=('Overall Rating', max),
    # Get min of the duration column for each group
    min_Overall_Rating=('Overall Rating', min),
    # Get sum of the duration column for each group
    sum_Overall_Rating=('Overall Rating', sum),
    # Apply a lambda to date column
    #num_days=("date", lambda x: (max(x) - min(x)).days)    
)


# In[159]:


df.groupby('Countryfullname_cont')[['Overall Rating']].mean()


# In[160]:


country_geo = 'world-countries.json'


# In[161]:


stage = df
data_to_plot = stage[['Country','Overall Rating']]


# In[162]:


stage = df
data_to_plot = stage[['Country','Overall Rating']]


# In[163]:


hist_indicator =  'Overall Rating'


# In[164]:


data_to_plot.head()


# In[165]:


import os
os.getcwd()


# In[166]:


import json
country_geo = json.load(open("world-countries.json")) 
#country_geo = 'world-countries.json'
map = folium.Map(location=[100, 0], zoom_start=1.5)
map.choropleth(geo_data=country_geo, data=data_to_plot,
             columns=['Country', 'Overall Rating'],
             key_on='feature.id',
             fill_color='YlOrRd', fill_opacity=0.5, line_opacity=0.2,
             legend_name=hist_indicator)


# In[167]:


# Create Folium plot
map.save('plot_data.html')


# In[168]:


# Create Folium plot
map.save('plot_data.html')
# Import the Folium interactive html file
from IPython.display import HTML
HTML('<iframe src=plot_data.html width=700 height=450></iframe>')


# In[169]:


df1=df
stage = df1
data_to_plot = stage[['Country','Skill']]


# In[170]:


hist_indicator =  'Skill'


# In[171]:


data_to_plot.head()


# In[172]:


import json
country_geo = json.load(open("world-countries.json")) 
#country_geo = 'world-countries.json'
map = folium.Map(location=[100, 0], zoom_start=1.5)
map.choropleth(geo_data=country_geo, data=data_to_plot,
             columns=['Country', 'Skill'],
             key_on='feature.id',
             fill_color='YlOrRd', fill_opacity=0.5, line_opacity=0.2,
             legend_name=hist_indicator)


# In[173]:


# Create Folium plot
map.save('plot_data1.html')
# Import the Folium interactive html file
from IPython.display import HTML
HTML('<iframe src=plot_data1.html width=700 height=450></iframe>')


# In[174]:


df= sns.PairGrid(sample)
df.map_diag(sns.kdeplot)
df.map_offdiag(sns.kdeplot, n_levels=6);


# In[175]:


import seaborn as sns; 
# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Physicality', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Dribbling', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Defending', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Height', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Skill', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='Base Stats', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


# Scatterplot arguments
sns.lmplot(x='Overall Rating', y='In Game Stats', data=sample,
           fit_reg=False, # No regression line
           hue='Position')   # Color by evolution stage


# In[ ]:


plt.figure(figsize=(15,6))
sns.countplot(x="Overall Rating",data=sample)  


# In[ ]:


df = sns.jointplot(x="Overall Rating", y="Physicality", data=sample, kind="kde", color="m")
df.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
df.ax_joint.collections[0].set_alpha(0)
df.set_axis_labels("Overall Rating", "Physically");


# In[ ]:


df = sns.jointplot(x="Overall Rating", y="Shooting", data=sample, kind="kde", color="m")
df.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
df.ax_joint.collections[0].set_alpha(0)
df.set_axis_labels("Overall Rating", "Shooting");


# In[ ]:


# Generate sequential data and plot
plt.figure(figsize=(15,6))
sd = sample.sort_values('Overall Rating', ascending=False)[:8]
x1 = np.array(list(sd['Name']))
y1 = np.array(list(sd['Overall Rating']))
sns.barplot(x1, y1, palette= "colorblind")
plt.ylabel("Overall Rating")


# In[ ]:


# Generate sequential data and plot
plt.figure(figsize=(15,6))
sd = sample.sort_values('Overall Rating', ascending=False)[:10]
x1 = np.array(list(sd['Country']))
y1 = np.array(list(sd['Overall Rating']))
sns.barplot(x1, y1, palette= "colorblind")
plt.ylabel("Overall Rating")


# In[ ]:


# Generate sequential data and plot
plt.figure(figsize=(15,6))
sd = sample.sort_values('Overall Rating', ascending=False)[:10]
x1 = np.array(list(sd['Countryfullname']))
y1 = np.array(list(sd['Overall Rating']))
sns.barplot(x1, y1, palette= "colorblind")
plt.ylabel("Overall Rating")


# In[ ]:


f_fuko = sample.loc[sample['Position']=='RW']['Overall Rating']
m_fuko = sample.loc[sample['Position']=='ST']['Overall Rating']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='RW')
sns.distplot(m_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='ST')
plt.legend()


# In[ ]:


g = sns.pairplot(sample, hue="Position")


# In[ ]:


x = sample['Overall Rating']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()


# In[ ]:


from matplotlib.pyplot import figure
figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
ax = sns.scatterplot(x="Shooting", y='Overall Rating',  size="Position", data=sample)
sns.regplot(x="Shooting", y="Overall Rating", data=sample)


# In[ ]:


g = sns.pairplot(sample, vars=["Overall Rating", "Skill"], hue="Position")


# In[ ]:


g = sns.pairplot(sample, vars=["Overall Rating", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality" ])


# In[ ]:


g = sns.pairplot(sample, vars=["Overall Rating", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"], hue="Position")


# In[ ]:


g = sns.pairplot(sample, vars=["Overall Rating", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"], hue="Position")


# In[ ]:


g = sns.pairplot(sample, vars=["Overall Rating", "Height", "Base Stats", "In Game Stats"], hue="Position")


# Sort players based on their countries

# In[ ]:


#sort players based on their countries
sample.sort_values(by=['Countryfullname'], inplace=True)


# In[ ]:




