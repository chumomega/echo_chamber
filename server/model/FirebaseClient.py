from firebase_admin import db

# Do not create yourself. please use via context initializers :)
class FirebaseClient:
    def __init__(self) -> None:
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