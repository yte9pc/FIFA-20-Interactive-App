#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import necessary libraries

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

#import urlib.requesst to open URLs
from urllib.request import urlopen 

#import Beautiful Soup package to extract data from html fles
from bs4 import BeautifulSoup
import re

#import necessary modules for data visualization
from pylab import rcParams
import seaborn as sns, numpy as np


# In[2]:


from requests import get
url = 'http://www.imdb.com/search/title?release_date=2019&sort=num_votes,desc&page=1'
response = get(url)


# In[3]:


from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


# In[4]:


mv_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')


# In[5]:


headers = {"Accept-Language": "en-US, en;q=0.5"}


# In[6]:


pages = [str(i) for i in range(1,10)]
years_url = [str(i) for i in range(2010,2019)]


# In[7]:


from time import sleep
from random import randint


# In[8]:


from time import time;start_time = time()
from datetime import timedelta
requests = 0
for _ in range(5):
# A request goes here
    requests += 1
    sleep(randint(1,3))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))


# In[9]:


from IPython.core.display import clear_output
# start_time = time()requests = 0
for _ in range(10):
# A request would go here
    requests += 1
    sleep(randint(1,3))
    current_time = time()
    elapsed_time = current_time - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
clear_output(wait = True)


# In[10]:


from warnings import warn
warn("Warning Simulation")


# In[11]:


# Redeclaring the lists to store data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
grade_class = []
runing_time = []
moviegenre = []

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every year in the interval 2010-2019
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page, headers = headers)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 100:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        imdb_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # For every movie of these 50
        for container in imdb_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_ = 'ratings-metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))

                # Scrape the number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))
                
                # Scrape the grade
                grade = container.find('span', class_ = 'certificate').text
                grade_class.append(grade) 
                
                # Scrape the runtime
                runtime = container.find('span', class_ = 'runtime').text
                runing_time.append(runtime) 
                
                # Scrape the genre
                genre = container.find('span', class_ = 'genre').text
                moviegenre.append(genre) 


# In[12]:


import pandas as pd 
imdb_ratings = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'grade': grade_class,
'runtime': runing_time,
'genre': moviegenre                               
})
print(movie_ratings.info())
imdb_ratings.tail(10)


# In[13]:


imdb_ratings = imdb_ratings[['movie', 'year', 'imdb', 'metascore', 'votes', 'grade', 'runtime', 'genre']]
imdb_ratings.head()


# In[14]:


imdb_ratings['year'].unique()


# In[15]:


imdb_ratings.loc[:, 'year'] = movie_ratings['year'].str[-5:-1].astype(int)


# In[16]:


imdb_ratings['year'].tail(3)


# In[17]:


imdb_ratings.describe().loc[['min', 'max'], ['imdb', 'metascore']]


# In[18]:


imdb_ratings['n_imdb'] = movie_ratings['imdb'] * 10
imdb_ratings.head(3)


# In[19]:


imdb_ratings.to_csv('movie_ratings_2019.csv')


# In[20]:


#Start to make charts and do statistical analysis
import seaborn as sns, numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,5)
plt.scatter(movie_ratings.imdb, movie_ratings.votes)
plt.show()


# In[21]:


df = movie_ratings
print(df['runtime'])


# In[22]:


ax = sns.scatterplot(x="imdb", y="votes", hue="grade",data=df)


# In[23]:


#Need to change format of Volume from string to numeric 
runtime_num_list = df['runtime'].tolist()
runtime_num = []
for i in runtime_num_list:
    if i.endswith('min'):
        num = i.strip("min")
        runtime_num.append(num)
#pass num back to Volume_list
df['runtime'] = runtime_num
df.head(5)
df['runtime'] = pd.to_numeric(df['runtime'])


# In[24]:


ax = sns.scatterplot(x="imdb", y="runtime", hue="grade",data=df)
yticks=np.arange(120,170,5)


# In[25]:


df = movie_ratings
df.describe()


# In[26]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# 
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(15, 8))
#using violinplot to showcase density and distribtuion of prices 
viz_2=sns.violinplot(data=df, x='grade', y='imdb')
viz_2.set_title('imdb rating by grade')


# In[27]:


df = movie_ratings
plt.figure(figsize=(15, 6))
sns.barplot(x='grade', y='imdb', hue='grade',data=df)


# In[28]:


#word cloud
from wordcloud import WordCloud, ImageColorGenerator
text = " ".join(str(each) for each in df.genre)
# Create and generate a word cloud image:
wordcloud = WordCloud(max_words=400).generate(text)
plt.figure(figsize=(15,10))
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[29]:


import sys
print(sys.executable)


# In[ ]:





# In[ ]:




