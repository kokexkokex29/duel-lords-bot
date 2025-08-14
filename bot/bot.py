import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime
from bot.commands.admin import AdminCommands
from bot.commands.tournament import TournamentCommands
from bot.commands.duel import DuelCommands
from bot.commands.stats import StatsCommands
from bot.utils.database import Database
from bot.utils.scheduler import DuelScheduler
from bot.utils.translations import Translator

class DuelLordsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            description="Duel Lords - Ultimate BombSquad Tournament Bot"
        )
        
        # Initialize components
        self.db = Database()
        self.scheduler = DuelScheduler(self)
        self.translator = Translator()
        
        # Bot configuration
        self.server_ip = "18.228.228.44"
        self.server_port = "3827"
        
    async def setup_hook(self):
        """Setup hook called when bot is ready"""
        print("🔧 Setting up bot commands...")
        
        # Add cogs
        await self.add_cog(AdminCommands(self))
        await self.add_cog(TournamentCommands(self))
        await self.add_cog(DuelCommands(self))
        await self.add_cog(StatsCommands(self))
        
        # Start scheduler
        self.scheduler_task.start()
        
        # Sync slash commands (only once)
        if not hasattr(self, '_commands_synced'):
            try:
                synced = await self.tree.sync()
                print(f"✅ Synced {len(synced)} slash commands")
                self._commands_synced = True
            except discord.HTTPException as e:
                if e.status == 429:  # Rate limited
                    print(f"⏳ Rate limited, skipping command sync")
                else:
                    print(f"❌ Failed to sync commands: {e}")
            except Exception as e:
                print(f"❌ Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f"🎯 {self.user} is now online!")
        print(f"🏆 Duel Lords Tournament Bot Ready!")
        print(f"📊 Serving {len(self.guilds)} guild(s)")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="BombSquad Tournaments | /help"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)
    
    async def on_application_command_error(self, interaction, error):
        """Handle slash command errors"""
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command!", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ An error occurred: {str(error)}", 
                ephemeral=True
            )
            print(f"Command error: {error}")
    
    @tasks.loop(seconds=30)
    async def scheduler_task(self):
        """Check for scheduled duels and send reminders"""
        try:
            await self.scheduler.check_reminders()
        except Exception as e:
            print(f"❌ Scheduler error: {e}")
    
    @scheduler_task.before_loop
    async def before_scheduler(self):
        """Wait until bot is ready before starting scheduler"""
        await self.wait_until_ready()
