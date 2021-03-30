from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    public_key = Column(String, default=None)
    private_key = Column(String, default=None)

    def __init__(self, _id, username, password):
        super(User, self).__init__()
        self._id = _id
        self.username = username
        self.password = password
        self.public_key = None
        self.private_key = None

    def set_keys(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

