import jwt
import datetime
import calendar

from helpers.constants import JWT_ALGO, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, email, password, is_refresh=False):

        user = self.user_service.get_one_by_email(email)

        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.check_password(user.password, password):
                raise Exception("Stop")

        data = {
            "email": user.email,
            "role": user.role
            }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        day180 = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data["exp"] = calendar.timegm(day180.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def check_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGO, ])
        email = data.get("email")

        user = self.user_service.get_one_by_email(email)

        if user is None:
            raise Exception()

        return self.generate_token(email, user.password, is_refresh=True)

    def valid_token(self, access_token, refresh_token):
        for token in [access_token, refresh_token]:
            try:
                jwt.decode(jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGO, ])
            except Exception as e:
                return str(e), False
        return True
