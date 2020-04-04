import sys
import django
import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'ChatBot_Main.settings')
# setting can be found in wsgi.py folder in pycache
os.environ['DJANGO_SETTINGS_MODULE'] = 'ChatBot_Main.settings'
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines, hospitalList
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

#### FOR GLOBAL STATUS - FOR INFECTION STATUS INTENT ####

class statusScrapper():
    
    def __init__(self):
        self.status_success = 0
        self.update_success = 0

    def start(self):
        globalLastUpdate.objects.all().delete()
        globalStatus.objects.all().delete()

        url = 'https://www.worldometers.info/coronavirus/'
        html_soup = get(url)
        print("Worldometer website response stataus: ",html_soup.status_code)
        html_soup = BeautifulSoup(html_soup.text, 'html.parser')
        LastUpdatetext = html_soup.find('div', class_='content-inner').find_all('div')[1].getText()
        table_rows = html_soup.find('table').find_all('tr')

        res = []
        for tr in table_rows[1:]:
            td = tr.find_all('td')
            row = []
            for i in td:
                val = i.text.strip().replace('+', '').replace(',', '').replace(' *','').lower() if i.text.strip() != "" else 0
                try:
                    val = int(val)
                except:
                    val = val
                row.append(val)
            res.append(row)

        col = ['country', 'diagnosed', 'new_cases', 'death',
            'new_death', 'discharged', 'active', 'critical','nonsense1','nonsense2','nonsense3','nonsense4']
        pd_table = pd.DataFrame(res, columns=col)
        global_dict = pd_table.to_dict('records')
        model_instance = [globalStatus(country=i['country'], diagnosed=i['diagnosed'], new_cases=i['new_cases'], death=i['death'], new_death=i['new_death'], discharged=i['discharged'], critical=i['critical'], active=i['active']) for i in global_dict]

        # Plot Charts
        pd_table['death_rate'] = pd_table['death']*100/pd_table['diagnosed']
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10,6), sharex=True)
        fig.suptitle(f'Infected & Death Cases Trend of Top 15 Countries as of {LastUpdatetext.split("Last updated: ")[1]}', fontsize= 18)
        pd_table.sort_values(by='diagnosed',ascending=False, inplace=True)
        ax1 = pd_table[2:17].plot.bar(x='country', y='diagnosed', ax = axs[0], fontsize=12, grid=True)
        ax2 = pd_table[2:17].plot.bar(x='country', y='death', ax = axs[1], fontsize=12, cmap = 'autumn', grid=True)
        ax3 = pd_table[2:17].plot.line(x='country', y='death_rate', ax = axs[1], fontsize=12, cmap = 'Dark2_r', grid=True, secondary_y=True, marker = 'o', linewidth=2)
        ax1.set_ylabel('Total Infected')
        ax2.set_ylabel('Total Death')
        ax2.set_xlabel('Countries')
        ax3.set_ylabel('Death Rate (%)')
        plt.tick_params(labelbottom=True)
        for tick in ax2.get_xticklabels():
            tick.set_rotation(45)
        ax3.set_xlim(-0.5,14.5)
        ax3.set_yticks(np.linspace(ax3.get_yticks()[0], round(ax3.get_yticks()[-1]), 6))
        ax2.set_yticks(np.linspace(ax2.get_yticks()[0], round(ax2.get_yticks()[-1],-3), 6))
        plt.savefig('static/plots/worldwide.png',bbox_inches = "tight")

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

        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12,6), sharex=True)
        for i in inf_global_grp.columns:
            sns.set(style="whitegrid")
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

        try:
            globalStatus.objects.bulk_create(model_instance)
            print('Update globalStatus complete!')
            self.status_success = 1
        except:
            print('Update globalstatus failed. Either something went wrong or data already exist.')

        try:
            globalLastUpdate.objects.create(last_update=LastUpdatetext)
            print('Update globalLastUpdate complete!')
            self.update_success = 1
        except:
            print('Error occurred. Update globalLastUpdate unsuccessful.')


###############

class newsScrapper():

    def __init__(self):
        self.success = 0

    def start(self):
        url = 'https://www.moh.gov.sg/covid-19'
        response = get(url)
        print("MOH website response stataus: ",response.status_code)

        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.findAll('table')[8].findAll('tr')

        for i, news in enumerate(a[1:]):
            dict = {
                    'news_date' : datetime.strptime(news.findAll('td')[0].getText().rstrip().replace('\xa0', ' '), '%d %b %Y').date(),
                    'news_title' : news.findAll('td')[1].getText().replace('\xa0',' '),
                    'news_link' : news.findAll('a', href=True)[0]['href']
                    }
            try:
                MOHHeadlines.objects.create(**dict) #use ** to add dict into models
                print(f'Title {i+1} updated successfully')
                self.success = 1
            except:
                print(f'Title {i+1} failed to update or data already exist')




if __name__ == "__main__":
    ss = statusScrapper()
    ss.start()
    ns = newsScrapper()
    ns.start()