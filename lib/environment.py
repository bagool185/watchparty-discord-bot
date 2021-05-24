from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Environment:
    # discord API stuff
    DISCORD_TOKEN = getenv('DISCORD_TOKEN')
    DISCORD_GUILD = getenv('DISCORD_GUILD')
    # uNoGS API stuff
    NETFLIX_API_DOMAIN = getenv('NETFLIX_API_DOMAIN')
    NETFLIX_API_KEY = getenv('NETFLIX_API_KEY')
    DISCORD_API_BASE_URL = getenv('DISCORD_API_BASE_URL')
    UK_CODE = getenv('UK_CODE')
    # Azure stuff
    COSMOS_DB_HOST = getenv('COSMOS_DB_HOST')
    COSMOS_DB_KEY = getenv('COSMOS_DB_KEY')
    DB_NAME = getenv('DB_NAME')
    CONTAINER_NAME = getenv('CONTAINER_NAME')
