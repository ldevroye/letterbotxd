import os
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from src.db import SqlDatabase
from src.models import PyDatabase


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

        await self.handle_command(message)

    async def handle_command(self, message):
        print(f"message: {message.content}, {message.author.id}")


if __name__ == '__main__':
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True

    db: SqlDatabase = SqlDatabase(False, 'test')

    client = MyBot(int(os.getenv('DISCORD_CHANNEL_ID')),
                   db,
                   os.getenv('DISCORD_PREFIX'),
                   intents=intents)

    client.run(os.getenv('DISCORD_API_KEY'))
