import os
import discord
import shlex
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from src.common import RequestType
from src.db import SqlDatabase
from src.models.py_db import PyDatabase


class MyBot(commands.Bot):
    def __init__(self, channel: int, py_db: PyDatabase, prefix: str, intents: Intents, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents, **kwargs)
        self._channel: int = channel
        self._db: PyDatabase = py_db
        self._prefix: str = prefix

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id != self._channel:
            return

        if message.content.startswith(self._prefix):
            await self.handle_command(message)

        print(f"Message ({message.author.name}): '{message.content}'")

    async def interact_db(self, request_type: RequestType, **options):
        self._db.interact_db(request_type=request_type, **options)

    async def handle_command(self, message):
        print(f"Command ({message.author.id}): {message.content}")

        msg_lst: list[str] = shlex.split(message.content[len(self._prefix):])
        print(f"msg list: {msg_lst}, len:{len(msg_lst)}")
        cmd: str = msg_lst[0].upper()

        cmd_list: list[str] = [r.name.upper() for r in RequestType if not r.name.startswith('_')]

        if cmd == cmd_list[0]:  # GET_USER
            user_id = message.author.id
            await self.interact_db(RequestType.GET_USER, user_id=user_id)

        elif cmd == cmd_list[1]:  # GET_TO_WATCH
            pass

        elif cmd == cmd_list[2]:  # GET_REVIEW
            pass

        elif cmd == cmd_list[3]:  # GET_RATING
            pass
        elif cmd == cmd_list[4]:  # GET_LIST_USER_TO_WATCH
            pass
        elif cmd == cmd_list[5]:  # GET_LIST_TO_WATCH_USERS
            pass
        elif cmd == cmd_list[6]:  # GET_RATINGS_TO_WATCH
            pass
        elif cmd == cmd_list[7]:  # GET_USER_RATINGS
            pass
        elif cmd == cmd_list[8]:  # ADD_USER
            pass
        elif cmd == cmd_list[9]:  # ADD_TO_WATCH
            pass
        elif cmd == cmd_list[10]:  # ADD_REVIEW
            pass
        elif cmd == cmd_list[11]:  # CHANGE_REVIEW
            pass
        elif cmd == cmd_list[12]:  # REMOVE_TO_WATCH
            pass
        elif cmd == cmd_list[13]:  # REMOVE_REVIEW
            pass
        elif cmd == cmd_list[14]:  # REMOVE_USER
            pass

        else:
            raise NotImplementedError(
                f"Command {cmd} not known, try one among: \n\t{cmd_list}")


if __name__ == '__main__':
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True

    sql_db: SqlDatabase = SqlDatabase(False, 'test')
    py_db: PyDatabase = PyDatabase(sql_db)

    client = MyBot(int(os.getenv('DISCORD_CHANNEL_ID')),
                   py_db,
                   os.getenv('DISCORD_PREFIX'),
                   intents=intents)

    client.run(os.getenv('DISCORD_API_KEY'))
