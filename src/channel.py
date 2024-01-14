import json
import os
from googleapiclient.discovery import build
from config import CHANNEL_DATA


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id

        self.channel_data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"

        self.subs_count = self.channel_data['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_data['items'][0]['statistics']['videoCount']
        self.views_count = self.channel_data['items'][0]['statistics']['subscriberCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        json_data = json.dumps(self.channel_data)

        with open(f"../Data/{file_name}", 'w') as file:
            file.write(json_data)
