import os
import asyncio
import threading
from bot.bot import DuelLordsBot
from keep_alive import keep_alive

def start_web_server():
    """Start the web dashboard server"""
    from web.app import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def main():
    """Main entry point for the Duel Lords bot"""
    # Start the keep-alive server in a separate thread
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # Start web dashboard in separate thread
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    # Get Discord token from environment variable
    discord_token = os.getenv("DISCORD_TOKEN")
    if not discord_token:
        print("❌ Error: DISCORD_TOKEN environment variable not found!")
        print("Please set your Discord bot token in the environment variables.")
        return
    
    # Create and run the bot
    bot = DuelLordsBot()
    
    try:
        print("🚀 Starting Duel Lords Bot...")
        asyncio.run(bot.start(discord_token))
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == "__main__":
    main()
