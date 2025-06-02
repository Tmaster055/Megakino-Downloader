import os
import platform
import random
import subprocess
import re

import requests

from bs4 import BeautifulSoup
from .search import search_for_movie

REDIRECT_PATTERN = re.compile(r"window\.location\.href\s*=\s*'(https://[^/]+/e/\w+)';")


def get_html_from_search():
    url = search_for_movie()
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_megakino_episodes(soup):
    iframe_tag = soup.find('iframe', src=True)
    if iframe_tag:
        return [iframe_tag['src']]
    return None


def get_title(soup):
    episodes = {}
    og_title = soup.find('meta', property='og:title')
    name = og_title['content'] + " -"
    try:
        episode_options = soup.select('.pmovie__series-select select')[0].find_all('option')
    except IndexError:
        for iframe in soup.find_all('iframe', attrs={'data-src': True}):
            data_src = iframe['data-src']
            if "voe.sx" in data_src:
                episodes[og_title['content']] = data_src
                return episodes
        episodes[og_title['content']] = ""
        return episodes


    for option in episode_options:
        ep_id = option['value']
        ep_name = f"{name} {option.text.strip()}"

        link_select = soup.find('select', {'id': ep_id})
        if link_select:
            link_option = link_select.find('option')
            if link_option and link_option.get('value'):
                episodes[ep_name] = link_option['value']

    return episodes


def clear() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_windows_cmd(msg):
    command = f"""cmd /c echo {msg.replace('"', "'")} """
    subprocess.run(command)


AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) "
    "Gecko/20100101 Firefox/130.",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) SamsungBrowser/26.0 Chrome/122.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Geck",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Config/91.2.1916.1",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.3",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) "
    "Gecko/20100101 Firefox/128."
]

USER_AGENT = random.choice(AGENTS)
