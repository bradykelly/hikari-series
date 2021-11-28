import os

import hikari
import lightbulb


bot = lightbulb.BotApp(
    os.getenv("TOKEN"),
    prefix='!',
    default_enabled_guilds=int(os.getenv("DEFAULT_GUILD")),
    help_slash_command=True,
    case_insensitive_prefix_commands=True
)

@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    pass

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    channel = bot.cache.get_guild_channel(int(os.getenv("STDOUT_CHANNEL_ID")))
    await channel.send("Bot started")

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()