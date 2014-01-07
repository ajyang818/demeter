from bs4 import BeautifulSoup
from lxml import etree
import requests
from StringIO import StringIO

parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False, ns_clean=True, encoding='utf-8', recover=True)


def get_user_reviews(url):
    """
    Given the url of the first page of a user's profile, retrieve all of their reviews

    Example of a user's URL (mine): http://www.yelp.com/user_details?userid=43QXqwA8KBIb_m7IBtoEgQ
    """

    reader = YelpProfileReader(url)
    reader.initiate()


class YelpProfileReader(object):

    def __init__(self, url):
        self.url = url

    def initiate(self):
        response = requests.get(url)
        if not response.ok:
            raise YelpProfilePageError('URL returned a non-ok response')
        res = response.content

        soup = BeautifulSoup(res)

        reviews = self.get_reviews_on_page(soup)

        if not reviews:
            raise YelpProfilePageError('No reviews found on the first page for this user')

        for review in reviews:
            self.parse_individual_review(review)

    def get_reviews_on_page(self, soup):
        return soup.find_all('div', 'review clearfix')

    def parse_individual_review(self, review):
        """
        Goal: dictionary per deal = {
            business_name: '',
            categories: [],
            neighborhood: '',
            review_date: '',
            stars: int,
            review: '',

            review_id: hash,
            business_link: url
        }
        """
        return



class YelpProfilePageError(Exception):
    pass
