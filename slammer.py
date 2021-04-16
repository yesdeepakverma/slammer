from google.cloud import firestore
import datetime
import json
import uuid
import base64
from cryptography.fernet import Fernet


class Slammer:

    def __init__(self):
        self.db = firestore.Client()
        self.collection = "slammer"
        self.notes = "notes"
        self.default_password = "Welcome@1234"

    def update_login_key(self, username):
        _key = str(uuid.uuid1())
        val = self.get_farnet_key(_key[:32]).decode()
        self.db.collection(self.collection).document(username).update({'login_key': val})
        return val

    def get_user_by_key(self, login_key):
        users = self.db.collection(self.collection).where('login_key', '==', login_key).where("status", '==', 'active').get()
        if len(users) >= 1:
            return users[0].to_dict()
        return None

    def list_user(self, username):
        ids = self.db.collection(self.collection).where("status", '==', "active").stream()  # != not supported by firestore
        ids = [i.to_dict() for i in ids]
        ids = [i for i in ids if i['username'] != username]
        return ids

    def get_user(self, slammer_id, status_check=True):
        user = self.db.collection(self.collection).document(slammer_id).get()
        if user is not None:
            user = user.to_dict()
            if status_check and user and user.get('status', 'active') != 'active':
                user = None
        return user

    def add_user(self, username, metadata=None):
        username = str(username)
        if metadata is None:
            metadata = dict()
            metadata['password'] = self.default_password
        metadata["username"] = username
        metadata['status'] = 'active'
        user = self.get_user(username, status_check=False)
        if user:
            print("User Already exists")
            return None
        else:
            self.db.collection(self.collection).document(username).set(metadata)
        return username

    def add_notes(self, to_slam, from_slam, note):
        to_slam_doc = self.db.collection(self.collection).document(to_slam)
        timestamp = int(datetime.datetime.utcnow().timestamp())

        enc_note = self.encrypt(timestamp, note)
        _note = {"from": from_slam, "note": enc_note, "timestamp": timestamp}
        to_slam_doc.update({self.notes: firestore.ArrayUnion([_note])})
        return _note

    def list_notes(self, to_slam):
        to_slam_doc = self.db.collection(self.collection).document(to_slam)
        notes = []
        if to_slam_doc:
            notes = to_slam_doc.get().to_dict().get(self.notes, [])
            for note in notes:
                key = self.get_farnet_key(note['timestamp'])
                try:
                    note['note'] = Fernet(key).decrypt(note['note']).decode()
                    note['timestamp'] = datetime.datetime.fromtimestamp(int(note['timestamp'])).strftime("%A, %d. %B %Y %I:%M%p")
                except TypeError:
                    pass

        return notes

    def get_farnet_key(self, value):
        value = str(value).ljust(32, '0')
        val = base64.urlsafe_b64encode(str(value).encode())
        return val

    def encrypt(self, key, value):
        fernet = Fernet(self.get_farnet_key(key))
        enc_note = fernet.encrypt(value.encode())
        return enc_note

    def decrypt(self, key, value):
        farnet = Fernet(self.get_farnet_key(key))
        val = farnet.decrypt(value).decode()
        return val

if __name__ == "__main__":
    nm = Slammer()
    nm.add_user("yesdeepakverma")
    print(nm.get_user('yesdeepakverma'))
    print(nm.list_user())
    print(nm.add_notes("yesdeepakverma", "dverma", "deepak"))
    print(nm.list_notes("yesdeepakverma"))