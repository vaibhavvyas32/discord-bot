import discord
from discord import app_commands
from discord.ext import commands

from database.db import (
    save_message,
    mark_message_deleted,
    get_latest_deleted_message
)


class MessageLogging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(
        self,
        message: discord.Message
    ):

        if message.author.bot:
            return

        if message.guild is None:
            return

        save_message(
            message_id=message.id,
            guild_id=message.guild.id,
            channel_id=message.channel.id,
            user_id=message.author.id,
            username=str(message.author),
            content=message.content,
            created_at=message.created_at.isoformat()
        )


    @commands.Cog.listener()
    async def on_raw_message_delete(
        self,
        payload: discord.RawMessageDeleteEvent
    ):

        mark_message_deleted(
            payload.message_id
        )


    @app_commands.command(
        name="snipe",
        description="Show the latest deleted message"
    )
    async def snipe(
        self,
        interaction: discord.Interaction
    ):

        message = get_latest_deleted_message(
            guild_id=interaction.guild.id,
            channel_id=interaction.channel.id
        )

        if message is None:

            await interaction.response.send_message(
                "No deleted messages found.",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title="Deleted Message",
            description=(
                message["content"]
                or "*No text content*"
            ),
            color=discord.Color.red()
        )

        embed.add_field(
            name="User",
            value=message["username"],
            inline=True
        )

        embed.add_field(
            name="Deleted",
            value=message["deleted_at"],
            inline=True
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        MessageLogging(bot)
    )