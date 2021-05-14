import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD = os.getenv('DISCORD_GUILD')
    NETFLIX_API_BASE_URL = os.getenv('NETFLIX_API_BASE_URL')
    NETFLIX_API_KEY = os.getenv('NETFLIX_API_KEY')