import string
from random import choice

from url_shortcutter.settings import DOMAIN_NAME

SYMBOLS = string.ascii_letters + string.digits


def symbol_generator():
    n = 0
    while n < 6:
        yield choice(SYMBOLS)
        n += 1


def get_short_url():
    short_code = ""
    for item in symbol_generator():
        short_code = short_code + item

    return DOMAIN_NAME + short_code
