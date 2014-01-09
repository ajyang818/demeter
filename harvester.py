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

        parsed_reviews = []
        for review in reviews:
            parsed_reviews.append(self.parse_individual_review(review))

        return parsed_reviews

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
        indiv_review_data = {}

        business_name_block = review.h4
        indiv_review_data['business_name'] = self._get_first_stripped_string(business_name_block)

        address_block = review.find('address')
        indiv_review_data['address'] = self._get_concatenated_string_from_stripped_strings(address_block)

        categories_neighborhood_block = review.find('p', 'smaller nobtm')
        indiv_review_data['categories'] = self._get_category_list(categories_neighborhood_block)
        indiv_review_data['neighborhood'] = self._get_neighborhod(categories_neighborhood_block)

        review_date_block = review.find('span', 'smaller date')
        indiv_review_data['review_date'] = self._get_first_stripped_string(review_date_block)

        stars_block = review.img  # stars_block.get('alt')
        indiv_review_data['stars'] = self._get_block_attribute(stars_block, 'alt', 0, 3)

        review_block = review.find('div', 'review_comment')
        indiv_review_data['review'] = self._get_first_stripped_string(review_block)

        review_id_block = review.find('div', 'rateReview')
        indiv_review_data['review_id'] = self._get_block_attribute(review_id_block, 'data-review-id', 0)

        business_link_block = review.a
        indiv_review_data['business_link'] = self._get_block_attribute(business_link_block, 'href', trun_char='#')

        return indiv_review_data

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
        temp_string = neighborhood_string[neighborhood_string.find(':') + 2:]
        return temp_string[:-1]

    def _get_block_attribute(self, html_block, attr_name, start_char=0, stop_char=None, trun_char=None):
        star_string = html_block.get(attr_name)
        if trun_char:
            return star_string[:star_string.find(trun_char)]
        if not stop_char:
            return star_string[start_char:]
        else:
            return star_string[start_char:stop_char]




class YelpProfilePageError(Exception):
    pass
