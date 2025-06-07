import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
OUTPUT_FILE = Path("movies.txt")

def write_title(title: str):
    """Appends a movie title to the file if it doesn't already exist."""
    existing_titles = []
    if OUTPUT_FILE.exists():
        with OUTPUT_FILE.open("r", encoding="utf-8") as file:
            existing_titles = [line.strip() for line in file]

    if title not in existing_titles:
        with OUTPUT_FILE.open("a", encoding="utf-8") as file:
            file.write(f"{title}\n")
    else:
        print(f"'{title}' is already in the list.")

def get_movie_titles() -> list[str]:
    """Scrapes the movie titles from the archived web page."""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return [h3.get_text(strip=True) for h3 in soup.find_all(name="h3", class_="title")]

def main():
    titles = get_movie_titles()
    for title in reversed(titles):  # Write from #1 to #100
        write_title(title)

if __name__ == "__main__":
    main()
