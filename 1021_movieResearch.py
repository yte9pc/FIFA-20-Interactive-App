#!/usr/bin/env python
# coding: utf-8

# In[93]:


# import necessary modulus 
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re

from pylab import rcParams
import seaborn as sns, numpy as np


# In[94]:


from requests import get
url = 'http://www.imdb.com/search/title?release_date=2019&sort=num_votes,desc&page=1'
response = get(url)


# In[95]:


from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


# In[96]:


movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')


# In[97]:


headers = {"Accept-Language": "en-US, en;q=0.5"}


# In[98]:


pages = [str(i) for i in range(0,9)]
years_url = [str(i) for i in range(2010,2019)]


# In[99]:


from time import sleep
from random import randint


# In[100]:


from time import time;start_time = time()
from datetime import timedelta
requests = 0
for _ in range(5):
# A request would go here
    requests += 1
    sleep(randint(1,3))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))


# In[101]:


from IPython.core.display import clear_output
# start_time = time()requests = 0
for _ in range(10):
# Start to reaquest
    requests += 1
    sleep(randint(1,3))
    current_time = time()
    elapsed_time = current_time - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
clear_output(wait = True)


# In[102]:


from warnings import warn
warn("Warning Simulation")


# In[103]:


# Given lists for storage
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
grade_class = []
runing_time = []
moviegenre = []

# Start request and check requst response
start_time = time()
requests = 0

# lopping from pages 2010-2019
for year_url in years_url:

    # looping the page
    for page in pages:

        # Ask a request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page, headers = headers)

        # Sleep 
        sleep(randint(8,15))

        # Check request and monitor request response
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Thrown warning 
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break reqesuts for >100
        if requests > 100:
            warn('Number of requests was greater than expected.')
            break

        # Parse to beautiful stoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Find items and put into containers
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # Movie container for each page
        for container in mv_containers:
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


# In[104]:


import pandas as pd 
movie_ratings = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'grade': grade_class,
'runtime': runing_time,
'genre': moviegenre                               
})
print(movie_ratings.info())
movie_ratings.tail(10)


# In[105]:


movie_ratings = movie_ratings[['movie', 'year', 'imdb', 'metascore', 'votes', 'grade', 'runtime', 'genre']]
movie_ratings.head()


# In[106]:


movie_ratings['year'].unique()


# In[107]:


movie_ratings.loc[:, 'year'] = movie_ratings['year'].str[-5:-1].astype(int)


# In[108]:


movie_ratings['year'].tail(3)


# In[109]:


movie_ratings.describe().loc[['min', 'max'], ['imdb', 'metascore']]


# In[110]:


movie_ratings['n_imdb'] = movie_ratings['imdb'] * 10
movie_ratings.head(3)


# In[111]:


#Remove unwanted character in genre
genre_list = movie_ratings['genre'].tolist()
genre_name = []
for i in genre_list:
    name = i.strip("\n")
    genre_name.append(name)
#pass name back to genre_list
movie_ratings['genre'] = genre_name
movie_ratings.head(5)
print(movie_ratings.head(5))


# In[112]:


movie_ratings.to_csv('cs5010_movie_ratings.csv')


# In[125]:


import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
ax1, ax2, ax3 = fig.axes
ax1.hist(movie_ratings['runtime'], bins = 10, range = (120,160)) # bin range = 1
ax1.set_title('Runtime')
ax2.hist(movie_ratings['metascore'], bins = 10, range = (0,100)) # bin range = 10
ax2.set_title('Metascore')
ax3.hist(movie_ratings['runtime'], bins = 10, range = (0,100), histtype = 'step')
ax3.hist(movie_ratings['metascore'], bins = 10, range = (0,100), histtype = 'step')
ax3.legend(loc = 'upper left')
ax3.set_title('The Two Normalized Distributions')
for ax in fig.axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
plt.show()


# In[114]:


import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
ax1, ax2, ax3 = fig.axes
ax1.hist(movie_ratings['imdb'], bins = 10, range = (0,10)) # bin range = 1
ax1.set_title('IMDB rating')
ax2.hist(movie_ratings['metascore'], bins = 10, range = (0,100)) # bin range = 10
ax2.set_title('Metascore')
ax3.hist(movie_ratings['n_imdb'], bins = 10, range = (0,100), histtype = 'step')
ax3.hist(movie_ratings['metascore'], bins = 10, range = (0,100), histtype = 'step')
ax3.legend(loc = 'upper left')
ax3.set_title('The Two Normalized Distributions')
for ax in fig.axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
plt.show()


# In[115]:


#Start to make charts and do statistical analysis
import seaborn as sns, numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,5)
plt.scatter(movie_ratings.imdb, movie_ratings.votes)
plt.show()


# In[116]:


df = movie_ratings
print(df['runtime'])


# In[117]:


ax = sns.scatterplot(x="imdb", y="votes", hue="grade",data=df)


# In[118]:


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


# In[119]:


ax = sns.scatterplot(x="imdb", y="runtime", hue="grade",data=df)
yticks=np.arange(120,170,5)


# In[120]:


df = movie_ratings
df.describe()


# In[121]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# 
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(15, 8))
#using violinplot to showcase density and distribtuion of prices 
viz_2=sns.violinplot(data=df, x='grade', y='imdb')
viz_2.set_title('imdb rating by grade')


# In[122]:


df = movie_ratings
plt.figure(figsize=(15, 6))
sns.barplot(x='grade', y='imdb', hue='grade',data=df)


# In[123]:


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


# In[124]:


import sys
print(sys.executable)


# In[ ]:





# In[ ]:




