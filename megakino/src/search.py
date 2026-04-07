import requests
from bs4 import BeautifulSoup
import curses
from .common import BASE_URL


def search_for_movie():
    print("Welcome to Megakino-Downloader!")
    keyword = input("What movie/series do you want to watch/download today? ")
    url = f"{BASE_URL}/index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story={keyword}"

    session = requests.Session()
    try:
        session.get(f"{BASE_URL}/index.php?yg=token", timeout=15)
        response = session.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Unable to fetch the page. Details: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    titles_links = []
    for link in soup.find_all('a', class_='poster'):
        title = link.find('h3', class_='poster__title')
        if title:
            titles_links.append((title.text.strip(), link['href']))

    if not titles_links:
        msg = f"No results found for '{keyword}'."
        raise ValueError(msg)

    def curses_menu(stdscr, titles_links):
        curses.curs_set(0)
        current_row = 0

        while True:
            try:
                stdscr.clear()

                stdscr.addstr(0, 0, "Top 20 Results:", curses.A_BOLD)

                for idx, (title, _) in enumerate(titles_links):
                    if idx == current_row:
                        stdscr.addstr(idx + 2, 0, title.encode("utf-8"), curses.color_pair(1))
                    else:
                        stdscr.addstr(idx + 2, 0, title.encode("utf-8"))

                stdscr.refresh()

                key = stdscr.getch()

                if key == curses.KEY_UP and current_row > 0:
                    current_row -= 1
                elif key == curses.KEY_DOWN and current_row < len(titles_links) - 1:
                    current_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    return titles_links[current_row][1]
                elif key == 27:
                    return None
            except Exception:
                raise ValueError("Please increase terminal size!")

    def main(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        return curses_menu(stdscr, titles_links)

    selected_link = curses.wrapper(main)
    return selected_link


if __name__ == "__main__":
    movie_link = search_for_movie()
    if movie_link:
        print(f"Selected Link: {movie_link}")
    else:
        print("No movie selected or an error occurred.")
