import requests

def get_user_reviews(url):
    """
    Given the url of the first page of a user's profile, retrieve all of their reviews

    Example of a user's URL: http://www.yelp.com/user_details?userid=43QXqwA8KBIb_m7IBtoEgQ (me)
    """

    # Access the first page, to see if it's ok
    response = requests.get(url)
    if not response.ok:
        raise YelpProfilePageError('URL returned a non-ok response')
    res = response.content

    page_has_reviews = check_current_profile_page_for_reviews(res)
    if page_has_reviews:
        YelpProfileReader(res)
        pass
        # Send first page to scraper

    # Paginate, send second page to scraper


def check_current_profile_page_for_reviews(res_html):
    """
    Given a url for a page of somebody's profile, checks to see if there are reviews there
    """
    return True


class YelpProfileReader(object):
    pass


class YelpProfilePageError(Exception):
    pass
