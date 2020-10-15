import discord
import re
from .command_system.command_system import CommandSystem


COMMANDS = CommandSystem()


async def reply(client, user_command, message):
    match = re.match(r"[^<]*<@!?(?P<user_id>\d+)>", user_command)
    member = await message.channel.guild.fetch_member(int(match.group("user_id")))
    reply_message = user_command[len(match.group(0)) :].strip()
    author_name = message.author.nick or message.author.name
    if member and reply_message:
        await member.send(f"{author_name} replied:\n{reply_message}")


COMMANDS.add_command(
    "reply",
    cmd_func=reply,
    help_summary="Reply to a user's message using `reply @USER ...`",
    help_full="Reply to a user's message using `reply @USER ...`\nE.g: `Reply @steve Hello world!`",
)
