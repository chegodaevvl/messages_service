from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    api_key = Column(String, nullable=True)


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String)
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete='CASCADE'))


class Follower(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, index=True)
    following_id = Column(Integer, ForeignKey("users.id"))
    follower_id = Column(Integer, ForeignKey("users.id"))
    follower = relationship("User", foreign_keys="Follower.follower_id")
    following = relationship("User", foreign_keys="Follower.following_id")


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    tweet_data = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User")
    media = relationship("Media")
    likes = relationship("Like")


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("users.id"))
    liker = relationship("User")
