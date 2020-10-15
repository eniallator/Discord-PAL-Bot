import os
import discord
import configparser
from src.commands import COMMANDS


TOKEN = os.environ.get("DISCORD_TOKEN")

config = configparser.ConfigParser()
config.read("auth.ini")

if not TOKEN:
    try:
        TOKEN = config.get("secret", "token")
    except configparser.NoSectionError:
        raise Exception(
            "Specify discord token either with a auth.ini file or as an argument."
        )


CLIENT = discord.Client()
GUILD_ID = int(config.get("config", "enginf-guild-id"))
PAL_INPUT = int(config.get("config", "pal-questions-input-channel"))
PAL_OUTPUT = int(config.get("config", "pal-questions-output-channel"))


async def command_handler(message, user_command):
    if user_command.lower().split(" ")[0] == "help":
        help_command = " ".join(user_command.split(" ")[1:])
        help_message = COMMANDS.help(help_command, CLIENT, help_command, message)
        await message.channel.send(help_message)
    else:
        output = await COMMANDS.execute(user_command, CLIENT, user_command, message)
        if isinstance(output, str):
            await message.channel.send(output)


@CLIENT.event
async def on_ready():
    print(f'Bot logged in with name: "{CLIENT.user.name}" and id: {CLIENT.user.id}')


@CLIENT.event
async def on_message(message):
    if message.author.bot:
        return

    prefix = "!"
    guild = discord.utils.get(CLIENT.guilds, id=GUILD_ID)
    input_channel = discord.utils.get(CLIENT.get_all_channels(), id=PAL_INPUT)
    output_channel = discord.utils.get(CLIENT.get_all_channels(), id=PAL_OUTPUT)
    is_DM = isinstance(message.channel, discord.DMChannel)
    if not is_DM and message.channel != input_channel:
        return
    if is_DM and message.author not in guild.members:
        await message.channel.send(
            f"You don't appear to be in the sussex enginf discord server. You need to be in the server to ask questions."
        )
        return

    if message.channel == input_channel:
        if message.content.startswith(prefix):
            user_command = message.content.replace(prefix, "", 1)
            await command_handler(message, user_command)
        return

    await output_channel.send(f"<@!{message.author.id}> sent:\n{message.content}")


CLIENT.run(TOKEN)
