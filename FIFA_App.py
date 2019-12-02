#!/usr/bin/env python
# coding: utf-8

# ### Import neccessary packages

# In[1]:


from bokeh.models.annotations import Title
from bokeh.plotting import figure
from bokeh.layouts import layout, column, gridplot, widgetbox, row
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, Div, Slider, Select, TextInput, RangeSlider, MultiSelect, CheckboxGroup, AutocompleteInput, Panel, Tabs, HoverTool
from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.models.layouts import LayoutDOM
from math import pi
import numpy as np
import pandas as pd
import math 


# ### Read in csv file

# In[2]:


fifa = pd.read_csv('FIFA Player Info.csv', keep_default_na = False)
fifa = fifa.drop(columns='Unnamed: 0')


# ### Create Slider, MultiSelect, and Input for Scatter Plot

# In[3]:


player = AutocompleteInput(title="Player Name", completions=fifa.Name.tolist())
overall_rating = RangeSlider(title="Overall Rating", start=fifa['Overall Rating'].min(), end=fifa['Overall Rating'].max(), value=(fifa['Overall Rating'].min(), fifa['Overall Rating'].max()), step=1)
skill = RangeSlider(title="Skill", start=fifa['Skill'].min(), end=fifa['Skill'].max(), value=(fifa['Skill'].min(), fifa['Skill'].max()), step=1, default_size = 400)
club = MultiSelect(title="Clubs", options=fifa.sort_values('Club').Club.unique().tolist(), size =  10)
league = MultiSelect(title="Leagues", options=fifa.sort_values('League').League.unique().tolist(), size =  10)
country = MultiSelect(title="Countries", options=fifa.sort_values('Country').Country.unique().tolist(), size =  10)
position = MultiSelect(title="Positions", options=['CF', 'ST', 'RW', 'RF', 'LW', 'LF', 'RM', 'LM', 'CAM', 'CM', 'CDM', 'LB', 'LWB', 'RB', 'RWB', 'CB', 'GK'], size =  10)


# ### Create Scatter Plot and html code for describing the interface

# In[11]:


axis_map = dict(zip(fifa.select_dtypes(include='int').columns.values, fifa.select_dtypes(include='int').columns.values))
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Dribbling")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Passing")

source = ColumnDataSource(data=dict(x=[], y=[], color=[], legend=[], player=[], overallrating=[], club=[], league=[], country = [], position=[]))
TOOLTIPS=[
    ("Player", "@player"),
    ("Overall Rating", "@overallrating"),
    ("Club", "@club"),
    ("League", "@league"),
    ("Country", "@country"),
    ("Position", "@position")
]
p = figure(plot_height=600, plot_width=700, tooltips=TOOLTIPS, sizing_mode="scale_both")

p.circle(x="x", y="y", source=source, size=10, color = "color", line_color='grey', hover_fill_color='black', 
         hover_alpha=0.5, legend="legend")

desc = Div(text="""<style>
h1 {
    margin: 1em 0 0 0;
    color: #2e484c;
    font-family: 'Julius Sans One', sans-serif;
    font-size: 1.8em;
    text-transform: uppercase;
}
a:link {
    font-weight: bold;
    text-decoration: none;
    color: #0d8ba1;
}
a:visited {
    font-weight: bold;
    text-decoration: none;
    color: #1a5952;
}
a:hover, a:focus, a:active {
    text-decoration: underline;
    color: #9685BA;
}
p {
    font: "Libre Baskerville", sans-serif;
    text-align: justify;
    text-justify: inter-word;
    width: 80%;
    max-width: 800;
}

</style>

<h1>An Interactive Explorer of FIFA 2020 Player Data</h1>

<p>
Interact with the widgets on the left to query a subset of players to plot.
Hover over the circles to see more information about each player.
</p>""",
sizing_mode="stretch_width")


# ### Select function updates the plot based on user selection

# In[15]:


def select_fifa():
    # Stores the values selected by the user
    overall_rating_val = overall_rating.value
    skill_level = skill.value
    player_val = player.value
    league_val = league.value
    club_val = club.value
    country_val = country.value
    position_val = position.value
    
    # Filter FIFA data based on overall rating and skill
    selected = fifa[
        (fifa['Overall Rating'] >= overall_rating_val[0]) &
        (fifa['Overall Rating'] <= overall_rating_val[1]) &
        (fifa['Skill'] >= skill_level[0]) &
        (fifa['Skill'] <= skill_level[1])
    ]
    
    # Filter FIFA data if player name, league, club, or position is not null
    if (player_val != ""):
        selected = selected[selected.Name.str.contains(player.value)==True]
    if (len(league_val) != 0):
        selected = selected[selected.League.isin(league_val)==True]
    if (len(club_val) != 0):
        selected = selected[selected.Club.isin(club_val)==True]
    if (len(country_val) != 0):
        selected = selected[selected.Country.isin(country_val)==True]
    if (len(position_val) != 0):
        selected = selected[selected.Position.isin(position_val)==True]
    
    # Calculate 75th, 50th, and 25th percentile
    per75 = np.percentile(selected[y_axis.value], 75)
    per50 = np.percentile(selected[y_axis.value], 50)
    per25 = np.percentile(selected[y_axis.value], 25)
    
    # Color each player based on percentile group
    selected["color"] = np.where(selected[y_axis.value] > per50, np.where(selected[y_axis.value] > per75,'#29788E', '#79D151'),
                       np.where(selected[y_axis.value] < per25, '#8C2980', '#FD9F6C') ) 
    # Create legend
    selected["legend"] = np.where(selected[y_axis.value] > per50, np.where(selected[y_axis.value] > per75,'Top 25th Percentile', '75th Percentile'),
                        np.where(selected[y_axis.value] < per25, 'Bottom 25th Percentile', '50th Percentile') )
    return selected


# ### Update function calls select_fifa() function to update plot automatically

# In[16]:


def update():
    # Retrieve the subset of data to plot
    df = select_fifa()

    # X and Y axis value selected by the user
    #x_name = axis_map.get(x_axis.value)
    #y_name = axis_map.get(y_axis.value)
    x_name = x_axis.value
    y_name = y_axis.value
    
    # Labels
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.xaxis.axis_label_text_font_size = "14pt"
    p.yaxis.axis_label_text_font_size = "14pt"
    p.xaxis.major_label_text_font_size = "12pt"
    p.yaxis.major_label_text_font_size = "12pt"
    
    # Title text
    p.title.text = str(len(df)) + " Players selected                                                              " + x_axis.value + ' vs ' + y_axis.value
    p.title.text_font_size = '16pt'
    
    # Legend position
    p.legend.location = "top_left"
    
    # Source data for scatter plot
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        legend=df["legend"],
        player=df["Name"],
        club=df["Club"], 
        league=df["League"], 
        position=df["Position"], 
        country=df['Country'],
        overallrating=df["Overall Rating"],
    )

# Check if the user input has changed
controls = [player, overall_rating, skill, league, club, country, position, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# Layout of first tab
inputs = column(*controls, width=350, height=1000)
inputs.sizing_mode = "fixed"
l = layout([
    [desc],
    [inputs, p],
], sizing_mode="scale_both")


# ###  Create Select for Histogram

# In[18]:


# X axis that user can select from
hist_x_axis = ['Skill', 'Weak Foot', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality', 'Height']

club3 = Select(title="Clubs", value = 'Any', options=['Any'] + fifa.sort_values('Club').Club.unique().tolist())
league3 = Select(title="Leagues", value = 'Any', options=['Any'] + fifa.sort_values('League').League.unique().tolist())
country3 = Select(title="Countries", value = 'Any', options=['Any'] + fifa.sort_values('Country').Country.unique().tolist())
position3 = Select(title="Position Groups", value = 'Any', options=['Any'] + fifa.sort_values('Position Group')['Position Group'].unique().tolist())
skills3 = Select(title="Skills", value = 'Passing', options=hist_x_axis)


# ### Create Histogram and html code for describing the interface

# In[ ]:


arr_src = ColumnDataSource(data=dict(count=[],left=[], right=[], f_count=[], f_interval=[]))

p3 = figure(plot_height=700, plot_width=1200, sizing_mode="scale_both",
                background_fill_color="#fafafa")

p3.quad(bottom=0, 
           top='count', 
           left='left', 
           right='right', 
           source=arr_src,
           hover_fill_alpha=0.5,
           hover_fill_color='grey',
           fill_color="orange", 
           line_color="black", 
            alpha=0.7)

# Title
p3.title.align = 'center'
p3.title.text = "Histogram of " + skills3.value + " Rating"

# Axis labels
p3.xaxis.axis_label = skills3.value + " Rating"
p3.yaxis.axis_label = "Number of Players"
p3.title.text_font_size = '16pt'
p3.xaxis.axis_label_text_font_size = "14pt"
p3.yaxis.axis_label_text_font_size = "14pt"
p3.xaxis.major_label_text_font_size = "12pt"
p3.yaxis.major_label_text_font_size = "12pt"

# Add a hover tool referring to the formatted columns
hover = HoverTool(tooltips = [(skills3.value, '@f_interval'),
                                  ('Count', '@f_count')])

# Add the hover tool to the graph
p3.add_tools(hover)

desc3 = Div(text="""<style>
h1 {
    margin: 1em 0 0 0;
    color: #2e484c;
    font-family: 'Julius Sans One', sans-serif;
    font-size: 1.8em;
    text-transform: uppercase;
}
a:link {
    font-weight: bold;
    text-decoration: none;
    color: #0d8ba1;
}
a:visited {
    font-weight: bold;
    text-decoration: none;
    color: #1a5952;
}
a:hover, a:focus, a:active {
    text-decoration: underline;
    color: #9685BA;
}
p {
    font: "Libre Baskerville", sans-serif;
    text-align: justify;
    text-justify: inter-word;
    width: 80%;
    max-width: 800;
}

</style>

<h1>An Interactive Explorer of FIFA 2020 Player Data</h1>

<p>
Interact with the widgets below to explore the distribution of players' skill.
</p>""",
sizing_mode="stretch_width")


# ### Select function updates the histogram based on user selection

# In[ ]:


def select_hist():
    # Stores the values selected by the user
    club3_val = club3.value
    league3_val = league3.value
    country3_val = country3.value
    position3_val = position3.value
    skills3_val = skills3.value
    
    selected = fifa
    
    # Filter FIFA data if league, club, country, or position is not null
    if (club3_val != 'Any'):
        selected = selected[selected.Club == club3_val]
    if (league3_val != 'Any'):
        selected = selected[selected.League == league3_val]
    if (country3_val != 'Any'):
        selected = selected[selected.Country == country3_val]
    if (position3_val != 'Any'):
        selected = selected[selected['Position Group'] == position3_val]
    
    return selected, skills3_val


# ### Update function calls select_hist() function to update histogram automatically

# In[ ]:


def update3():
    # Retrieve the subset of data to use
    df, skill = select_hist()
    arr_hist, edges = np.histogram(df[skill], density=False, bins='auto')

    # Column data source
    arr_df = pd.DataFrame({'count': arr_hist, 'left': edges[:-1], 'right': edges[1:]})
    arr_df['f_count'] = ['%d' % count for count in arr_df['count']]
    arr_df['f_interval'] = ['%d to %d ' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
    
    # Update Title and X-axis
    p3.title.text = "Histogram of " + skill + " Rating"
    p3.xaxis.axis_label = skill + " Rating"
    
    # Source data for Histogram
    arr_src.data = dict(count=arr_df['count'],
                        left=arr_df['left'], 
                        right=arr_df['right'], 
                        f_count=arr_df['f_count'], 
                        f_interval=arr_df['f_interval'],) 

# Check if the user input has changed    
controls3 = [club3, league3, country3, position3, skills3]
for control in controls3:
    control.on_change('value', lambda attr, old, new: update3())

# Layout of second tab
inputs3 = row(*controls3, width=1200)
inputs3.sizing_mode = "fixed"
l3 = column(row(desc3),row(club3, league3, country3, position3,skills3),row(p3))


# ### Best Starting 11

# In[ ]:


# Formation to select from
formation_list = ['Any','442', '433', '451', '352']

# Remove countries without enough players
countrylist = fifa.groupby('Country')
minplayers = countrylist.filter(lambda x: x['Overall Rating'].count() > 18)

# Skill set
best_x_axis = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Overall Rating']


# #### Create Select and MultiSelect

# In[ ]:


skills2 = Select(title="Skills", value = 'Overall Rating', options=best_x_axis)
formation = Select(title="Formation", value = 'Any', options=formation_list)
club2 = MultiSelect(title="Clubs", options=fifa.sort_values('Club').Club.unique().tolist(), size =  10)
league2 = MultiSelect(title="Leagues", options=fifa.sort_values('League').League.unique().tolist(), size =  10)
country2 = MultiSelect(title="Countries", options=minplayers.sort_values('Country').Country.unique().tolist(), size =  10)
continent = MultiSelect(title="Continent", options=fifa.sort_values('Continent').Continent.unique().tolist(), size = 6)


# ### Create Plot of Best Starting 11 and html code for describing the interface

# In[ ]:


source2 = ColumnDataSource(data=dict(x=[], y=[], color=[], legend=[], player=[], club=[], league=[], 
                                   country = [], continent= [], overallrating=[], pace=[], shooting=[],
                                   passing=[], dribbling=[], defending=[], physicality=[]))
TOOLTIPS2=[
    ("Player", '@player'),
    ("Club", "@club"),
    ("League", "@league"),
    ("Country", "@country"),
    ("Continent", "@continent"),
    ("Overall Rating", "@overallrating"),
    ("Pace", "@pace"),
    ("Shooting", "@shooting"),
    ("Passing", "@passing"),
    ("Dribbling", "@dribbling"),
    ("Defending", "@defending"),
    ("Physicality", "@physicality")
]
p2 = figure(plot_height=900, plot_width=1000, tooltips=TOOLTIPS2, sizing_mode="scale_both", x_range=(5, 130))
p2.circle(x="x", y="y", source=source2, size=75, color = "color", line_color='grey', hover_fill_color='black', 
         hover_alpha=0.5, legend="legend")

desc2 = Div(text="""<style>
h1 {
    margin: 1em 0 0 0;
    color: #2e484c;
    font-family: 'Julius Sans One', sans-serif;
    font-size: 1.8em;
    text-transform: uppercase;
}
a:link {
    font-weight: bold;
    text-decoration: none;
    color: #0d8ba1;
}
a:visited {
    font-weight: bold;
    text-decoration: none;
    color: #1a5952;
}
a:hover, a:focus, a:active {
    text-decoration: underline;
    color: #9685BA;
}
p {
    font: "Libre Baskerville", sans-serif;
    text-align: justify;
    text-justify: inter-word;
    width: 80%;
    max-width: 800;
}

</style>

<h1>An Interactive Explorer of FIFA 2020 Player Data</h1>

<p>
Interact with the widgets on the left to discover the best starting 11 players.
Hover over the circles to see more information about each player.
</p>""",
sizing_mode="stretch_width")


# In[ ]:


def bestplayers(df, formation, skill):
    # Each position group
    df_GK = df[df['Position Group'] == 'Goal Keeper']
    df_DD = df[df['Position Group'] == 'Defender']
    df_MD = df[df['Position Group'] == 'Midfielder']
    df_AK = df[df['Position Group'] == 'Attacker']
    
    # Number of Defenders, Midfielders, and Attackers
    i = int(formation[0])
    j = int(formation[1])
    k = int(formation[2])
    
    # Best Goalie, Defenders, Midfielders, and Attackers based on the formation and skill
    team = df_GK.nlargest(1, skill)
    team = team.append(df_DD.nlargest(i, skill))
    team = team.append(df_MD.nlargest(j, skill))
    team = team.append(df_AK.nlargest(k, skill))
    return team

def bestformation(df, formation, skill):
    # Formation selected
    formation2_value = formation

    # If formation is Any then pick the formation with the highest mean skill rating
    if formation2_value == 'Any':
        best_formation = [0,'formation']
        new_formation_list = ['442', '433', '451', '352']
        for i in new_formation_list:
            if bestplayers(df, i, skill)[skill].mean() > best_formation[0]:
                best_formation[0] = bestplayers(df, i, skill)[skill].mean()
                best_formation[1] = i
        best_formation = best_formation[1]
    else:
        best_formation = formation2_value
    
    # Return the best starting 11
    best = bestplayers(df, best_formation, skill)
    
    # Based on the formation define where to plot each player
    if best_formation == '442':
        best['X'] = [62.5, 25, 50, 75, 100, 25, 50, 75, 100, 41.7, 83.3]
        best['Y'] = [40, 60, 60, 60, 60, 85, 85, 85, 85, 110, 110]
    if best_formation == '433':
        best['X'] = [62.5, 25, 50, 75, 100, 31.3, 62.5, 93.75, 31.3, 62.5, 93.75]
        best['Y'] = [40, 60, 60, 60, 60, 85, 85, 85, 110, 110, 110]
    if best_formation == '451':
        best['X'] = [62.5, 25, 50, 75, 100, 20.8, 41.7, 62.5, 83.3, 104.2, 62.5]
        best['Y'] = [40, 60, 60, 60, 60, 85, 85, 85, 85, 85, 110]
    if best_formation == '352':
        best['X'] = [62.5, 31.3, 62.5, 93.75, 20.8, 41.7, 62.5, 83.3, 104.2, 41.7, 83.3]
        best['Y'] = [40, 60, 60, 60, 85, 85, 85, 85, 85, 110, 110]
        
    return best


# In[ ]:


def select_fifa2():
    formation_val = formation.value
    club_val = club2.value
    league_val = league2.value
    country_val = country2.value
    continent_val = continent.value
    
    selected = fifa
    if (len(league_val) != 0):
        selected = selected[selected.League.isin(league_val)==True]
    if (len(club_val) != 0):
        selected = selected[selected.Club.isin(club_val)==True]
    if (len(country_val) != 0):
        selected = selected[selected.Country.isin(country_val)==True]
    if (len(continent_val) != 0):
        selected = selected[selected.Continent.isin(continent_val)==True]
        
    selected = bestformation(selected, formation_val, skills2.value)
    
    # Color code each position group
    color = []
    for column in selected['Position Group']:
        if column == 'Goal Keeper':
            color.append('#29788E')
        if column == 'Defender':
            color.append('#79D151')    
        if column == 'Midfielder':
            color.append('#8C2980')
        if column == 'Attacker':
            color.append('#FD9F6C')
    selected["color"] = color
    # Legend
    selected["legend"] = selected['Position Group']
    return selected

def update2():
    df = select_fifa2()
    
    # No x and y axis
    p2.xgrid.grid_line_color = None
    p2.ygrid.grid_line_color = None
    # Title
    p2.title.text = "Best Starting 11 Based on " + formation.value + " Formation & " + skills2.value
    p2.title.text_font_size = '16pt'
    # Legend
    p2.legend.location = "top_right"
    p2.axis.visible = False
    
    # Source data for plot
    source2.data = dict(
        x=df['X'],
        y=df['Y'],
        color=df["color"],
        legend=df["legend"],
        player=df["Name"],
        club=df["Club"], 
        league=df["League"], 
        country=df["Country"],
        continent=df["Continent"],
        overallrating=df['Overall Rating'],
        pace=df["Pace"],
        shooting=df["Shooting"],
        passing=df["Passing"],
        dribbling=df["Dribbling"],
        defending=df["Defending"],
        physicality=df["Physicality"],
    )

# Check if the user input has changed       
controls2 = [club2, league2, country2, continent, skills2, formation]
for control in controls2:
    control.on_change('value', lambda attr, old, new: update2())

# Layout of third tab
inputs2 = column(club2, league2, country2, continent, width=320, height=850)
inputs2.sizing_mode = "fixed"
l2 = column(row(desc2),row(inputs2, p2, column(formation, skills2)))


# In[ ]:


# Create a panel for each tab
first_tab = Panel(child = l, title = 'Scatter Plot')
second_tab = Panel(child = l3, title = 'Histogram of Players Skill')
third_tab = Panel(child = l2, title = 'Best Starting 11')
tabs = Tabs(tabs =[first_tab, second_tab, third_tab])

# initial load of the data
update()
update2()
update3()
curdoc().add_root(tabs)
curdoc().title = "FIFA 2020 Players"

