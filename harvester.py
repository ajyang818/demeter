from bs4 import BeautifulSoup
import csv
import re
import requests
import string
import unicodedata


def get_user_reviews(url):
    """
    Given the url of the first page of a user's profile, retrieve all of their reviews

    Example of a user's URL (mine): http://www.yelp.com/user_details?userid=43QXqwA8KBIb_m7IBtoEgQ
    """

    harvester = YelpProfileHarvester(url)
    harvester.initiate()


class YelpProfileHarvester(object):

    DEFAULT_EXCEL_OUTPUT_FILE = 'test_output.csv'

    def __init__(self, url, excel_output=False, clear=False):
        self.url = url
        self.excel_output = excel_output
        if clear:
            clearing_file = open(self.DEFAULT_EXCEL_OUTPUT_FILE, "w+")
            clearing_file.close()
        if excel_output:
            self.file = open(self.DEFAULT_EXCEL_OUTPUT_FILE, 'a')
            self.writer = csv.writer(self.file)

    def initiate(self):

        parsed_reviews = []
        review_counter = 0

        while True:  # This is probably not good
            paged_url = "{}&rec_pagestart={}&review_sort=time".format(self.url, review_counter)
            reviews, has_reviews = self._get_reviews_from_url(paged_url)
            if not has_reviews:
                if review_counter == 0:
                    raise YelpProfilePageError('No reviews found on first page for this user')
                break
            for review in reviews:
                parsed_review = self.parse_individual_review(review)
                if self.excel_output == True:
                    self._output_to_excel(parsed_review)
                parsed_reviews.append(parsed_review)
            review_counter += 10

        if self.excel_output:
            self.file.close()

        return parsed_reviews

    ######################################################
    # "Getting" methods

    def _get_reviews_from_url(self, url):
        response = requests.get(url)
        if not response.ok:
            raise YelpProfilePageError('URL returned a non-ok response')
        res = response.content

        soup = BeautifulSoup(res)
        reviews = self.get_reviews_on_page(soup)
        return reviews, bool(len(reviews))

    def get_reviews_on_page(self, soup):
        return soup.find_all('div', 'review clearfix')

    ######################################################
    # "Outputting" methods

    def _output_to_excel(self, parsed_review):
        self.writer.writerow([
            parsed_review['review_date'],
            parsed_review['business_name'],
            parsed_review['review_id'],
            parsed_review['stars'],
            parsed_review['address'],
            parsed_review['neighborhood'],
            parsed_review['categories'],
            parsed_review['business_link'],
            parsed_review['review'],
        ])

    ######################################################
    # Individual Review Parser Methods

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
        raw_business_name = self._get_first_stripped_string(business_name_block)
        indiv_review_data['business_name'] = clean_weird_characters(raw_business_name)

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
        review_text = self._get_first_stripped_string(review_block)
        indiv_review_data['review'] = clean_weird_characters(review_text)

        review_id_block = review.find('div', 'rateReview')
        indiv_review_data['review_id'] = self._get_block_attribute(review_id_block, 'data-review-id', 0)

        business_link_block = review.a
        indiv_review_data['business_link'] = self._get_block_attribute(business_link_block, 'href', trun_char='#')

        return indiv_review_data

    def _get_first_stripped_string(self, html_block):
        return html_block.get_text(strip=True)

    def _get_concatenated_string_from_stripped_strings(self, html_block, delimiter='|'):
        strings = [clean_string for clean_string in html_block.stripped_strings]
        return delimiter.join(strings)

    def _get_category_list(self, html_block):
        return [dirty_string.get_text(strip=True) for dirty_string in html_block.find_all('a')]

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


# Shamelessly taken from StackOverflow
def clean_weird_characters(messy_string):
   intermediate_string = ''.join((ch for ch in unicodedata.normalize('NFD', unicode(messy_string)) if unicodedata.category(ch) != 'Mn'))
   return filter(lambda ch: ch in string.printable, intermediate_string)


class YelpProfilePageError(Exception):
    pass
