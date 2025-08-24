from src.db import *
from src.my_bot import *

CONFIG: dict[str: str] = dict()
intents = discord.Intents.default()
intents.message_content = True


def get_env() -> dict[str: str]:
    load_dotenv()

    to_ret: dict[str: str] = dict()

    to_ret['DISCORD_API_KEY'] = os.getenv('DISCORD_API_KEY')
    to_ret['DISCORD_CHANNEL_ID'] = os.getenv('DISCORD_CHANNEL_ID')
    to_ret['DISCORD_PREFIX'] = os.getenv('DISCORD_PREFIX')
    to_ret['DB_NAME'] = os.getenv('DB_NAME')
    to_ret['DB_CREATE'] = os.getenv('DB_CREATE')
    to_ret['DB_ERASE'] = os.getenv('DB_ERASE')
    to_ret['DB_STR_TYPE'] = os.getenv('DB_STR_TYPE')
    to_ret['DB_INT_TYPE'] = os.getenv('DB_INT_TYPE')
    to_ret['DB_PRIMARY_KEY_TYPE'] = os.getenv('DB_PRIMARY_KEY_TYPE')
    to_ret['DB_FLOAT_TYPE'] = os.getenv('DB_FLOAT_TYPE')

    return to_ret


def start_db() -> Database:
    name: str = CONFIG["DB_NAME"]
    create: bool = eval(CONFIG["DB_CREATE"])
    erase: bool = eval(CONFIG["DB_ERASE"])
    try:
        print(
            f'Starting database {name} create from scratch:{create}...')
        if erase:
            if os.path.exists(name):
                os.remove(name)

            set_key('.env', 'DB_ERASE', 'False')

        to_ret = Database(create, name)
    except:
        raise RuntimeError(
            f'Could not start the database {name} try looking at the .env and "{name}.sql"')

    return to_ret


def start_bot(db: Database) -> MyBot:
    print(f"Starting bot... listening to {CONFIG["DISCORD_PREFIX"]} commands")
    try:
        to_ret = MyBot(channel=int(CONFIG["DISCORD_CHANNEL_ID"]),
                       prefix=CONFIG["DISCORD_PREFIX"],
                       db=db,
                       intents=intents)
    except:
        raise RuntimeError(
            f'Could not start/connect the BOT, check DISCORD_API_KEY (String) and DISCORD_CHANNEL_ID (Integer)')

    return to_ret


def link_bot():
    pass


if __name__ == '__main__':
    CONFIG = get_env()
    database: Database = start_db()
    bot: MyBot = start_bot(database)
    bot.run(token=CONFIG["DISCORD_API_KEY"])
    link_bot()
