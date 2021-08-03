
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff 


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://i.pinimg.com/originals/27/07/eb/2707ebe3f9114547b13a6ad01daf5f51.png')
user_menue = st.sidebar.radio(
    'Chose an Option',
    ('Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis')
)


if user_menue == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    country, year = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year', year)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall performance')
    
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in ' + str(selected_year) + ' Olympics')
    
    st.table(medal_tally)


if user_menue == 'Overall Analysis':

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x = 'Edition', y = 'region')
    st.title('Participating Nations Over Time')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x = 'Edition', y = 'Event')
    st.title('Events Over Time')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x = 'Edition', y = 'Name')
    st.title('Athletes Over Time')
    st.plotly_chart(fig)

    st.title('No of Events Over Time(Every Sport)')
    fig, ax = plt.subplots(figsize = (20, 20))
    y = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(y.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc = 'count').fillna(0).astype('int'), 
                annot = True)
    st.pyplot(fig)

    
    st.title('Most Succesfull Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    z = helper.most_succesfull(df, selected_sport)
    st.table(z)
    

if user_menue == 'Country wise Analysis':
    st.sidebar.title('Country-Wise Analysis')

    country_list = np.unique(df['region'].dropna()).tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Country', country_list)
    
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x = 'Year', y = 'Medal')
    st.title(selected_country + ' Medals Over Time')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in the following sports')
    country_heatmap = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize = (20, 20))
    ax = sns.heatmap(country_heatmap, annot = True)
    st.pyplot(fig)

    st.title('Top 10 most succesfull Athletes of ' + selected_country)
    top10_df = helper.most_succesfull_countrywise(df, selected_country)
    st.table(top10_df)



if user_menue == 'Athlete wise Analysis':
    st.title('Age Distribution')

    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                    show_hist = False,show_rug = False)
    fig.layout.update({'xaxis':{'title': 'Age'}})
    fig.update_layout(autosize = False, width = 1000, height = 590)
    st.plotly_chart(fig)


    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Polo', 'Ice Hockey']


    st.title('Age Distribution wrt to Sports')
    medel_list = ['Gold', 'Silver', 'Bronze']
    selected_medel = st.selectbox('Select Medel', medel_list)
    st.header(selected_medel + ' Medalist')

    x = []
    name = []

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        temp_df = temp_df.dropna(subset = ['Sport'])
        x.append(temp_df[temp_df['Medal'] == selected_medel]['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist = False, show_rug = False)
    fig.layout.update({'xaxis':{'title': 'Age'}})
    fig.update_layout(autosize = False, width = 1000, height = 590)
    st.plotly_chart(fig)


    st.title('Weight vs Height')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    
    w_v_h = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(w_v_h['Weight'], w_v_h['Height'], hue = w_v_h['Medal'], style = w_v_h['Sex'], s = 50)
    st.pyplot(fig)


    st.title('Men vs Women participation over the years')
    final = helper.male_v_female(df)
    fig = px.line(final, x = 'Year', y = ['Male', 'Female'])
    fig.update_layout(autosize = False, width = 1000, height = 590)
    st.plotly_chart(fig)


