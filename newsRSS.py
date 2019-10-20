import feedparser
import requests
import bs4
import urllib.parse

websiteURL = "https://www.kurdistan24.net/so/rsspage"
pageRSS = requests.get(websiteURL)
soupContent = bs4.BeautifulSoup(pageRSS.content, "lxml")
soupLinks = soupContent.find('div', class_='rsslink')
print(soupLinks.a['href'])


newsFeed = feedparser.parse("https://www.kurdistan24.net/page/RSS/97.xml")


for newsItem in newsFeed.entries:
    print(newsItem.link)
