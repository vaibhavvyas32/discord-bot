import asyncio
import sys
import discord
from discord import app_commands
from discord.ext import commands

from services.youtube import extract_audio


FFMPEG_OPTIONS = {
    "before_options":
        "-reconnect 1 "
        "-reconnect_streamed 1 "
        "-reconnect_delay_max 5",

    "options":
        "-vn"
}


class Music(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.queues = {}

        self.now_playing = {}


    def get_queue(self, guild_id):

        if guild_id not in self.queues:

            self.queues[guild_id] = []

        return self.queues[guild_id]


    async def play_next(
        self,
        guild: discord.Guild
    ):

        queue = self.get_queue(
            guild.id
        )

        voice_client = guild.voice_client

        if voice_client is None:
            return

        if not queue:

            self.now_playing.pop(
                guild.id,
                None
            )

            return

        song = queue.pop(0)

        self.now_playing[
            guild.id
        ] = song

        source = discord.FFmpegPCMAudio(
            song["url"],
            stderr=sys.stderr,
            **FFMPEG_OPTIONS
)


        def after_playing(error):

            if error:

                print(
                    f"Playback error: {error}"
                )

            asyncio.run_coroutine_threadsafe(
                self.play_next(guild),
                self.bot.loop
            )


        voice_client.play(
            source,
            after=after_playing
        )


    @app_commands.command(
        name="play",
        description="Play a YouTube video or search YouTube"
    )
    @app_commands.describe(
        query="YouTube URL or search query"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str
    ):

        if (
            interaction.user.voice
            is None
        ):

            await interaction.response.send_message(
                "You need to join a voice channel first.",
                ephemeral=True
            )

            return


        await interaction.response.defer()


        voice_channel = (
            interaction
            .user
            .voice
            .channel
        )


        voice_client = (
            interaction.guild.voice_client
        )


        if voice_client is None:

            voice_client = (
                await voice_channel.connect()
            )

        elif (
            voice_client.channel
            != voice_channel
        ):

            await voice_client.move_to(
                voice_channel
            )


        try:

            song = await extract_audio(
                query
            )

        except Exception as error:

            print(error)

            await interaction.followup.send(
                "Could not load that YouTube video."
            )

            return


        queue = self.get_queue(
            interaction.guild.id
        )


        if (
            voice_client.is_playing()
            or voice_client.is_paused()
        ):

            queue.append(song)

            await interaction.followup.send(
                f"Added to queue: **{song['title']}**"
            )

            return


        queue.append(song)

        await self.play_next(
            interaction.guild
        )

        await interaction.followup.send(
            f"Now playing: **{song['title']}**"
        )
    @app_commands.command(
        name="pause",
        description="Pause the current song"
    )
    async def pause(
        self,
        interaction: discord.Interaction
    ):

        voice_client = (
            interaction.guild.voice_client
        )

        if (
            voice_client
            and voice_client.is_playing()
        ):

            voice_client.pause()

            await interaction.response.send_message(
                "Playback paused."
            )

        else:

            await interaction.response.send_message(
                "Nothing is currently playing.",
                ephemeral=True
            )


    @app_commands.command(
        name="resume",
        description="Resume playback"
    )
    async def resume(
        self,
        interaction: discord.Interaction
    ):

        voice_client = (
            interaction.guild.voice_client
        )

        if (
            voice_client
            and voice_client.is_paused()
        ):

            voice_client.resume()

            await interaction.response.send_message(
                "Playback resumed."
            )

        else:

            await interaction.response.send_message(
                "Nothing is paused.",
                ephemeral=True
            )


    @app_commands.command(
        name="skip",
        description="Skip the current song"
    )
    async def skip(
        self,
        interaction: discord.Interaction
    ):

        voice_client = (
            interaction.guild.voice_client
        )

        if (
            voice_client
            and (
                voice_client.is_playing()
                or voice_client.is_paused()
            )
        ):

            voice_client.stop()

            await interaction.response.send_message(
                "Skipped."
            )

        else:

            await interaction.response.send_message(
                "Nothing is currently playing.",
                ephemeral=True
            )


    @app_commands.command(
        name="stop",
        description="Stop playback and clear the queue"
    )
    async def stop(
        self,
        interaction: discord.Interaction
    ):

        guild_id = interaction.guild.id

        self.queues[
            guild_id
        ] = []

        self.now_playing.pop(
            guild_id,
            None
        )

        voice_client = (
            interaction.guild.voice_client
        )

        if voice_client:

            voice_client.stop()

        await interaction.response.send_message(
            "Playback stopped and queue cleared."
        )


    @app_commands.command(
        name="leave",
        description="Disconnect from voice"
    )
    async def leave(
        self,
        interaction: discord.Interaction
    ):

        voice_client = (
            interaction.guild.voice_client
        )

        if voice_client is None:

            await interaction.response.send_message(
                "I am not connected to a voice channel.",
                ephemeral=True
            )

            return


        self.queues[
            interaction.guild.id
        ] = []

        self.now_playing.pop(
            interaction.guild.id,
            None
        )

        await voice_client.disconnect()

        await interaction.response.send_message(
            "Disconnected from voice."
        )
    
    @app_commands.command(
        name="queue",
        description="Show the music queue"
    )
    async def queue(
        self,
        interaction: discord.Interaction
    ):

        guild_id = interaction.guild.id

        queue = self.get_queue(
            guild_id
        )

        current = self.now_playing.get(
            guild_id
        )

        lines = []


        if current:

            lines.append(
                f"**Now playing:** "
                f"{current['title']}"
            )


        if queue:

            lines.append(
                "\n**Up next:**"
            )

            for index, song in enumerate(
                queue[:10],
                start=1
            ):

                lines.append(
                    f"{index}. "
                    f"{song['title']}"
                )


        if not lines:

            await interaction.response.send_message(
                "The queue is empty.",
                ephemeral=True
            )

            return


        await interaction.response.send_message(
            "\n".join(lines)
        )


    @app_commands.command(
        name="nowplaying",
        description="Show the currently playing song"
    )
    async def nowplaying(
        self,
        interaction: discord.Interaction
    ):

        song = self.now_playing.get(
            interaction.guild.id
        )


        if song is None:

            await interaction.response.send_message(
                "Nothing is currently playing.",
                ephemeral=True
            )

            return


        embed = discord.Embed(
            title="Now Playing",
            description=song["title"],
            color=discord.Color.blue()
        )


        if song.get(
            "uploader"
        ):

            embed.add_field(
                name="Channel",
                value=song["uploader"]
            )


        if song.get(
            "thumbnail"
        ):

            embed.set_thumbnail(
                url=song["thumbnail"]
            )


        await interaction.response.send_message(
            embed=embed
        )

async def setup(bot):
    await bot.add_cog(Music(bot))