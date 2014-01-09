from bs4 import BeautifulSoup
from lxml import etree
import re
import requests
from StringIO import StringIO

parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False, ns_clean=True, encoding='utf-8', recover=True)


def get_user_reviews(url):
    """
    Given the url of the first page of a user's profile, retrieve all of their reviews

    Example of a user's URL (mine): http://www.yelp.com/user_details?userid=43QXqwA8KBIb_m7IBtoEgQ
    """

    harvester = YelpProfileHarvester(url)
    harvester.initiate()


class YelpProfileHarvester(object):

    def __init__(self, url):
        self.url = url

    def initiate(self):
        response = requests.get(self.url)
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
            address: '',
            categories: [],
            neighborhood: '',
            review_date: '',
            stars: int,
            review: '',

            review_id: hash,
            business_link: url
        }
        """
        business_name_block = review.h4
        business_name = self._get_first_stripped_string(business_name_block)

        address_block = review.find('address')
        address = self._get_concatenated_string_from_stripped_strings(address_block)

        categories_neighborhood_block = review.find('p', 'smaller nobtm')
        categories = self._get_category_list(categories_neighborhood_block)
        neighborhood = self._get_neighborhod(categories_neighborhood_block)

        review_date_block = review.find('span', 'smaller date')
        stars_block = review.img  # stars_block.get('alt')
        review_block = review.find('div', 'review_comment')
        review_id_block = review.find('div', 'rateReview')
        business_link_block = review.a

        return

    def _get_first_stripped_string(self, html_block):
        return html_block.get_text(strip=True)

    def _get_concatenated_string_from_stripped_strings(self, html_block, delimiter='|'):
        strings = [string for string in html_block.stripped_strings]
        return delimiter.join(strings)

    def _get_category_list(self, html_block):
        return [string.get_text(strip=True) for string in html_block.find_all('a')]

    def _get_neighborhod(self, html_block):
        neighborhood_string = html_block.find(text=re.compile("Neighborhood"))
        if not neighborhood_string:
            return None
        NEIGHBORHOOD = 'Neighborhood: '
        return neighborhood_string[NEIGHBORHOOD:]


class YelpProfilePageError(Exception):
    pass
