import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import seaborn as sns
from chatbot_app.models import graphPlot
from django.core.files.images import ImageFile
import io

class Gen_graph():
    
    def __init__(self):
        self.status_success = 0

    def plot_it(self, countries = ['China','France','Germany', 'Italy','Malaysia','Singapore','Spain']):
        #countries = ['China','France','Germany', 'Iran', 'Italy','Malaysia','Philippines','Singapore','Spain','United Kingdom']
        #plot individual country charts
        inf_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        inf_link_us = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"

        inf_global = pd.read_csv(inf_link)
        inf_us = pd.read_csv(inf_link_us)

        inf_us = pd.concat([inf_us.iloc[:,6:8], inf_us.iloc[:,-30:]],axis=1)
        inf_global = pd.concat([inf_global.iloc[:,0:2],inf_global.iloc[:,-30:]],axis=1)
        inf_us_grp = inf_us.groupby(by='Country_Region').sum().T
        inf_global_grp = inf_global.groupby(by='Country/Region').sum().T

        dead_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        dead_link_us = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

        dead_global = pd.read_csv(dead_link)
        dead_us = pd.read_csv(dead_link_us)

        dead_us = pd.concat([dead_us.iloc[:,6:8], dead_us.iloc[:,-30:]],axis=1)
        dead_global = pd.concat([dead_global.iloc[:,0:2],dead_global.iloc[:,-30:]],axis=1)
        dead_us_grp = dead_us.groupby(by='Country_Region').sum().T
        dead_global_grp = dead_global.groupby(by='Country/Region').sum().T

        sns.set(style="whitegrid")
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12,6), sharex=True)
        for i in countries:
            df = inf_global_grp[i]
            df.index = pd.to_datetime(df.index)
            df2 = dead_global_grp[i]
            df2.index = pd.to_datetime(df.index)
            fig.suptitle(f'Total Confirmed Cases in {i} for Past 30 Days', fontsize= 18)
            ax = sns.lineplot(data=df, palette="tab10", linewidth=2.5, marker='o', color="coral", ax = axs[0], legend='full')
            ax2 = sns.lineplot(data=df2, palette="tab10", linewidth=2.5, marker='o', color="red", ax = axs[1], legend='full')
            ax.set_ylabel('Total Diagnosed')
            ax2.set_ylabel('Total Death')
            ax.figure.legend(['Total Diagnosed', 'Total Death'])
            ax.set_xlim(df.index[0],df.index[-1])
            xfmt = mdates.DateFormatter('%d-%m')
            ax.xaxis.set_major_formatter(xfmt)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            for tick in ax2.get_xticklabels():
                tick.set_rotation(45)
                tick.set_horizontalalignment("center")
            figure = io.BytesIO()
            plt.savefig(figure, format = 'png',bbox_inches = "tight")
            image = ImageFile(figure)
            plot_instance = graphPlot(name = f'{i.lower()}.png')
            plot_instance.plot.save(f'{i.lower()}.png', image)
            print(f'Plotted {i}')
            ax.cla()
            ax2.cla()

        # US ONLY
        df = inf_us_grp['US']
        df.index = pd.to_datetime(df.index)
        df2 = dead_us_grp['US']
        df2.index = pd.to_datetime(df.index)
        fig.suptitle(f'Total Confirmed Cases in USA for Past 30 Days', fontsize= 18)
        ax = sns.lineplot(data=df, palette="tab10", linewidth=2.5, marker='o', color="coral", ax = axs[0], legend='full')
        ax2 = sns.lineplot(data=df2, palette="tab10", linewidth=2.5, marker='o', color="red", ax = axs[1], legend='full')
        ax.set_ylabel('Total Diagnosed')
        ax2.set_ylabel('Total Death')
        ax.figure.legend(['Total Diagnosed', 'Total Death'])
        ax.set_xlim(df.index[0],df.index[-1])
        xfmt = mdates.DateFormatter('%d-%m')
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        for tick in ax2.get_xticklabels():
            tick.set_rotation(45)
            tick.set_horizontalalignment("center")
        figure = io.BytesIO()
        plt.savefig(figure, format = 'png',bbox_inches = "tight")
        image = ImageFile(figure)
        plot_instance = graphPlot(name = 'usa.png')
        plot_instance.plot.save('usa.png', image)
        print('Plotted usa')
        
        self.status_success = 1
        return print('Daily Graph plots done')


if __name__ == "__main__":
    gg = gen_graph()
    gg.plot_it()