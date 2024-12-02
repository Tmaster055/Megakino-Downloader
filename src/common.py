import os
import platform
import shutil
import subprocess

import requests

from bs4 import BeautifulSoup
from search import search_for_movie


def get_html_from_search():
    url = search_for_movie()
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_episodes(soup):
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

def clear() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_windows_cmd(msg):
    command = f"""cmd /c echo {msg.replace('"', "'")} """
    subprocess.run(command)


def find_program(program_name: str, fallback_path: str) -> str:
    program_path = shutil.which(program_name)

    if program_path:
        return program_path

    if platform.system() == "Windows" and program_name.lower() == "syncplayconsole":
        fallback_program_path = os.path.join(fallback_path, "syncplay")
    else:
        fallback_program_path = os.path.join(fallback_path, program_name.lower())

    #if os.path.isfile(fallback_program_path):
    return fallback_program_path