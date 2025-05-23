import re
import requests

from .common import USER_AGENT

def megakino_get_direct_link(link):
    response = requests.get(link, timeout=15, headers={
        "User-Agent": USER_AGENT})
    uid_match = re.search(r'"uid":"(.*?)"', response.text)
    md5_match = re.search(r'"md5":"(.*?)"', response.text)
    id_match = re.search(r'"id":"(.*?)"', response.text)

    if not all([uid_match, md5_match, id_match]):
        return None

    uid = uid_match.group(1)
    md5 = md5_match.group(1)
    video_id = id_match.group(1)

    stream_link = f"https://watch.gxplayer.xyz/m3u8/{uid}/{md5}/master.txt?s=1&id={video_id}&cache=1"
    return stream_link
