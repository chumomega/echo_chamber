from firebase_admin import db
from model.Chamber import Chamber
from model.ChamberType import ChamberType

CHAMBERS_TABLE = "tables/chambers"
CHAMBER_MEMBERS_TABLE = "tables/chamber_members"
COMMENTS_TABLE = "tables/comments"
COMMENT_TAGS_TABLE = "tables/comment_tags"
TAGS_TABLE = "tables/tags"

# Do not create yourself. please use via context initializers :)
class FirebaseClient:
    def __init__(self) -> None:
        return
    
    def add_chamber(self, chamber: Chamber, chamber_type: ChamberType) -> None:
        chamber_x_ref = db.reference(CHAMBERS_TABLE).child(chamber_type.value).child(chamber.get_id())
        chamber_x_ref.set(chamber.get_json_body())

    def get_chamber(self, identifier: str, chamber_type: ChamberType) -> Chamber:
        ref = db.reference(CHAMBERS_TABLE + "/{}/{}".format(chamber_type.value, identifier))
        chamber_response = ref.get()
        if chamber_response is None:
            return None
        return Chamber (
            id = identifier,
            title = chamber_response.get("title", None),
            description = chamber_response.get("description", None),
            author = chamber_response.get("author", None), 
            created_timestamp = chamber_response.get("created_timestamp", None),
            label_magnitudes = chamber_response.get("label_magnitudes", None)
        )