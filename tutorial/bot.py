import hikari
import lightbulb

bot = lightbulb.BotApp(
    token,
    prefix='!',
    default_enabled_guilds=914223711043866667,
    help_slash_command=True,
    case_insensitive_prefix_commands=True
)