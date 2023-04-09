import discord


class DiscordBot(discord.Client):
    async def on_message(self, message :discord.Message):
        if message.author == self.user:
            return
        
        print(message)

        await message.channel.send("Панч лох")
    
    async def on_ready(self):
        print(f"{self.user} has connected to Discord")




def start(token : str):
    intents = discord.Intents.default()
    intents.message_content = True
    client  = DiscordBot(intents=intents)

    client.run(token)