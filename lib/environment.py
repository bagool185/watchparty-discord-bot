import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD = os.getenv('DISCORD_GUILD')
    NETFLIX_API_DOMAIN = os.getenv('NETFLIX_API_DOMAIN')
    NETFLIX_API_KEY = os.getenv('NETFLIX_API_KEY')
    DISCORD_API_BASE_URL = os.getenv('DISCORD_API_BASE_URL')
    UK_CODE = os.getenv('UK_CODE')
