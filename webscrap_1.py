import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

class Webscrapper():

    def __init__(self):
        self.headline = None 
        self.link = None
        self.checkFile()

    def start(self):
        url = 'https://www.moh.gov.sg/covid-19'
        response = requests.get(url)
        print (response)

        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.findAll('a')
        #for i in a:
        #    print(str(i)+'\n')

        
        for tag in soup.findAll('a')[52:64]:
            print(tag)
            print (tag.string)        
            print (type(tag.string))
            self.link = tag['href']
            if (self.link[0] == '/'):
                self.link = 'https://www.moh.gov.sg' + self.link 
        #    dl_url = 'http://web.mta.info/developers/'+ link
            self.headline = tag.string
            if (tag.string == None):
                self.headline = tag.span.string
            if (tag.string == ""):
                self.headline = tag['title']
            #urllib.request.urlretrieve(link, './webpages/covid19_latest_news_'+ str(i) + '.html')
            self.write()
            print('\n')
            
        #    time.sleep(1)
    def checkFile(self):
        if os.path.exists("HeadlinesWithLinks.txt"):
            os.remove("HeadlinesWithLinks.txt")

    def write(self):
        f = open("HeadlinesWithLinks.txt", "a")
        str = self.headline + '\n' + self.link + '\n\n' 
        f.write(str)
        f.close()

if __name__ == "__main__":
    ws = Webscrapper()
    ws.start()