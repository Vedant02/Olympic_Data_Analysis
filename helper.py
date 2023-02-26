import numpy as np
import pandas as pd


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Gold'].astype(int) + medal_tally['Silver'].astype(int) + medal_tally[
        'Bronze'].astype(int)

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    # years.remove(1906)

    country = np.unique(df['Region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def fetch_medal_tally(df, year, country,season):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])

    flag = 0
    temp_df = medal_df
    if year == 'Overall' and country == 'Overall':
        if season == 'Summer':
            df = pd.read_html("https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table")
            t = df[1]
            b = t['Team']
            a = t['Summer Olympic Games']
            a = a.drop(columns=['No.'])

            region = pd.DataFrame()

            k = list()

            for i in b:
                for j in b[i]:
                    n = j.split('\xa0')
                    k.append(n[0])

            region.insert(0, 'Region', k)
            m = pd.concat([region,
                           a], axis=1)

            m.rename(
                columns={
                    '.mw-parser-output .tooltip-dotted{border-bottom:1px dotted;cursor:help}Team (IOC code)': 'Region',
                    'Unnamed: 2_level_1': 'Gold', 'Unnamed: 3_level_1': 'Silver', 'Unnamed: 4_level_1': 'Bronze'},
                inplace=True)

            m.at[96, 'Region'] = 'North Macedonia'
            m.at[144, 'Region'] = 'USA'
            remove = [156, 155, 154, 153, 113, 112, 111]
            m.drop(remove, axis=0, inplace=True)
            temp_df = m
        if season == 'Winter':
            temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['Region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['Region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:

        x = temp_df.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        return x.sort_values('Total', ascending=False)

    return x


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'Region']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Region'] == country]

    if len(new_df) == 0:
        return new_df

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['Region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset = ['Name','Region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset = ['Name','Region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on= 'Year', how = 'left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace = True)

    final.fillna(0,inplace=True)

    return final
