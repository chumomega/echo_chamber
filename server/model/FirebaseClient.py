from firebase_admin import db
from model.Chamber import Chamber
from model.Comment import Comment
from model.ChamberType import ChamberType
import logging

CHAMBERS_TABLE = "tables/chambers"
CHAMBER_MEMBERS_TABLE = "tables/chamber_members"
COMMENTS_TABLE = "tables/comments"
COMMENT_TAGS_TABLE = "tables/comment_tags"
TAGS_TABLE = "tables/tags"

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

    def get_chamber(self, identifier: str, chamber_type: ChamberType) -> Chamber:
        ref = db.reference(
            CHAMBERS_TABLE + "/{}/{}".format(chamber_type.value, identifier)
        )
        chamber_response = ref.get()
        if chamber_response is None:
            return None
        return Chamber(
            id=identifier,
            title=chamber_response.get("title", None),
            description=chamber_response.get("description", None),
            author=chamber_response.get("author", None),
            created_timestamp=chamber_response.get("created_timestamp", None),
            label_magnitudes=chamber_response.get("label_magnitudes", None),
        )

    def get_chamber_members(
        self, identifier: str, chamber_type: ChamberType
    ) -> list[Comment]:
        ref = db.reference(
            CHAMBER_MEMBERS_TABLE + "/{}/{}".format(chamber_type.value, identifier)
        )
        chamber_members: dict = ref.get()
        logger.info(f"The retrieved chamber members: {chamber_members}")

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
