import os
import platform
import subprocess
import re

import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

REDIRECT_PATTERN = re.compile(r"window\.location\.href\s*=\s*'(https://[^/]+/e/\w+)';")


def get_latest_domain():
    response = requests.get("https://raw.githubusercontent.com/Yezun-hikari/new-domain-check/refs/heads/main/monitors/megakino/domain.txt", timeout=15)
    response.raise_for_status()
    return f"https://{response.text.strip()}"

BASE_URL = get_latest_domain()


def get_html_from_search():
    from .search import search_for_movie
    url = search_for_movie()
    session = requests.Session()
    try:
        session.get(f"{BASE_URL}/index.php?yg=token", timeout=15)
        response = session.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Unable to fetch the page. Details: {e}")
        return None
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


USER_AGENT = UserAgent().random
