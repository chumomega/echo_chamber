from firebase_admin import db
from model.Chamber import Chamber
from model.Comment import Comment
from model.ChamberType import ChamberType
import logging
from model.LabelMagnitudes import PoliticalLabelMagnitudes

CHAMBERS_TABLE = "tables/chambers"
CHAMBER_MEMBERS_TABLE = "tables/chamber_members"
COMMENTS_TABLE = "tables/comments"
TAGS_TABLE = "tables/tags"
CHAMBER_TAGS_TABLE = "tables/chamber_tags"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Do not create yourself. please use via context initializers :)
class FirebaseClient:
    def __init__(self) -> None:
        return

    def add_chamber(self, chamber: Chamber, chamber_type: ChamberType) -> None:
        chamber_x_ref = (
            db.reference(CHAMBERS_TABLE)
            .child(chamber_type.value)
            .child(chamber.get_id())
        )
        chamber_x_ref.set(chamber.get_json_body())

    def add_chamber_member(
        self, chamber_identifier: str, chamber_type: ChamberType, comment: Comment
    ) -> None:
        # Store Comment data
        comments_ref = (
            db.reference(COMMENTS_TABLE)
            .child(chamber_type.value)
            .child(comment.get_id())
        )
        comments_ref.set(comment.get_json_body())

        # Associate comment data with chamber table
        chamber_members_ref = (
            db.reference(CHAMBER_MEMBERS_TABLE)
            .child(chamber_type.value)
            .child(chamber_identifier)
        )
        chamber_members_ref.child(comment.get_id()).set(True)

    def add_chamber_tags(
        self, chamber_identifier: str, chamber_type: ChamberType, tags: list[str]
    ) -> None:
        logger.info(f"Storing tags for {chamber_identifier} in Firebase...")
        chamber_tags_ref = db.reference(
            CHAMBER_TAGS_TABLE + "/{}/{}".format(chamber_type.value, chamber_identifier)
        )
        for tag in tags:
            tags_ref = db.reference(TAGS_TABLE).child(chamber_type.value).child(tag)
            tags_ref.child(chamber_identifier).set(True)
            chamber_tags_ref.child(tag).set(True)

    def get_chamber(self, identifier: str, chamber_type: ChamberType) -> Chamber:
        ref = db.reference(
            CHAMBERS_TABLE + "/{}/{}".format(chamber_type.value, identifier)
        )
        chamber_response = ref.get()
        if chamber_response is None:
            return None
        return Chamber(
            id=identifier,
            chamber_type=chamber_type.value,
            title=chamber_response.get("title", None),
            description=chamber_response.get("description", None),
            author=chamber_response.get("author", None),
            created_timestamp=chamber_response.get("created_timestamp", None),
            label_magnitudes=chamber_response.get("label_magnitudes", None),
            chamber_status=chamber_response.get("chamber_status", None),
            chamber_reasoning=chamber_response.get("chamber_reasoning", None),
        )

    def update_chamber_label_magnitudes(
        self,
        identifier: str,
        chamber_type: str,
        label_magnitudes: PoliticalLabelMagnitudes,
    ):
        ref = db.reference(
            CHAMBERS_TABLE
            + "/{}/{}/{}".format(chamber_type, identifier, "label_magnitudes")
        )
        ref.update(label_magnitudes)

    def add_chamber_status(
        self,
        identifier: str,
        chamber_type: str,
        chamber_status: str,
    ):
        ref = db.reference(
            CHAMBERS_TABLE
            + "/{}/{}/{}".format(chamber_type, identifier, "chamber_status")
        )
        ref.set(chamber_status)

    def add_chamber_reasoning(
        self,
        identifier: str,
        chamber_type: str,
        chamber_reasoning: str,
    ):
        ref = db.reference(
            CHAMBERS_TABLE
            + "/{}/{}/{}".format(chamber_type, identifier, "chamber_reasoning")
        )
        ref.set(chamber_reasoning)

    def get_chamber_members(
        self, identifier: str, chamber_type: ChamberType
    ) -> list[Comment]:
        ref = db.reference(
            CHAMBER_MEMBERS_TABLE + "/{}/{}".format(chamber_type.value, identifier)
        )
        chamber_members: dict = ref.get()

        if chamber_members is None or len(chamber_members) == 0:
            return []

        full_chamber_member_data = []
        for member_key, member_value in chamber_members.items():
            if member_value is True:
                comment_ref = (
                    db.reference(COMMENTS_TABLE)
                    .child(chamber_type.value)
                    .child(member_key)
                )
                comment = comment_ref.get()
                full_chamber_member_data.append(
                    Comment(
                        id=member_key,
                        text=comment["text"] if "text" in comment else None,
                        author=comment["author"] if "author" in comment else None,
                        created_timestamp=(
                            comment["created_timestamp"]
                            if "created_timestamp" in comment
                            else None
                        ),
                        label_magnitudes=(
                            comment["label_magnitudes"]
                            if "label_magnitudes" in comment
                            else None
                        ),
                    )
                )

        return full_chamber_member_data

    def get_chamber_tags(self, identifier: str, chamber_type: ChamberType) -> list[str]:
        chamber_tags_ref = db.reference(
            CHAMBER_TAGS_TABLE + "/{}/{}".format(chamber_type.value, identifier)
        )
        chamber_tags: dict = chamber_tags_ref.get()

        if chamber_tags is None or len(chamber_tags) == 0:
            return []

        tags = []
        for chamber_tag, tag_value in chamber_tags.items():
            if tag_value is True:
                tags.append(chamber_tag)

        return tags

    def get_tag_chamber_urls(self, tag: str, chamber_type: ChamberType) -> list[str]:
        """
        This function returns a list of chamber urls that share a tag with the input tag.
        Only chambers with the same chamber_type will be retrieved
        """
        tags_ref = db.reference(TAGS_TABLE).child(chamber_type.value).child(tag)
        tag_members: dict = tags_ref.get()

        chambers_with_similar_tag = []
        for tag_member, tag_value in tag_members.items():
            if tag_value is not True:
                return []
            chambers_with_similar_tag.append(
                self.__get_url_for_chamber(tag_member, chamber_type)
            )

        return chambers_with_similar_tag

    def get_tag_chamber_ids(self, tag: str, chamber_type: ChamberType) -> list[str]:
        """
        This function returns a list of chamber ids that share a tag with the input tag.
        Only chambers with the same chamber_type will be retrieved
        """
        tags_ref = db.reference(TAGS_TABLE).child(chamber_type.value).child(tag)
        tag_members: dict = tags_ref.get()

        chambers_with_similar_tag = []
        for tag_member, tag_value in tag_members.items():
            if tag_value is not True:
                return []
            chambers_with_similar_tag.append(tag_member)

        return chambers_with_similar_tag

    def __get_url_for_chamber(self, identifier: str, chamber_type: ChamberType) -> str:
        match chamber_type:
            case ChamberType.YOUTUBE:
                return f"https://www.youtube.com/watch?v={identifier}"
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")
