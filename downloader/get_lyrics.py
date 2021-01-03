from logging import Logger
from typing import Union

import requests
from bs4 import BeautifulSoup


class GetLyrics:
    def __init__(self, lyrics_root_url: str, log: Logger):
        self.lyrics_root_url = lyrics_root_url
        self.log = log

    def get_lyrics(self, lyrics_url: str) -> Union[str, None]:
        url = f"{self.lyrics_root_url}/{lyrics_url}"
        self.log.info(f"Getting lyrics from {url}...")
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        all_divs = soup.select("div")

        for div in all_divs:
            if (
                " Usage of azlyrics.com content by any third-party lyrics provider "
                "is prohibited by our licensing agreement. Sorry about that. "
                in div.contents
            ):
                return div.text

        return None
