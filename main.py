import os
import DiscordBot

def main(token):
    DiscordBot.start(token)
        
if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if token is None:
        raise Exception("No token provided")
    main(token)