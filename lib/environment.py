import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD = os.getenv('DISCORD_GUILD')