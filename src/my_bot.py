import os
import discord
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

    async def handle_command(self, message):
        print(f"Commande ({message.author.id}): {message.content}")

        self._db.interact_db(RequestType.ADD_REVIEW, user_idd=1, review="hehe")


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
