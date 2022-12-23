from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    access_key = Column(String, nullable=True)
    tweets = relationship("tweets")
    followers = relationship("followers")
    likes = relationship("likes")


class Media(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True, index=True)
    file = Column(String)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))


class Follower(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    follower_id = Column(Integer, ForeignKey("users.id"))


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    tweet_data = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    medias = relationship("medias")
    likes = relationship("likes")


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
