import os
import discord
from discord import client
from dotenv import load_dotenv

from src.db import Database


class MyBot(discord.Client):
    def __init__(self, api_key: str, channel: int, db: Database, prefix: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api_key: str = api_key
        self._channel: int = channel
        self._db: Database = db
        self._prefix: str = prefix

    async def run(self, **kwargs):
        super().run(token=self._api_key, **kwargs)

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.channel.id != self._channel:
            return

        await self.handle_command(message)

    async def handle_command(self, message: str):
        print(f"message: {message}")

    """
    CHATGPT - guez
    
    @client.command(name='addmovie')
    async def add_movie(ctx, *, movie_name):
        user_id = ctx.author.id
        username = ctx.author.name

        # Add user if not exists
        db.add_user(user_id, username)

        # Add movie to global list and user's watchlist
        if db.add_movie_to_watchlist(user_id, movie_name):
            await ctx.send(f"Added '{movie_name}' to {username}'s watchlist!")
        else:
            await ctx.send(f"'{movie_name}' is already in your watchlist!")
    """


if __name__ == '__main__':
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyBot(os.getenv('DISCORD_API_KEY'),
                   int(os.getenv('DISCORD_CHANNEL_ID')),
                   Database(False, 'test'),
                   os.getenv('DISCORD_PREFIX'),
                   intents=intents)
    client.run()
