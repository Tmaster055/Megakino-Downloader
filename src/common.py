import os
import platform
import requests

from bs4 import BeautifulSoup
from search import search_for_movie


def get_html_from_search():
    url = search_for_movie()
    html_content = requests.get(url, timeout=15)
    return html_content

def get_episodes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    select_tags = soup.find_all('select', class_='mr-select')
    episode_links = [select.find('option')['value'] for select in select_tags]
    return episode_links

def clear() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")