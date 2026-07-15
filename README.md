# Discordo YT 🎵

A self-hosted Discord bot built with **Python**, **discord.py**, **Flask**, **yt-dlp**, and **FFmpeg**.

The bot provides YouTube audio playback in Discord voice channels, moderation commands, deleted-message logging, and a lightweight Flask health/status API.

It can be run locally or deployed as a Docker-based web service.

---

## Features

### 🎵 YouTube Music

Play YouTube videos as audio directly inside a Discord voice channel.

| Command         | Description                                           |
| --------------- | ----------------------------------------------------- |
| `/play <query>` | Play a YouTube URL or search YouTube using a query    |
| `/pause`        | Pause the currently playing track                     |
| `/resume`       | Resume a paused track                                 |
| `/skip`         | Skip the currently playing track                      |
| `/stop`         | Stop playback and clear the queue                     |
| `/leave`        | Disconnect the bot from the voice channel             |
| `/queue`        | Display the current music queue                       |
| `/nowplaying`   | Display information about the currently playing track |

The bot uses **yt-dlp** to resolve YouTube audio streams and **FFmpeg** to stream the audio into Discord.

---

### 🛡️ Moderation

| Command           | Description                                       |
| ----------------- | ------------------------------------------------- |
| `/purge <amount>` | Delete multiple messages from the current channel |

The user running `/purge` must have the **Manage Messages** permission.

---

### 🗑️ Deleted Message Logging

Messages are stored while the bot is running. If a stored message is later deleted, the bot marks it as deleted in the local SQLite database.

| Command  | Description                                              |
| -------- | -------------------------------------------------------- |
| `/snipe` | Show the latest deleted message from the current channel |

> **Note:** The bot can only log messages that it observed while it was online.

---

### 🌐 Flask API

The bot also runs a lightweight Flask web server.

Available endpoints:

| Endpoint      | Description                                             |
| ------------- | ------------------------------------------------------- |
| `/`           | Basic application information                           |
| `/health`     | Lightweight health-check endpoint                       |
| `/api/status` | Discord bot status, latency, and connected server count |

Example:

```text
http://127.0.0.1:5000/health
```

The Flask server allows the bot to run as a web service on hosting platforms such as Render.

---

# Tech Stack

* Python
* discord.py
* Flask
* yt-dlp
* FFmpeg
* SQLite
* PyNaCl
* davey
* Docker

---

# Project Structure

```text
discordo-yt/
│
├── app.py
├── bot.py
├── config.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .dockerignore
│
├── cogs/
│   ├── __init__.py
│   ├── logging.py
│   ├── moderation.py
│   └── music.py
│
├── database/
│   ├── __init__.py
│   └── db.py
│
└── services/
    ├── __init__.py
    └── youtube.py
```

---

# Prerequisites

Before running the bot, make sure you have:

* Python 3.10 or newer
* FFmpeg
* A Discord bot application
* A Discord server where you can invite the bot

---

# 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd discord-bot
```

---

# 2. Create a Virtual Environment

Create the environment:

```bash
python -m venv venv
```

### Windows

Activate it using:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

# 3. Install Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

The project uses:

```text
discord.py[voice]
Flask
python-dotenv
yt-dlp
PyNaCl
davey
```

---

# 4. Install FFmpeg

FFmpeg is required for Discord voice playback.

## Windows

Using `winget`:

```bash
winget install Gyan.FFmpeg
```

After installation, restart your terminal and verify:

```bash
ffmpeg -version
```

## Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify:

```bash
ffmpeg -version
```

## macOS

Using Homebrew:

```bash
brew install ffmpeg
```

Verify:

```bash
ffmpeg -version
```

The command:

```bash
ffmpeg -version
```

must work before starting the bot.

---

# 5. Create a Discord Bot

Open the Discord Developer Portal:

```text
https://discord.com/developers/applications
```

Then:

1. Click **New Application**.
2. Enter a name for your bot.
3. Open the **Bot** section.
4. Create the bot if necessary.
5. Generate or reset the bot token.
6. Copy the token.

> Never commit your Discord bot token to GitHub.

---

# 6. Enable Required Discord Intents

Inside the Discord Developer Portal, open:

```text
Bot
→ Privileged Gateway Intents
```

Enable:

```text
MESSAGE CONTENT INTENT
```

The bot uses this intent to store message content for deleted-message logging.

---

# 7. Invite the Bot to Your Server

In the Discord Developer Portal, generate an OAuth2 installation URL.

Include these scopes:

```text
bot
applications.commands
```

Recommended bot permissions:

```text
View Channels
Send Messages
Embed Links
Read Message History
Manage Messages
Connect
Speak
```

Authorize the bot for your Discord server.

---

# 8. Get Your Discord Server ID

Enable Developer Mode in Discord:

```text
User Settings
→ Advanced
→ Developer Mode
```

Then:

1. Right-click your Discord server.
2. Click **Copy Server ID**.

This ID is used to register slash commands directly to your server during development.

---

# 9. Configure Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_discord_server_id
```

Example:

```env
DISCORD_BOT_TOKEN=YOUR_TOKEN_HERE
DISCORD_GUILD_ID=123456789012345678
```

Do not commit `.env`.

Your `.gitignore` should contain:

```gitignore
.env
*.env

venv/
__pycache__/
*.pyc

database/bot.db
```

---

# 10. Run the Bot Locally

Make sure your virtual environment is activated:

```bash
venv\Scripts\activate
```

Start the application:

```bash
python app.py
```

You should see output similar to:

```text
Synced 10 commands to guild 123456789012345678
Logged in as YourBot
Connected to 1 server(s).

Running on http://127.0.0.1:5000
```

The bot should now appear online in Discord.

---

# Testing the Bot

## Test Deleted Message Logging

Send a message:

```text
Hello, this message will be deleted.
```

Delete the message.

Then run:

```text
/snipe
```

The bot should display the latest deleted message from that channel.

---

## Test YouTube Playback

Join a Discord voice channel.

Run:

```text
/play never gonna give you up
```

You can also provide a YouTube URL:

```text
/play <YouTube URL>
```

The bot should:

1. Join your voice channel.
2. Search or resolve the YouTube video.
3. Extract the audio stream using yt-dlp.
4. Stream the audio using FFmpeg.

You can then use:

```text
/pause
/resume
/skip
/queue
/nowplaying
/stop
/leave
```

---

# Command Reference

## Music Commands

### `/play <query>`

Play audio from a YouTube URL or search query.

Example:

```text
/play Linkin Park Numb
```

If music is already playing, the track is added to the queue.

---

### `/pause`

Pause the current track.

---

### `/resume`

Resume the currently paused track.

---

### `/skip`

Skip the current track and play the next queued track.

---

### `/stop`

Stop playback and clear the current queue.

---

### `/leave`

Disconnect the bot from the current voice channel.

---

### `/queue`

Display the current track and queued tracks.

---

### `/nowplaying`

Display information about the currently playing track.

---

## Moderation Commands

### `/purge <amount>`

Delete multiple messages from the current channel.

Example:

```text
/purge 20
```

The user must have the **Manage Messages** permission.

---

## Message Logging Commands

### `/snipe`

Display the latest deleted message from the current channel.

Messages are stored in:

```text
database/bot.db
```

The database is created automatically when the bot starts.

---

# Running with Docker

The project includes a Dockerfile that installs FFmpeg automatically.

Build the image:

```bash
docker build -t discordo-yt .
```

Run the container:

```bash
docker run \
    -e DISCORD_BOT_TOKEN="your_token" \
    -e DISCORD_GUILD_ID="your_server_id" \
    -p 5000:5000 \
    discordo-yt
```

The application will be available at:

```text
http://localhost:5000
```

---

# Deploying to Render

The project can be deployed as a Docker-based Web Service.

## 1. Push the Project to GitHub

Make sure the following files are not committed:

```text
.env
discord token.txt
database/bot.db
venv/
```

Never commit your Discord bot token.

---

## 2. Create a Render Web Service

Create a new Web Service and connect the GitHub repository.

Deploy the project using the included:

```text
Dockerfile
```

---

## 3. Configure Environment Variables

Add the following environment variables in Render:

```text
DISCORD_BOT_TOKEN
DISCORD_GUILD_ID
```

Do not add the Discord token directly to the source code.

---

## 4. Configure the Health Check

Set the Render health-check path to:

```text
/health
```

The Flask application listens on Render's provided `PORT` environment variable.

---

## 5. Optional External Monitoring

A monitoring service can periodically request:

```text
https://your-service.example/health
```

The endpoint returns a lightweight HTTP response that can be used for service health monitoring.

---

# SQLite Persistence

The bot currently uses SQLite for message logging:

```text
database/bot.db
```

This works well for local usage.

On cloud platforms with ephemeral filesystems, the database may be deleted when the service is redeployed or recreated.

For persistent production storage, consider replacing SQLite with:

* PostgreSQL
* Another managed relational database
* A persistent disk or volume

---

# Troubleshooting

## Slash Commands Are Not Showing

Make sure the bot was invited with:

```text
applications.commands
```

and:

```text
bot
```

For development, commands can be synced directly to your Discord server using `DISCORD_GUILD_ID`.

Restart the bot after changing or adding commands.

---

## `davey library needed in order to use voice`

Install Discord voice dependencies:

```bash
pip install -U "discord.py[voice]"
```

If required by your installed discord.py version:

```bash
pip install davey
```

Then restart the bot.

---

## FFmpeg Was Not Found

Verify:

```bash
ffmpeg -version
```

If the command is not recognized, install FFmpeg and ensure it is available in your system `PATH`.

Restart the terminal after modifying the `PATH`.

---

## YouTube Playback Stops Working

Update yt-dlp:

```bash
pip install -U yt-dlp
```

YouTube frequently changes its internal behavior, so older versions of yt-dlp may stop extracting audio correctly.

---

## Bot Cannot Join a Voice Channel

Check that the bot has:

```text
View Channel
Connect
Speak
```

permissions for the voice channel.

Also make sure the user running `/play` is already connected to a voice channel.

---

## `/snipe` Cannot Find a Deleted Message

The bot can only retrieve messages that were observed while it was online.

If the bot was offline when the message was sent, it cannot reconstruct the deleted content.

---

# Security

Never commit:

```text
Discord bot tokens
.env files
API keys
Credentials
```

If a Discord bot token is accidentally committed or exposed:

1. Reset the token immediately in the Discord Developer Portal.
2. Remove the token from Git history.
3. Update the environment variable with the new token.

Do not reuse an exposed token.

---

# Current Limitations

* Deleted-message logging only works for messages observed while the bot is online.
* SQLite data may not persist on ephemeral cloud deployments.
* YouTube extraction depends on yt-dlp and may require updates when YouTube changes its platform.
* The music queue is stored in memory and is lost when the bot restarts.
* The bot currently focuses on YouTube audio playback rather than general-purpose audio sources.

---

# License

This project is intended for personal and educational use.

When using third-party services or content sources, ensure your usage complies with their applicable terms and policies.
