from model.ChamberType import ChamberType
from context_initializers import get_firebase, get_youtube, get_reddit
from model.Chamber import Chamber
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChamberFactory:

    def __init__(self) -> None:
        return

    def get_chamber(self, identifier: str, chamber_type: str) -> Chamber:
        match chamber_type:
            case ChamberType.YOUTUBE.value:
                return self.__get_youtube_chamber(identifier)
            case ChamberType.REDDIT.value:
                return self.__get_reddit_chamber(identifier)
            case ChamberType.X.value:
                return self.__get_x_chamber(identifier)
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")

    def get_chambers(self, chamber_ids_and_types: list[tuple]) -> list[Chamber]:
        chambers = []
        for chamber_id_and_type in chamber_ids_and_types:
            chamber = self.get_chamber(
                identifier=chamber_id_and_type[0], chamber_type=chamber_id_and_type[1]
            )
            if chamber is not None:
                chambers.append(chamber)
        return chambers

    def __get_youtube_chamber(self, identifier: str) -> Chamber:
        firebase_client = get_firebase()
        chamber_from_db = firebase_client.get_chamber(identifier, ChamberType.YOUTUBE)
        if chamber_from_db is not None:
            return chamber_from_db

        youtube_client = get_youtube()
        chamber = youtube_client.get_video_chamber(identifier)
        firebase_client.add_chamber(chamber, ChamberType.YOUTUBE)
        return chamber

    def __get_reddit_chamber(self, identifier: str) -> Chamber:
        firebase_client = get_firebase()
        chamber_from_db = firebase_client.get_chamber(identifier, ChamberType.REDDIT)
        if chamber_from_db is not None:
            return chamber_from_db

        reddit_client = get_reddit()
        chamber = reddit_client.get_post_chamber(identifier=identifier)
        firebase_client.add_chamber(chamber, ChamberType.REDDIT)

        return chamber

    def __get_x_chamber(self, tags: list[str]) -> Chamber:
        raise NotImplementedError

    def get_similar_chambers_ids(self, chamber_type: str, tags: list[str]) -> set[str]:
        match chamber_type:
            case ChamberType.YOUTUBE.value:
                return self.__get_similar_youtube_chamber_ids(tags)
            case ChamberType.REDDIT.value:
                return self.__get_similar_reddit_chamber_ids(tags)
            case ChamberType.X.value:
                return self.__get_similar_x_chamber(tags)
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")

    def get_similar_youtube_chamber_urls(self, tags: list[str]) -> list[str]:
        """
        This method retrieve all chambers with similar tags for now...
        """
        firebase_client = get_firebase()

        if len(tags) == 0:
            return []

        similar_chambers = set()
        for tag in tags:
            similar_chambers.update(
                firebase_client.get_tag_chamber_urls(tag, ChamberType.YOUTUBE)
            )
        return list(similar_chambers)

    def __get_similar_youtube_chamber_ids(self, tags: list[str]) -> list[str]:
        """
        This method retrieve all chambers with similar tags for now...
        """
        firebase_client = get_firebase()

        if len(tags) == 0:
            return []

        similar_chambers = set()
        for tag in tags:
            similar_chambers.update(
                firebase_client.get_tag_chamber_ids(tag, ChamberType.YOUTUBE)
            )
        return similar_chambers

    def __get_similar_reddit_chamber_ids(self, tags: list[str]) -> list[Chamber]:
        """
        This method retrieve all chambers with similar tags for now...
        """
        firebase_client = get_firebase()

        if len(tags) == 0:
            return []

        similar_chambers = set()
        for tag in tags:
            similar_chambers.update(
                firebase_client.get_tag_chamber_ids(tag, ChamberType.REDDIT )
            )
        return similar_chambers

    def __get_similar_x_chamber(self, tags: list[str]) -> list[Chamber]:
        raise NotImplementedError
