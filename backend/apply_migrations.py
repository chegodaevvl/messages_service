from alembic import command
from alembic.config import Config


config = Config("alembic.ini")

command.upgrade(config, "head")
