from firebase_admin import db
from model import Chamber

# Do not create yourself. please use via context initializers :)
class FirebaseClient:
    def __init__(self) -> None:
        self.chambers_table = db.reference('tables/chambers')
        self.chamber_members_table = db.reference('tables/chamber_members')
        self.comments_table = db.reference('tables/comments')
        self.comment_tags_table = db.reference('tables/comment_tags')
        self.tags_table = db.reference('tables/tags')
        return
    
    def add_chamber(self, chamber: Chamber) -> None:
        chamber_x_ref = self.chambers_table.child(chamber.get_id())
        chamber_x_ref.set(chamber.get_json_body())