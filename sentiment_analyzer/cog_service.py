from logging import Logger

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient


class CogService:
    def __init__(self, client: TextAnalyticsClient, log: Logger):
        self.client = client
        self.log = log

    def get_sentiment(self, doc: dict) -> float:
        self.log.debug(f"Getting sentiment for {doc['id']}")
        analysis = self.client.sentiment(documents=[doc])
        return analysis.documents[0].score
