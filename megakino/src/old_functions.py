from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import requests
import logging
import re
from base64 import b64decode
from bs4 import BeautifulSoup

from .common import USER_AGENT

REDIRECT_PATTERN = re.compile(r"window\.location\.href\s*=\s*'(https://[^/]+/e/\w+)';")
EXTRACT_VEO_HLS_PATTERN = re.compile(r"'hls': '(?P<hls>.*)'")

# Developer Note: I changed this tool a lot because of the lacking voe support and very bad scripting
# To review the old mechanics for future implementation, see commit "Removed VOE support and made big changes"


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

def get_titles(voe_links):
    titles = []
    for link in voe_links:
        soup = BeautifulSoup(requests.get(link).content, 'html.parser')
        redirect_match = REDIRECT_PATTERN.search(str(soup.prettify))
        redirect_url = redirect_match.group(1)
        print(redirect_url)

        response = requests.get(redirect_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        og_title_tag = soup.find('meta', attrs={'name': 'og:title'})
        og_title = og_title_tag['content']
        if og_title:
            titles.append(og_title)
        else:
            titles.append("Title not found!")
    return titles


def get_voe_episodes(soup):
    select_tags = soup.find_all('select', class_='mr-select')
    episode_links = [select.find('option')['value'] for select in select_tags]
    if episode_links:
        return episode_links

    voe_links = []
    for iframe in soup.find_all('iframe', attrs={'data-src': True}):
        data_src = iframe['data-src']
        if "voe.sx" in data_src:
            voe_links.append(data_src)
            return voe_links
