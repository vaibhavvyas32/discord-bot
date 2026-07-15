import discord
from discord.ext import commands

from database.db import initialize_database


class DiscordBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()

        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        intents.voice_states = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )


    async def setup_hook(self):

        initialize_database()

        await self.load_extension(
            "cogs.moderation"
        )

        await self.load_extension(
            "cogs.logging"
        )

        await self.load_extension(
            "cogs.music"
        )

        commands = await self.tree.sync()

        print(
            f"Synced {len(commands)} slash commands."
        )


    async def on_ready(self):

        print(
            f"Logged in as {self.user}"
        )

        print(
            f"Connected to {len(self.guilds)} server(s)."
        )


bot = DiscordBot()