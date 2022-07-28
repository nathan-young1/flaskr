from sqlalchemy import Column, Integer, VARCHAR
from db.db_connector import Base

class User(Base):
    __tablename__ : str = 'authentication'

    id_no = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(30), unique=True)
    password = Column(VARCHAR(255))

    def __repr__(self):
        return f'<User(username={self.username})>'

    def __str__(self):
        return f'User(username={self.username})'

