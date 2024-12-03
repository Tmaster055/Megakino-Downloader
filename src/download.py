import pathlib
import subprocess


DEFAULT_DOWNLOAD_PATH = pathlib.Path.home() / "Downloads"

def download(direct_links, titles):
    counter = 0
    for link in direct_links:
        title = titles[counter].split('(')[0].strip()
        output_file = fr"{DEFAULT_DOWNLOAD_PATH}//{title}"
        print(output_file)
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
