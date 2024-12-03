import pathlib
import subprocess


DEFAULT_DOWNLOAD_PATH = pathlib.Path.home() / "Downloads"

def download(direct_links):
    counter = 1
    for link in direct_links:
        output_file = fr"{DEFAULT_DOWNLOAD_PATH}//File {counter}"
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
        print(link)
        subprocess.run(command)
