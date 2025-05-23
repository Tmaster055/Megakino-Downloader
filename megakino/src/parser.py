import argparse
import pathlib

DEFAULT_DOWNLOAD_PATH = pathlib.Path.home() / "Downloads"

parser = argparse.ArgumentParser(
    description="Megakino Downloader Arguments"
)

parser.add_argument(
    "--path",
    type=str,
    default=DEFAULT_DOWNLOAD_PATH,
    help="Pick a folder were to save your movies/series"
)

args = parser.parse_args()
