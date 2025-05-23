import os
import pathlib
import subprocess

DEFAULT_DOWNLOAD_PATH = pathlib.Path.home() / "Downloads"


def download(direct_links, titles):
    counter = 0
    for link in direct_links:
        title = titles[counter]
        output_file = os.path.join(DEFAULT_DOWNLOAD_PATH, title, f"{title}.mp4")
        counter += 1
        command = [
            "yt-dlp",
            "--fragment-retries", "infinite",
            "--concurrent-fragments", "4",
            "-o", output_file,
            "--quiet",
            "--no-warnings",
            link,
            "--progress"
        ]
        subprocess.run(command)
