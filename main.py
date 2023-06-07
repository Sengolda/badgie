import sys
import json
import asyncio

import discord
from discord import app_commands
from discord.utils import oauth_url

if not sys.version_info[:2] >= (3, 8):
    print(
        "Python 3.8 or higher must be installed to run this program. If it is installed try `python3 main.py`",
        file=sys.stderr,
    )
    sys.exit(1)


print(
    """

██████╗░░█████╗░██████╗░░██████╗░██╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝░██║██╔════╝
██████╦╝███████║██║░░██║██║░░██╗░██║█████╗░░
██╔══██╗██╔══██║██║░░██║██║░░╚██╗██║██╔══╝░░
██████╦╝██║░░██║██████╔╝╚██████╔╝██║███████╗
╚═════╝░╚═╝░░╚═╝╚═════╝░░╚═════╝░╚═╝╚══════╝
"""
)

config = {}
try:
    with open("./config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    pass

token = config.get("token")
if not token:
    print("Token is missing please input token")
    token = input("token:  ")
    config["token"] = token


to_sync_guild = None
guild_id = config.get("guild_id")

if guild_id is None:
    guild_id = input(
        "Input the id of the guild you will be using (this is not required but putting the id would be faster):  "
    )
    guild_id = int(guild_id) if guild_id else 0
    config["guild_id"] = guild_id
    to_sync_guild = discord.Object(id=guild_id)

with open("./config.json", "w") as f:
    json.dump(config, f, indent=4)


class BadgieBadgeGiver(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(
            "Badgie Giver is ready!\n\n Use this to invite the bot:  ",
            oauth_url(self.user.id, permissions=discord.Permissions.all()),
        )

    def run(self):
        super().run(token)

    async def setup_hook(self):
        if not to_sync_guild or not to_sync_guild.id:
            await self.tree.sync()
        else:
            self.tree.copy_global_to(guild=to_sync_guild)
            await self.tree.sync(guild=to_sync_guild)


client = BadgieBadgeGiver()


@client.tree.command()
async def hello(interaction: discord.Interaction):
    msg = (
        f"Hi, {interaction.user.mention},",
        "please visit https://discord.com/developers/active-developer to get your badge, if you don't see it just wait 24 hours and you will see it.",
        "if you still do not get it even after that time period please open an issue at: ",
        "https://github.com/sengolda/badgie/issues/"
    )

    await interaction.response.send_message("\n".join(msg))


client.run()
