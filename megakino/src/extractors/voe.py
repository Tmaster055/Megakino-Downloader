import re
import base64
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import requests
from bs4 import BeautifulSoup

from megakino.src.common import USER_AGENT


def shift_letters(input_str):
    result = ''
    for c in input_str:
        code = ord(c)
        if 65 <= code <= 90:
            code = (code - 65 + 13) % 26 + 65
        elif 97 <= code <= 122:
            code = (code - 97 + 13) % 26 + 97
        result += chr(code)
    return result


def replace_junk(input_str):
    junk_parts = ['@$', '^^', '~@', '%?', '*~', '!!', '#&']
    for part in junk_parts:
        input_str = re.sub(re.escape(part), '_', input_str)
    return input_str


def shift_back(s, n):
    return ''.join(chr(ord(c) - n) for c in s)


def decode_voe_string(encoded):
    step1 = shift_letters(encoded)
    step2 = replace_junk(step1).replace('_', '')
    step3 = base64.b64decode(step2).decode()
    step4 = shift_back(step3, 3)
    step5 = base64.b64decode(step4[::-1]).decode()
    return json.loads(step5)


def extract_voe_from_script(html):
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", type="application/json")
    return decode_voe_string(script.text[2:-2])["source"]


def voe_get_direct_link(link: str) -> str:
    response = requests.get(
        link,
        headers={'User-Agent': USER_AGENT},
        timeout=30
    )

    redirect = re.search(r"https?://[^'\"<>]+", response.text)
    if not redirect:
        raise ValueError("No redirect found.")

    redirect_url = redirect.group(0)

    try:
        with urlopen(
            Request(
                redirect_url,
                headers={'User-Agent': USER_AGENT}
            ),
            timeout=30
        ) as resp:
            html = resp.read().decode()
    except (HTTPError, URLError, TimeoutError) as err:
        raise ValueError(f"Redirect failed: {err}") from err

    extracted = extract_voe_from_script(html)
    if extracted:
        return extracted

    b64match = re.search(r"var a168c='([^']+)'", html)
    if b64match:
        decoded = base64.b64decode(b64match.group(1)).decode()[::-1]
        return json.loads(decoded)["source"]

    hls = re.search(r"'hls': '(?P<hls>[^']+)'", html)
    if hls:
        return base64.b64decode(hls.group("hls")).decode()


if __name__ == '__main__':
    link = input("Enter VOE Link: ")
    print(voe_get_direct_link(link))
