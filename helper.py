
import numpy as np


def country_year_list(df):
    # getting all the name of countries 
    country = np.unique(df['region'].dropna()).tolist()
    country.sort()
    country.insert(0, 'Overall')

    # getting all the years
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    return country, year


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def data_over_time(df, col):
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    data_over_time.rename(columns = {'index': 'Edition', 'Year': col}, inplace= True)

    return data_over_time


def most_succesfull(df, sport):
    temp_df = df.dropna(subset = ['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on = 'index', right_on = 'Name', 
                how = 'left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns = {'index': 'Name', 'Name_x': 'Total Medels', 'region': 'Region'}, inplace = True)    
    
    return x


def yearwise_medal_tally(df, country):

    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):

    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport', columns =  'Year', values = 'Medal', aggfunc = 'count').fillna(0).astype('int')

    return pt 


def most_succesfull_countrywise(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
        
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on = 'index', right_on = 'Name', 
                how = 'left')[['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns = {'index': 'Name', 'Name_x': 'Total Medels', 'region': 'Region'}, inplace = True)    
    
    return x


def weight_v_height(df, sport):

    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace = True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    
    return athlete_df


def male_v_female(df):

    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])

    male = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = male.merge(female, on = 'Year', how = 'left')
    final.rename(columns = {'Name_x': 'Male', 'Name_y': 'Female'}, inplace = True)
    final.fillna(0, inplace = True)

    return final


