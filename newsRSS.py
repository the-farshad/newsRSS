import feedparser
import requests
import bs4
import urllib.parse

websiteURL = "https://www.kurdistan24.net/so/rsspage"
pageRSS = requests.get(websiteURL)
pageCode = pageRSS.status_code
if (pageCode != 200):
    print(f'RSS file not loaded, Response {pageCode} check connection and try again')
else:
    soupContent = bs4.BeautifulSoup(pageRSS.content, "lxml")
    for soupLinks in soupContent.find_all('div', class_='rsslink'):
        rssLink = soupLinks.a['href']
        newsFeed = feedparser.parse("https://www.kurdistan24.net" + rssLink)
        for newsItem in newsFeed.entries:
            pageGet = requests.get(newsItem.link)
            pageCode = pageRSS.status_code
            print(pageCode)
            if (pageCode != 200):
                print(f'Link file not loaded, Response {pageCode} check connection and try again')
                continue
            soupReady = bs4.BeautifulSoup(pageGet.content, 'lxml')
            titleField = soupReady.select("div#PrintArea.col-xs-12.no-padding.news-reader.bg-white.no-gutter h1")
            print(titleField)
            if (titleField != []):
                print(titleField[0].text)
                dateField = soupReady.find("span" , class_="registerdate")
                print(f"Data added {dateField.text} ")
                imgLink = soupReady.find("img", id="img-responsive")
                print(imgLink["src"])
            break
        break

