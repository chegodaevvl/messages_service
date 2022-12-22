"""Create main tables

Revision ID: 3bf4da1963c9
Revises: 
Create Date: 2022-12-22 13:02:06.070979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence


# revision identifiers, used by Alembic.
revision = '3bf4da1963c9'
down_revision = None
branch_labels = None
depends_on = None


def create_users_table():
    op.execute(CreateSequence(Sequence('user_id_seq')))
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=200), nullable=False),
                    sa.Column('access_key', sa.String(length=200), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def create_tweets_table():
    op.execute(CreateSequence(Sequence('tweet_id_seq')))
    op.create_table('tweets',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('tweet_data', sa.String(length=200), nullable=False),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def create_medias_table():
    op.execute(CreateSequence(Sequence('media_id_seq')))
    op.create_table('medias',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('file', sa.String(length=200), nullable=False),
                    sa.Column('tweet_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def create_followers_table():
    op.execute(CreateSequence(Sequence('follower_id_seq')))
    op.create_table('followers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.Column('follower_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ['follower_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def create_likes_table():
    op.execute(CreateSequence(Sequence('like_id_seq')))
    op.create_table('likes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('tweet_id', sa.Integer, nullable=False),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def upgrade() -> None:
    create_users_table()
    create_tweets_table()
    create_medias_table()
    create_followers_table()
    create_likes_table()


def downgrade() -> None:
    op.drop_table('likes')
    op.drop_table('followers')
    op.drop_table('medias')
    op.drop_table('tweets')
    op.drop_table('users')
