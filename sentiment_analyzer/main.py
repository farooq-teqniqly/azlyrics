import codecs
import json
import logging
import os

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
from msrest.authentication import CognitiveServicesCredentials
from tqdm import tqdm

from cog_service import CogService

load_dotenv(".env", override=True)
log_level = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

input_file = os.getenv("LYRICS_INPUT_FILE")

if not input_file:
    raise ValueError(f"LYRICS_INPUT_FILE environment variable not set!")

output_file = os.getenv("OUTPUT_FILE")

if not output_file:
    raise ValueError(f"OUTPUT_FILE environment variable not set!")

cog_key = os.getenv("COG_KEY")

if not cog_key:
    raise ValueError(f"COG_KEY environment variable not set!")

cog_endpoint = os.getenv("COG_ENDPOINT")

if not cog_endpoint:
    raise ValueError(f"COG_ENDPOINT environment variable not set!")

text_analytics_client = TextAnalyticsClient(
    endpoint=cog_endpoint, credentials=CognitiveServicesCredentials(cog_key)
)

cog_service = CogService(text_analytics_client, log)

with codecs.open(input_file, "r", "utf-8") as reader:
    text = reader.read()
    albums = json.loads(text)

    docs = []

    log.info("Getting sentiment scores...")
    lyric_count = int(albums["lyric_count"])

    with tqdm(total=lyric_count) as progress:
        for album, metadata in albums.items():
            if album == "lyric_count":
                continue
            for meta in metadata:
                score = cog_service.get_sentiment(
                    {"id": meta["name"], "text": meta["lyrics"]})
                meta["sentiment"] = score
                progress.update(1)

    log.info(f"Writing output to {output_file}...")

    with codecs.open(output_file, "w", "utf-8") as writer:
        writer.write(json.dumps(albums))

    log.info("Done.")
