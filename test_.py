import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

class newsScrapper():

    def __init__(self):
        self.success = 0

    def start(self):
        url = 'https://www.moh.gov.sg/covid-19'
        response = get(url)
        print(response.status_code)

        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.findAll('table')[2].findAll('tr')

        for i, news in enumerate(a[1:]):
            dict = {
                    'news_date' : datetime.strptime(news.findAll('td')[0].getText().replace('\xa0', ' '), '%d %b %Y').date(),
                    'news_title' : news.findAll('td')[1].getText().replace('\xa0',' '),
                    'news_link' : news.findAll('a', href=True)[0]['href']
                    }
            print(dict)
            

if __name__ == "__main__":
    ns = newsScrapper()
    ns.start()