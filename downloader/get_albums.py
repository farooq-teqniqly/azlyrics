from typing import Dict, List, Any, Union

import requests
from logging import Logger

from bs4 import BeautifulSoup, Tag


class GetAlbums:
    def __init__(self, band_url: str, log: Logger):
        if not band_url:
            raise ValueError("band_url not specified.")

        if not log:
            raise ValueError("log not specified.")

        self.log = log
        self.log.info(f"Retrieving {band_url}...")
        self.soup = BeautifulSoup(requests.get(band_url).text, "html.parser")

    def get_albums(self) -> Dict[Union[str, Any], Union[Union[List[Any], int], Any]]:
        all_divs = self.soup.select("#listAlbum")[0].contents

        current_album = ""
        album_dict: Dict[Union[str, Any], Union[Union[List[Any], int], Any]] = {}
        lyric_count = 0

        for index, div in enumerate(
            d for d in all_divs if type(d) == Tag if d.text != ""
        ):

            if "album" in div.attrs["class"]:
                current_album = div.text
                album_dict[current_album] = list()
            elif "listalbum-item" in div.attrs["class"]:
                lyrics_meta = dict()

                for lyrics_href in [
                    d.attrs["href"] for d in div.descendants if d.name == "a"
                ]:
                    lyrics_meta["href"] = lyrics_href

                lyrics_meta["name"] = div.text
                lyrics_meta["index"] = index
                album_dict[current_album].append(lyrics_meta)
                lyric_count = lyric_count + 1
            else:
                continue

        album_dict["lyric_count"] = lyric_count

        return album_dict
