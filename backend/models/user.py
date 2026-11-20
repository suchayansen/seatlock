from flask_login import UserMixin


class User(UserMixin):

    def __init__(
        self,
        id,
        name,
        email,
        role,
        is_active=True
    ):
        self.id = str(id)
        self.name = name
        self.email = email
        self.role = role
        self._is_active = is_active

    @property
    def is_active(self):
        return self._is_active