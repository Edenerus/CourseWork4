from dao.model.user import User


class UserDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        entity = self.session.query(User).get(uid)

        return entity

    def get_one_by_username(self, username):
        entity = self.session.query(User).filter(User.username == username).first()

        return entity

    def get_all(self):
        entity_list = self.session.query(User).all()

        return entity_list

    def get_all_user_role(self, role):
        all_users = self.session.query(User).filter(User.role == role)

        return all_users.all()

    def create(self, data):
        user = User(**data)

        self.session.add(user)
        self.session.commit()

        return user

    def update(self, user):
        self.session.add(user)
        self.session.commit()

        return user

    def delete(self, uid):
        user = self.get_one(uid)

        self.session.delete(user)
        self.session.commit()
