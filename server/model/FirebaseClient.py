import firebase_admin
from firebase_admin import db

class FirebaseClient:
    fb_app = None

    def __init__(self) -> None:
        firebase_admin.initialize_app(options = {"databaseURL": "https://echo-chamber-427700-default-rtdb.firebaseio.com/"})
        self.ref = db.reference('tables/chambers')
        return
    
    def add_users(self) -> None:
        users_ref = self.ref.child('users')
        users_ref.set({
            'alanisawesome': {
                'date_of_birth': 'June 23, 1912',
                'full_name': 'Alan Turing'
            },
            'gracehop': {
                'date_of_birth': 'December 9, 1906',
                'full_name': 'Grace Hopper'
            }
        })