from dotenv import load_dotenv
from bot.bot import Bot

import os

def main():
    load_dotenv()

    bot = Bot(
        token=os.getenv("MATTERMOST_BOT_TOKEN"),
        base_url=os.getenv("MATTERMOST_SERVER_URL"),
        external_database_url=os.getenv("EXTERNAL_DATABASE_URL"),
        auxiliary_database_url=os.getenv("AUXILIARY_DATABASE_URL"),
        team_mattermost=os.getenv("TEAM_MATTERMOST_NAME")
    )

    bot.start()

if __name__ == "__main__":
    main()
