import logging
import os

import hikari
from hikari import intents
import lightbulb
from aiohttp import ClientSession
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
    # Thus redis cache doesn't work with Python 3.10
        
    # cache = sake.redis.RedisCache(bot, bot, address="redis://127.0.0.1:6379")
    # await cache.open()
    # log.info("Connected to Redis")
    
    bot.d.scheduler.start()
    bot.d.session = ClientSession(trust_env=True)
    log.info("AIOHTTP session started")

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    await bot.rest.create_message(
        int(os.getenv("STDOUT_CHANNEL_ID")), 
        "Hikari bot is online."
    )

@bot.listen(hikari.StoppingEvent)    
async def on_stopping(event: hikari.StoppingEvent) -> None:
    bot.d.scheduler.shutdown()
    await bot.d.session.close()
    log.info("AIOHTTP session closed")

    await bot.rest.create_message(
        int(os.getenv("STDOUT_CHANNEL_ID")),
        "Hikari bot is shutting down."
    )

@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent) -> None:
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)    
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandNotFound):
        await bot.rest.create_message(
            int(os.getenv("STDOUT_CHANNEL_ID")), 
            f"Command `{event.context.command.name}` not found."
        )
        return

    if isinstance(event.exception, lightbulb.NotEnoughArguments):
        msg = f"Missing arguments for command `{event.command.name}`: " 
        + ", ".join(event.exception.missing_options)
        await event.context.respond(msg)
        return

    if isinstance(event.exception, lightbulb.ConverterFailure):
        await event.context.respond(
            f"The {event.exception.option} option is invalid."
        ) 
        return

    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"Command `{event.context.command.name}` is on cooldown. "
            + f"Try again in {event.exception.retry_after:.0f} seconds."
        )
        return

    await event.context.respond("I have errored and cannot get up.")

    if isinstance(event.exception, lightbulb.CommandInvocationError):
        raise event.exception.original

    raise event.exception

@bot.command()
@lightbulb.command("shutdown", "Shutdown the bot.", aliases=["die", "stop"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def shutdown(ctx: lightbulb.context.Context) -> None:
    await ctx.respond("Shutting down...")
    await bot.close()


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()