import os


def main(app_id, public_key):
    
    pass
        
if __name__ == "__main__":
    app_id = os.getenv("DISCORD_BOT_APP_ID")
    public_key = os.getenv("DISCORD_BOT_KEY")
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if app_id is None or public_key is None:
        raise Exception("No public key or app id provided")
    main(app_id, public_key)