import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="purge",
        description="Delete multiple messages from the current channel"
    )
    @app_commands.describe(
        amount="Number of messages to delete"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100]
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        deleted = await interaction.channel.purge(
            limit=amount
        )

        await interaction.followup.send(
            f"Deleted {len(deleted)} messages.",
            ephemeral=True
        )


    @purge.error
    async def purge_error(
        self,
        interaction: discord.Interaction,
        error
    ):

        if isinstance(
            error,
            app_commands.MissingPermissions
        ):
            await interaction.response.send_message(
                "You need the **Manage Messages** permission to use this command.",
                ephemeral=True
            )
            return

        raise error


async def setup(bot):
    await bot.add_cog(
        Moderation(bot)
    )