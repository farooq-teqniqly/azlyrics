import codecs
import json
import logging
import os
import random
import time

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(".env", override=True)
log_level = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

get_albums_only = False
get_albums_only_str = os.getenv("GET_ALBUMS_ONLY")
log.info(f"GET_ALBUMS_ONLY={get_albums_only_str}")

if get_albums_only_str:
    if int(get_albums_only_str) > 0:
        get_albums_only = True

if get_albums_only:
    album_output_file = os.getenv("ALBUMS_OUTPUT_FILE")

    if not album_output_file:
        raise ValueError("ALBUMS_OUTPUT_FILE not set!")

    band_url = os.getenv("BAND_URL")
    log.info(f"BAND_URL={band_url}")

    from get_albums import GetAlbums

    ga = GetAlbums(band_url, log)
    albums = ga.get_albums()

    log.info(f"Writing albums to {album_output_file}...")

    with codecs.open(album_output_file, "w", "utf-8") as writer:
        writer.write(json.dumps(albums))
        log.info("Done.")
else:
    lyrics_input_file = os.getenv("LYRICS_INPUT_FILE")

    if not lyrics_input_file:
        raise ValueError("LYRICS_INPUT_FILE environment variable not set.")

    lyrics_root_url = os.getenv("LYRICS_ROOT_URL")

    if not lyrics_root_url:
        raise ValueError("LYRICS_ROOT_URL environment variable not set.")

    lyrics_output_file = os.getenv("LYRICS_OUTPUT_FILE")

    if not lyrics_output_file:
        raise ValueError("LYRICS_OUTPUT_FILE environment variable not set.")

    from get_lyrics import GetLyrics

    gl = GetLyrics(lyrics_root_url, log)

    with codecs.open(lyrics_input_file, "r", "utf-8") as reader:
        albums = json.loads(reader.read())

    lyric_count = int(albums["lyric_count"])

    log.info("Downloading lyrics...")

    try:
        with tqdm(total=lyric_count) as progress:
            for album, metadata in albums.items():
                for meta in metadata:
                    lyrics = gl.get_lyrics(meta["href"])
                    meta["lyrics"] = lyrics
                    progress.update(1)
                    time.sleep(random.randint(30, 60))
    finally:
        log.info(f"Writing lyrics to {lyrics_output_file}...")
        with codecs.open(lyrics_output_file, "w", "utf-8") as writer:
            writer.write(json.dumps(albums))
