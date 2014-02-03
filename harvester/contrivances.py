from bs4 import BeautifulSoup
from collections import defaultdict
from django.conf import settings
import oauth2
import requests
import string
import unicodedata


# Shamelessly taken from StackOverflow
def clean_weird_characters(messy_string):
   intermediate_string = ''.join((ch for ch in unicodedata.normalize('NFD', unicode(messy_string)) if unicodedata.category(ch) != 'Mn'))
   return filter(lambda ch: ch in string.printable, intermediate_string)


def yelp_oauth(url_piece, api_version=2):
    key = settings.YELP_KEY
    secret = settings.YELP_SECRET
    token = settings.YELP_TOKEN
    token_secret = settings.YELP_TOKEN_SECRET

    YELP_API_URL_BASE = 'http://api.yelp.com/v2/'

    url = YELP_API_URL_BASE + url_piece

    consumer = oauth2.Consumer(key, secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                      'oauth_timestamp': oauth2.generate_timestamp(),
                      'oauth_token': token,
                      'oauth_consumer_key': key})
    token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    return signed_url


def pull_yelp_categories():
    categories_url = 'http://www.yelp.com/developers/documentation/category_list'
    response = requests.get(categories_url)
    if not response.ok:
        raise ValidationError("Error getting Yelp categories URL")

    res = response.content
    soup = BeautifulSoup(res)

    categories = soup.find('ul', 'attr-list')
    yelp_category_nester(categories)

    return


def yelp_category_nester(soupobj):
    import ipdb; ipdb.set_trace();
    nested_tree = defaultdict(list)
    for child in soupobj.children:
        if child.name == 'li':
            # Child is a 'parent'
            nested_tree[child.name] = None
        elif child.name == 'ul':
            if child.findChildren('li'):
                child_dict = yelp_category_nester(child)
                nested_tree[parent_category].append(child_dict)
            nested_tree[parent_category].append(yelp_category_nester(child))
        else:
            continue
