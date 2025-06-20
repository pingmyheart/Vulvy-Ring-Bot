from pathlib import Path

from configuration.bot_configuration import bot
from configuration.mongo_configuration import mongo_client

base_directory = str(Path(__file__).resolve().parent).replace("/configuration", "")

mongodb_bean = mongo_client()
bot = bot()
