import discord
import re
from .command_system.command_system import CommandSystem


COMMANDS = CommandSystem()


async def send(client, user_command, message):
    match = re.match(r"[^<]*<@!?(?P<user_id>\d+)>", user_command)
    member = await message.channel.guild.fetch_member(int(match.group("user_id")))
    send_message = user_command[len(match.group(0)) :].strip()
    author_name = message.author.nick or message.author.name
    if member and send_message:
        await member.send(f"{author_name} replied:\n{send_message}")


COMMANDS.add_command(
    "send",
    cmd_func=send,
    help_summary="send a message to a user using `send @USER ...`",
    help_full="send a message to a user using `send @USER ...`\nE.g: `send @steve Hello world!`",
)
