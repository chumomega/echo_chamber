from firebase_admin import db
from model import Chamber, ChamberType

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

    def get_chamber(self, identifier: str) -> ChamberType:
        ref = db.reference(CHAMBERS_TABLE + "/{}".format(identifier))
        chamber_response = ref.get()
        if chamber_response is None:
            return None
        return Chamber (
            id = identifier,
            title = chamber_response["title"],
            description = chamber_response["description"],
            author = chamber_response["author"], 
            created_timestamp = chamber_response["created_timestamp"],
            label_magnitudes = chamber_response["label_magnitudes"]
        )