import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from flask import render_template

def read_data():
    
    COVID_CONFIRMED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    covid_confirmed = pd.read_csv(COVID_CONFIRMED_URL)
    covid_confirmed.head()
    
    COVID_DEATHS_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    covid_deaths = pd.read_csv(COVID_DEATHS_URL)
    covid_deaths.head()
    
    COVID_RECOVERED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    covid_recovered = pd.read_csv(COVID_RECOVERED_URL)
    covid_recovered.head()
    
    return analyse_data(covid_confirmed,covid_deaths,covid_recovered)


def analyse_data(covid_confirmed,covid_deaths,covid_recovered):
    covid_confirmed['Country/Region'].replace('Mainland China', 'China', inplace=True)
    covid_deaths['Country/Region'].replace('Mainland China', 'China', inplace=True)
    covid_recovered['Country/Region'].replace('Mainland China', 'China', inplace=True)
    
    covid_confirmed[['Province/State']] = covid_confirmed[['Province/State']].fillna('')
    covid_confirmed.fillna(0, inplace=True)
    
    covid_deaths[['Province/State']] = covid_deaths[['Province/State']].fillna('')
    covid_deaths.fillna(0, inplace=True)
    
    covid_recovered[['Province/State']] = covid_recovered[['Province/State']].fillna('')
    covid_recovered.fillna(0, inplace=True)
    
    covid_confirmed.isna().sum().sum()
    covid_deaths.isna().sum().sum()
    covid_recovered.isna().sum().sum()
    
    covid_deaths_count = covid_deaths.iloc[:, 4:].sum().max()
    covid_recovered_count = covid_recovered.iloc[:, 4:].sum().max()
    covid_confirmed_count = covid_confirmed.iloc[:, 4:].sum().max()
    
    world_df = pd.DataFrame({
        'confirmed': [covid_confirmed_count],
        'deaths': [covid_deaths_count],
        'recovered': [covid_recovered_count],
        'active': [covid_confirmed_count - covid_deaths_count - covid_recovered_count]
    })
    
    world_long_df = world_df.melt(value_vars=['active', 'deaths', 'recovered'],
                                var_name="status",
                                value_name="count")
    
    world_long_df['upper'] = 'confirmed'
    
    covid_worldwide_confirmed = covid_confirmed.iloc[:, 4:].sum(axis=0)
    covid_worldwide_confirmed.head()
    
    covid_worldwide_deaths = covid_deaths.iloc[:, 4:].sum(axis=0)
    covid_worldwide_deaths.head()
    
    covid_worldwide_recovered = covid_recovered.iloc[:, 4:].sum(axis=0)
    covid_worldwide_recovered.head()
    
    covid_worldwide_active = covid_worldwide_confirmed - covid_worldwide_deaths - covid_worldwide_recovered
    covid_worldwide_active.head()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    
    sns.lineplot(x=covid_worldwide_confirmed.index, y=covid_worldwide_confirmed, sort=False, linewidth=2)
    sns.lineplot(x=covid_worldwide_deaths.index, y=covid_worldwide_deaths, sort=False, linewidth=2)
    sns.lineplot(x=covid_worldwide_recovered.index, y=covid_worldwide_recovered, sort=False, linewidth=2)
    sns.lineplot(x=covid_worldwide_active.index, y=covid_worldwide_active, sort=False, linewidth=2)
    
    plt.suptitle("Coronavirus cases - Worldwide", fontsize=30, fontweight='bold', color='blue')
    plt.xticks(rotation=45, fontsize=10)
    plt.ylabel('Cases')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.legend(['Confirmed', 'Death', 'Recovered', 'Active'])
    plt.tick_params(axis='x', which='major', labelsize=8)
    plt.savefig("app/static/covid-image.png")
