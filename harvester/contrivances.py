from django.conf import settings
import oauth2
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
