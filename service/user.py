import hashlib
import base64
import hmac

from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDao


class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_one_by_email(self, email):
        return self.dao.get_by_email(email)

    def get_all(self, role):

        if role:
            all_users = self.dao.get_all_user_role(role)

            return all_users

        all_users = self.dao.get_all()

        return all_users

    def create(self, data):
        data["password"] = self.get_hash(data.get("password"))

        self.dao.create(data)

    def update(self, data):

        uid = data.get("id")
        user = self.get_one(uid)

        fields_to_update = ["email", "name", "surname", "favorite_genre"]

        for field in fields_to_update:
            if data.get(field):
                setattr(user, field, data.get(field))

        self.dao.update(user)

        return self.dao.update(user)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def check_password(self, password_hash, password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ))
