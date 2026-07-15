from threading import Thread

from flask import Flask, jsonify

from bot import bot
from config import DISCORD_BOT_TOKEN


app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({
        "application": "Discord Bot",
        "status": "running"
    })


@app.route("/api/status")
def status():

    return jsonify({
        "bot_ready": bot.is_ready(),
        "latency_ms": (
            round(bot.latency * 1000)
            if bot.is_ready()
            else None
        ),
        "guild_count": len(bot.guilds)
    })


def run_flask():

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":

    flask_thread = Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()

    bot.run(
        DISCORD_BOT_TOKEN
    )