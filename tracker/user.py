from flask_login import UserMixin

from tracker.db import open_connection

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = open_connection()
        cursor = db.cursor()
        user_sql = cursor.execute(
            f"SELECT * FROM user WHERE id = {user_id}"
        )
        user = cursor.fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        db.close()
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        user = (id_, name, email, profile_pic)
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (id, name, email, profile_pic)"
            "VALUES (%s, %s, %s, %s)", user
        )
        db.commit()
        db.close()