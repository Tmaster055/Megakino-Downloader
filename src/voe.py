from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import requests
import logging
import re
from base64 import b64decode
from bs4 import BeautifulSoup

from common import USER_AGENT

REDIRECT_PATTERN = re.compile(r"window\.location\.href\s*=\s*'(https://[^/]+/e/\w+)';")
EXTRACT_VEO_HLS_PATTERN = re.compile(r"'hls': '(?P<hls>.*)'")


def voe_get_direct_link(link):
    response = requests.get(link, timeout=15, headers = {
    "User-Agent": USER_AGENT})
    soup = BeautifulSoup(response.content, 'html.parser')
    redirect_match = REDIRECT_PATTERN.search(str(soup.prettify))
    if not redirect_match:
        logging.warning("No redirect link found.")
        return None

    redirect_url = redirect_match.group(1)
    try:
        with urlopen(
            Request(
                redirect_url
            ),
            timeout=10
        ) as response:
            redirect_content = response.read()
        redirect_content_str = redirect_content.decode('utf-8')
    except (HTTPError, URLError, TimeoutError) as e:
        return None

    hls_match = EXTRACT_VEO_HLS_PATTERN.search(redirect_content_str)
    if not hls_match:
        logging.warning("No HLS link found.")
        return None

    hls_link = b64decode(hls_match.group("hls")).decode()
    return hls_link
