import discord
from .Balaboba import balaboba_text
from typing import Any
from .CommandProcessor import CommandProcessor


class DiscordBot(discord.Client):
    def __init__(self, *, intents: discord.Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self._command_processor = CommandProcessor()
        self._command_processor.register("!балабоба", self.on_balaboba)

    async def on_balaboba(self, rest_text: str, message: discord.Message):
        text = await balaboba_text(rest_text)

        await message.channel.send(text)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        await self._command_processor.process(message.content, message)

    async def on_ready(self):
        print(f"{self.user} has connected to Discord")


def start(token: str):
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordBot(intents=intents)

    print(client.on_message)

    client.run(token)
