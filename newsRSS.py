"""Fetch news articles from Kurdistan24 RSS feeds and print the title, date
and image of each item."""

import bs4
import feedparser
import requests

BASE_URL = "https://www.kurdistan24.net"
RSS_PAGE_URL = BASE_URL + "/so/rsspage"
TITLE_SELECTOR = (
    "div#PrintArea.col-xs-12.no-padding.news-reader.bg-white.no-gutter h1"
)


def main():
    session = requests.Session()
    rss_page = session.get(RSS_PAGE_URL)
    if rss_page.status_code != 200:
        print(
            f"RSS page not loaded, response {rss_page.status_code}; "
            "check the connection and try again"
        )
        return

    soup = bs4.BeautifulSoup(rss_page.content, "lxml")
    for link in soup.find_all("div", class_="rsslink"):
        feed = feedparser.parse(BASE_URL + link.a["href"])
        for item in feed.entries:
            article = session.get(item.link)
            if article.status_code != 200:
                print(
                    f"Article not loaded, response {article.status_code}; "
                    "skipping"
                )
                continue
            article_soup = bs4.BeautifulSoup(article.content, "lxml")
            title = article_soup.select(TITLE_SELECTOR)
            if not title:
                continue
            print(title[0].text)
            date = article_soup.find("span", class_="registerdate")
            if date:
                print(f"Date added: {date.text}")
            image = article_soup.find("img", id="img-responsive")
            if image:
                print(image["src"])


if __name__ == "__main__":
    main()
