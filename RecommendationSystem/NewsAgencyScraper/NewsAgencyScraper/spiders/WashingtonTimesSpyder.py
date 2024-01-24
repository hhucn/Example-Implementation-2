import datetime
import logging
from typing import List

from scrapy import Selector
from scrapy.loader import ItemLoader
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from RecommendationSystem.NewsAgencyScraper.NewsAgencyScraper.items import ArticleDataItem

from RecommendationSystem.NewsAgencyScraper.NewsAgencyScraper.spiders.NewsAgenciesSpyder import \
    NewsAgenciesSpyder

from RecommendationSystem.NewsAgencyScraper.NewsAgencyScraper.spiders.spyder_utils import parse_pub_date, \
                                                                                          get_selenium_chrome_driver, \
                                                                                          click_button_to_load_all_comments


class WashingtonTimesSpyder(NewsAgenciesSpyder):
    name = "WashingtonTimesSpyder"
    
    def __init__(self):
        self.news_agency = "WashingtonTimes"
        self.news_agency_url = "https://www.washingtontimes.com"
        self.article_start_page_xpath = "//article/h2/a/@href"
        self.is_relative_urls = True

    def extract_article_data(self, article_data_item: ArticleDataItem, article_selector: Selector) -> ItemLoader:
        logging.info("Parse article response")

        loader: ItemLoader = ItemLoader(item=article_data_item, selector=article_selector)

        title = article_selector.xpath("//h1[@class='page-headline']/text()").get().strip()
        loader.add_value("article_title", title)
        loader.add_value("keywords", self.__parse_keywords(article_data_item["url"][0]))
        pub_date = article_selector.xpath("//meta[@name='cXenseParse:publishtime']/@content").get()
        
        loader.add_value("pub_date", parse_pub_date(pub_date))

        return loader

    def extract_comment_section_data(self, article_data_item, comment_selector: Selector) -> List:
        loader: ItemLoader = ItemLoader(item=article_data_item, selector=comment_selector)

        driver = get_selenium_chrome_driver()
        driver.get(article_data_item["url"][0])
        selector = Selector(text=driver.page_source)

        # Add comments to list and store them in ItemLoader
        comments_url = selector.xpath("//div[@class='so-comments']/iframe/@src").extract()
        comments = []
        if len(comments_url) > 0:
            driver.get(comments_url[0])

            click_button_to_load_all_comments(driver, '//button[contains(@class, "LoadMoreButton")]')

            scrapy_selector = Selector(text=driver.page_source)

            comment_selector = scrapy_selector.xpath(
                "//div[contains(@class, 'CommentsTree__ListWrapLoadStateContainer-sc-psk8fb-3 jNGwKD')]/div")
            comments = self.__extract_comments(comment_selector)

        loader.add_value('comments', comments)

        return loader
    
    @staticmethod
    def __extract_comments(comments_selector: Selector) -> List:
        comments = []
        for comment_selector in comments_selector:
            comment_parts = comment_selector.xpath('div//p[contains(@class, "CommentText")]')
            comment = ""
            for part in comment_parts:
                comment_part = part.xpath('span/text()').get()
                comment = comment + "\n" + comment_part
            up_votes = comment_selector.xpath('div//span[contains(@class, "Text-sc-1jeqstd-0 kQCqRZ")]/text()').get()
            if up_votes is None:
                up_votes = 0
            comments.append([comment, up_votes])
        return comments

    @staticmethod
    def __parse_keywords(url):
        url_parts = url.split("/")
        print(url_parts)
        return url_parts[-2].replace("-", " ")
