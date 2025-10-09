import shutil

from src.db import *
from src.my_bot import *
import os

CONFIG: dict[str: str] = dict()
intents = discord.Intents.default()
intents.message_content = True


def check_env():
    env: Final[str] = '.env'
    exmpl: Final[str] = env+'.example'

    if not os.path.exists(env):
        shutil.copy(exmpl, env)


def get_env() -> dict[str: str]:
    check_env()
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


def start_db() -> SqlDatabase:
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

        to_ret = SqlDatabase(create, name)
    except:
       raise RuntimeError(
          f'Could not start the database {name} try looking at the .env and "{name}"')

    return to_ret


def start_bot(py_db: PyDatabase) -> MyBot:
    print(f"Starting bot... listening to {CONFIG["DISCORD_PREFIX"]} commands")
    try:
        to_ret = MyBot(channel=int(CONFIG["DISCORD_CHANNEL_ID"]),
                       prefix=CONFIG["DISCORD_PREFIX"],
                       py_db=py_db,
                       intents=intents)
    except:
        raise RuntimeError(
            f'Could not start/connect the BOT, check DISCORD_API_KEY (String) and DISCORD_CHANNEL_ID (Integer)')

    return to_ret


def link_bot():
    pass


if __name__ == '__main__':
    CONFIG = get_env()
    sql_database: SqlDatabase = start_db()
    py_database: PyDatabase = PyDatabase(sql_database)
    bot: MyBot = start_bot(py_database)
    bot.run(token=CONFIG["DISCORD_API_KEY"])
    link_bot()
