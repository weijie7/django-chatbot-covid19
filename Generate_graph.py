import sys
import django
import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'ChatBot_Main.settings')
# setting can be found in wsgi.py folder in pycache
os.environ['DJANGO_SETTINGS_MODULE'] = 'ChatBot_Main.settings'
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


class plotGraphs():

    def start(self):
        #plot individual country charts
        inf_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        inf_link_us = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"

        inf_global = pd.read_csv(inf_link)
        inf_us = pd.read_csv(inf_link_us)

        inf_us = pd.concat([inf_us.iloc[:,6:8], inf_us.iloc[:,-30:]],axis=1)
        inf_global = pd.concat([inf_global.iloc[:,0:2],inf_global.iloc[:,-30:]],axis=1)
        inf_us_grp = inf_us.groupby(by='Country_Region').sum().T
        inf_pr_grp = inf_us[inf_us['Province_State'] == 'Puerto Rico'].groupby(by='Province_State').sum().T
        inf_global_grp = inf_global.groupby(by='Country/Region').sum().T

        dead_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        dead_link_us = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

        dead_global = pd.read_csv(dead_link)
        dead_us = pd.read_csv(dead_link_us)

        dead_us = pd.concat([dead_us.iloc[:,6:8], dead_us.iloc[:,-30:]],axis=1)
        dead_global = pd.concat([dead_global.iloc[:,0:2],dead_global.iloc[:,-30:]],axis=1)
        dead_us_grp = dead_us.groupby(by='Country_Region').sum().T
        dead_pr_grp = dead_us[dead_us['Province_State'] == 'Puerto Rico'].groupby(by='Province_State').sum().T
        dead_global_grp = dead_global.groupby(by='Country/Region').sum().T

        sns.set(style="whitegrid")
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12,6), sharex=True)
        for i in inf_global_grp.columns:
            df = inf_global_grp[i]
            df.index = pd.to_datetime(df.index)
            df2 = dead_global_grp[i]
            df2.index = pd.to_datetime(df.index)
            fig.suptitle(f'Total Confirmed Cases in {i} for Past 30 Days', fontsize= 18)
            ax = sns.lineplot(data=df, palette="tab10", linewidth=2.5, marker='o', color="coral", ax = axs[0], legend='full')
            ax2 = sns.lineplot(data=df2, palette="tab10", linewidth=2.5, marker='o', color="red", ax = axs[1], legend='full')
            ax.set_ylabel('Total Diagnosed')
            ax2.set_ylabel('Total Death')
            ax.set_xlabel('Date (past 30 days)')
            ax.figure.legend(['Total Diagnosed', 'Total Death'])
            fig.autofmt_xdate()
            plt.savefig(f'static/plots/{i.lower().replace("*","")}.png',bbox_inches = "tight")
            ax.cla()
            ax2.cla()
            print(f"graph {i} plotted")

        # US ONLY
        
        for i in inf_us_grp.columns:
            sns.set(style="whitegrid")
            df = inf_us_grp[i]
            df.index = pd.to_datetime(df.index)
            df2 = dead_us_grp[i]
            df2.index = pd.to_datetime(df.index)
            fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12,6), sharex=True)
            fig.suptitle(f'Total Confirmed Cases in {i} for Past 30 Days', fontsize= 18)
            ax = sns.lineplot(data=df, palette="tab10", linewidth=2.5, marker='o', color="coral", ax = axs[0], legend='full')
            ax2 = sns.lineplot(data=df2, palette="tab10", linewidth=2.5, marker='o', color="red", ax = axs[1], legend='full')
            ax.set_ylabel('Total Diagnosed')
            ax2.set_ylabel('Total Death')
            ax.set_xlabel('Date (past 30 days)')
            ax.figure.legend(['Total Diagnosed', 'Total Death'])
            fig.autofmt_xdate()
            plt.savefig(f'static/plots/usa.png',bbox_inches = "tight")
            

        print('Graphs Job Completed')

if __name__ == "__main__":
    plot = plotGraphs()
    plot.start()