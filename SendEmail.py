import requests
import time
from bs4 import BeautifulSoup
import datetime
from nytimesarticle import articleAPI
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Links you can use:
# https://www.nytimes.com/
# https://news.ycombinator.com/

class NewsWebScraper:

    #defining initial self terms
    def __init__(self, keywords, newsSources):
        self.hasArticles = False
        self.news_sources = newsSources
        self.markup = []
        self.keywords = keywords

    def parse(self):
        #for the number of news sources you have loop through them
        for i in range(len(self.news_sources)):
            if self.news_sources[i] == 'NewsYCombinator':
                #access the website and find all the stories on the front page
                self.markup.append(requests.get('https://news.ycombinator.com/').text)
                soup = BeautifulSoup(self.markup[i], 'html.parser')
                links = soup.findAll("a", {"class": "storylink"})
                self.saved_links = []
                #search all stories on front page to find out whether or not your key words are there
                for link in links:
                    for keyword in self.keywords:
                        if keyword in link.text:
                            self.saved_links.append(link)

                #get all of the links and save them, then declare that articles have been found
                self.read_links = []
                for a in range(len(self.saved_links)):
                    self.read_links.append(str(self.saved_links[a]['href']))
                    self.hasArticles = True
            elif self.news_sources[i] == 'NewYorkTimes':
                #To get your api key go to nyt developers website create an account and create an app, then select search api and copy your key from there
                api = articleAPI('Your API Key')
                #loop through all key words to find out whether or not articles have them
                for a in range(len(self.keywords)):
                    articles = api.search( q = self.keywords[a], begin_date = datetime.datetime.now().year * 10000 + (datetime.datetime.now().month - 1) * 100 + datetime.datetime.now().day, page=1 )
                    self.list_of_articles = []
                    for docs in articles['response']['docs']:
                        article_blurbs = {}
                        article_blurbs = docs.get('headline').get('main') + '\n' + docs.get('web_url') + '\n' + docs.get('snippet')
                        self.list_of_articles.append(str(article_blurbs))
                #if has an article, declare articles have been found
                if len(self.list_of_articles) > 0:
                    self.hasArticles = True

    def email(self):
        #Setting up the email itself: where from, where to, and the subject
        from_address = 'from_email'
        to_address = 'to_email'
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = 'Daily News'

        #If newsycombinator is chosen as one of the news networks this is where all of its links are stored
        links = self.read_links
        if (self.hasArticles):
            for i in range(len(self.news_sources)):
                #sending email from newsycombinator
                if self.news_sources[i] == 'NewsYCombinator':
                    body = 'These are some news links that we found from NewsYCombinator that you might like on ' + str(self.keywords) + ':\n\n' + '\n\n'.join(links)
                    msg.attach(MIMEText(body, 'plain'))
                #sending email from nyt
                if self.news_sources[i] == 'NewYorkTimes':
                    body2 = '\n\n These are some news links that we found from The New York Times that you might like on ' + str(self.keywords) + ':\n\n' + str("\n\n".join(self.list_of_articles))
                    msg.attach(MIMEText(body2, 'plain'))
        else:
            #if nothing is found on the subject/keywords on either news network this will be displayed
            body = 'Unfortunately there were no articles from ' + str(self.news_sources) + " discussing " + ', '.join(self.keywords)
            msg.attach(MIMEText(body, 'plain'))

        #Enter from email and password (also make sure to allow unauthorized third parties to acces the gmail so the script will work. So don't use an important email!)
        email = "email"
        password = "password"

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(email, password)
        text = msg.as_string()
        mail.sendmail(from_address, to_address, text)
        mail.quit()

#If it's 7 am send email
if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == 0 and datetime.datetime.now().second == 0:
    news_sources = ['NewsYCombinator', 'NewYorkTimes']
    news_keywords = ['Biotech','Python']
    n = NewsWebScraper(news_keywords, news_sources)
    n.parse()
    n.email()
    time.sleep(1)