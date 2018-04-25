from sgmon.log import get_logger

import requests
from requests.exceptions import RequestException

logger = get_logger(__name__)


class HTTPClientError(Exception):
    pass


def handle_exception(func):
    """
    Decorator to catch exception
    """
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestException as err:
            raise HTTPClientError("Exception into {}(): {}".format(
                func.__name__, err))

    return wrapped


class HTTPClient(object):

    def __init__(self, url):
        self.url = url
        self.ses = requests.Session()

    def set_headers(self, headers):
        self.ses.headers.update(headers)

    def has_failed(self, response):
        status_code = str(response.status_code)
        return status_code.startswith('4') or \
            status_code.startswith('5')

    @handle_exception
    def get(self):
        response = self.ses.get(self.url)
        if response.status_code != 200:
            return []

        logger.info("Get success: {}".format(response))

        return response.json()

    @handle_exception
    def post(self, data):
        response = self.ses.post(self.url, data=data)
        if self.has_failed(response):
            logger.error("Post failed: %s", response)
            response.raise_for_status()

        return response.text
