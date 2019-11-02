import pandas as pd

def position(DFColumn):
    positions = {
            'Attacker' : ['CF', 'ST', 'RW', 'RF', 'LW', 'LF'], 
            'Midfieder' : ['RM', 'LM', 'CAM', 'CM', 'CDM'],
            'Defender' : ['LB', 'LWB', 'RB', 'RWB', 'CB'],
            'Goal Keeper' : ['GK']}
    for position in positions.keys():
        if DFColumn in positions.get(position):
            return(position)

DF = pd.read_csv('FIFA Player Info.csv')
DF.insert(6, "Position Group", DF['Position'].apply(position), True) 

countries = DF["Country"].unique() 

#Select best players from a specific country, based on their formation
#The input value df is the dataframe containing all players from that country
#The 2nd input formation is a string of three digits, '442', '433', '451', or '352'
def countryteam(df, formation):
    df_GK = df[df['Position Group'] == 'Goal Keeper']
    df_DD = df[df['Position Group'] == 'Defender']
    df_MD = df[df['Position Group'] == 'Midfieder']
    df_AK = df[df['Position Group'] == 'Attacker']
    i = int(formation[0])
    j = int(formation[1])
    k = int(formation[2])
    team = df_GK.nlargest(1, ['Overall Rating'])
    team = team.append(df_DD.nlargest(i, ['Overall Rating']))
    team = team.append(df_MD.nlargest(j, ['Overall Rating']))
    team = team.append(df_AK.nlargest(k, ['Overall Rating']))
    return(team)

#this function is to return a dataframe with all players from a certain country
def countryplayers(df, country):
    dfc = df[df['Country']==country]
    return(dfc)

#the best country team irrespective of their formations
#the input is the dataframe containing all players
def countryteam_allform(df):
    formations = ('442', '433', '451', '352')
    high_score = 0
    for tp in formations:
        if sum(countryteam(df, tp)['Overall Rating']) > high_score:
            high_score = sum(countryteam(df, tp)['Overall Rating'])
            bestcountryteam = countryteam(df, tp)
    return(bestcountryteam)


# countryteams is a dictionary, key is the name of country, 
# value is the best team from that country irrespective of its formation
countryteams = {}
for country in countries:
    countryteams.update({country: \
        countryteam_allform(countryplayers(DF, country))})
maxrating = 0
for key in countryteams:
    sumrating = sum(countryteams[key]['Overall Rating'])
    if sumrating > maxrating:
        maxrating = sumrating
        bestcountry = key
print(bestcountry)
print(countryteam_allform(countryplayers(DF, bestcountry)))
print(sum(countryteams[bestcountry]['Overall Rating']))    
 
    