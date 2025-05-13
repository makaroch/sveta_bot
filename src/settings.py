from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")

    POSTGRES_DB = getenv("POSTGRES_DB")
    POSTGRES_USER = getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = getenv("POSTGRES_HOST")
    POSTGRES_PORT = getenv("POSTGRES_PORT")