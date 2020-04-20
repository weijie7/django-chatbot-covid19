from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines, hospitalList, graphPlot
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from django.core.files.images import ImageFile
import io

#### FOR GLOBAL STATUS - FOR INFECTION STATUS INTENT ####

class Webscrape():
    
    def __init__(self):
        self.status_success = 0
        self.update_success = 0

    def statusScrapper(self):

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
                if val == 'n/a': val = 0
                try:
                    val = int(val)
                except:
                    val = val
                row.append(val)
            res.append(row)

        col = ['country', 'diagnosed', 'new_cases', 'death',
            'new_death', 'discharged', 'active', 'critical']
        pd_table = pd.DataFrame(res).iloc[8:,:8]
        pd_table.columns = col
        pd_table.drop( pd_table[ pd_table['country'] == 'total:' ].index , inplace=True)
        global_dict = pd_table.to_dict('records')
        model_instance = [globalStatus(country=i['country'], diagnosed=i['diagnosed'], new_cases=i['new_cases'], death=i['death'], new_death=i['new_death'], discharged=i['discharged'], critical=i['critical'], active=i['active']) for i in global_dict]

        # Plot Charts
        pd_table['death_rate'] = pd_table['death']*100/pd_table['diagnosed']
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10,6), sharex=True)
        fig.suptitle(f'Infected & Death Cases Trend of Top 15 Countries as of {LastUpdatetext}', fontsize= 18)
        ax1 = pd_table[0:16].plot.bar(x='country', y='diagnosed', ax = axs[0], fontsize=12, grid=True)
        ax2 = pd_table[0:16].plot.bar(x='country', y='death', ax = axs[1], fontsize=12, cmap = 'autumn', grid=True)
        ax3 = pd_table[0:16].plot.line(x='country', y='death_rate', ax = axs[1], fontsize=12, cmap = 'Dark2_r', grid=True, secondary_y=True, marker = 'o', linewidth=2)
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
        #plt.savefig('static/plots/worldwide.png',bbox_inches = "tight")
        figure = io.BytesIO()
        plt.savefig(figure, format = 'png',bbox_inches = "tight")
        image = ImageFile(figure)
        plot_instance = graphPlot(name = 'worldwide.png')
        plot_instance.plot.save('worldwide.png', image)

        print('Graphs Job Completed')

        globalLastUpdate.objects.all().delete()
        globalStatus.objects.all().delete()
        graphPlot.objects.all().delete()
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

    def newsScrapper(self):
        url = 'https://www.moh.gov.sg/covid-19'
        response = get(url)
        print("MOH website response stataus: ",response.status_code)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            a = soup.findAll('table')[12].findAll('tr')

            for i, news in enumerate(a[1:]):
                for fmt in ('%d %b %Y', '%d %B %Y'):
                    try:
                        dict = {
                                'news_date' : datetime.strptime(news.findAll('td')[0].getText().rstrip().replace('\xa0', ' '), fmt).date(),
                                'news_title' : news.findAll('td')[1].getText().replace('\xa0',' '),
                                'news_link' : news.findAll('a', href=True)[0]['href']
                                }
                    except ValueError:
                        pass
                try:
                    MOHHeadlines.objects.create(**dict) #use ** to add dict into models
                    print(f'Title {i+1} updated successfully')
                    self.success = 1
                except:
                    print(f'Title {i+1} failed to update or data already exist')


if __name__ == "__main__":
    ss = Webscrape()
    ss.statusScrapper()
    ss.newsScrapper()