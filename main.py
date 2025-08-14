import os
import asyncio
import threading
from bot.bot import DuelLordsBot
from keep_alive import keep_alive

def start_web_server():
    """Start the web dashboard server"""
    import time
    time.sleep(3)  # Wait a bit before starting web server
    try:
        from web.app import app
        # Use PORT from environment (Render assigns this)
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Web server error: {e}")

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
    
    # Create and run the bot with rate limit handling
    bot = DuelLordsBot()
    
    # Bot with retry mechanism for rate limits
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"🚀 Starting Duel Lords Bot... (Attempt {retry_count + 1})")
            asyncio.run(bot.start(discord_token))
            break  # If successful, exit the loop
        except KeyboardInterrupt:
            print("\n⏹️ Bot stopped by user")
            break
        except Exception as e:
            retry_count += 1
            if "429" in str(e) or "rate limit" in str(e).lower():
                print(f"⏳ Bot rate limited by Discord (Attempt {retry_count}/{max_retries})")
                if retry_count < max_retries:
                    print("💡 Waiting 60 seconds before retry...")
                    import time
                    time.sleep(60)
                else:
                    print("💡 Max retries reached. Bot will stay alive with web server.")
            else:
                print(f"❌ Error running bot: {e}")
                if retry_count < max_retries:
                    print("🔄 Retrying in 30 seconds...")
                    import time
                    time.sleep(30)
                break
    
    # Keep the process alive for the web server
    print("✅ Web server is running. Application will stay alive.")
    try:
        while True:
            import time
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n⏹️ Application stopped by user")

if __name__ == "__main__":
    main()
