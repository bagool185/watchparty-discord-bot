import os

from dotenv import load_dotenv

load_dotenv()


class Environment:
    # discord API stuff
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD = os.getenv('DISCORD_GUILD')
    # uNoGS API stuff
    NETFLIX_API_DOMAIN = os.getenv('NETFLIX_API_DOMAIN')
    NETFLIX_API_KEY = os.getenv('NETFLIX_API_KEY')
    DISCORD_API_BASE_URL = os.getenv('DISCORD_API_BASE_URL')
    UK_CODE = os.getenv('UK_CODE')
    # Azure stuff
    COSMOS_DB_HOST = os.getenv('COSMOS_DB_HOST')
    COSMOS_DB_KEY = os.getenv('COSMOS_DB_KEY')
    DB_NAME = os.getenv('DB_NAME')
    CONTAINER_NAME = os.getenv('CONTAINER_NAME')
