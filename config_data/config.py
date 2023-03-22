import os
import dotenv


class TgBot:
    def __init__(self, token, admins_ids):
        self.token = token
        self.admins_ids = admins_ids


class Config:
    def __init__(self, bot):
        self.bot = bot


def load_config(path: str | None = None):

    dotenv.load_dotenv(path)

    return Config(TgBot(token=os.getenv('BOT_TOKEN'),
                        admins_ids=os.getenv('ADMIN_ID')))
