import os
import subprocess

from megakino.src.parser import args
from megakino.src.common import USER_AGENT


def download(direct_links, titles):
    counter = 0
    for link in direct_links:
        title = titles[counter]
        output_file = os.path.join(args.path, title, f"{title}.mp4")
        counter += 1
        command = [
            "yt-dlp",
            "--fragment-retries", "infinite",
            "--concurrent-fragments", "4",
            "--user-agent", USER_AGENT,
            "-o", output_file,
            "--quiet",
            "--no-warnings",
            link,
            "--progress"
        ]
        subprocess.run(command)
