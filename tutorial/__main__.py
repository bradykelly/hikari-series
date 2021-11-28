import logging
import os

import hikari
from hikari import intents
import lightbulb
import sake
from lightbulb import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

log = logging.getLogger(__name__)

bot = lightbulb.BotApp(
    os.getenv("TOKEN"),
    prefix='!',
    default_enabled_guilds=int(os.getenv("DEFAULT_GUILD")),
    help_slash_command=True,
    case_insensitive_prefix_commands=True,
    intents=hikari.Intents.ALL,
)
bot.d.scheduler = AsyncIOScheduler()
bot.d.scheduler.configure(timezone=utc)

@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    # cache = sake.redis.RedisCache(bot, bot, address="redis://127.0.0.1")
    # await cache.open()
    # log.info("Connected to Redis")
    ...

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    await bot.rest.create_message(
        int(os.getenv("STDOUT_CHANNEL_ID")), 
        "Hikari bot is online."
    )

@bot.command()
@lightbulb.command("shutdown", "Shutdown the bot.", aliases=["die", "stop"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def shutdown(ctx: lightbulb.context.Context) -> None:
    await ctx.respond("Shutting down...")
    await bot.rest.create_message(
        int(os.getenv("STDOUT_CHANNEL_ID")), 
        "Shutting down..."
    )
    await bot.close()


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()