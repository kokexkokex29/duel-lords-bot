import asyncio
import discord
from datetime import datetime, timedelta
from bot.utils.database import Database
from bot.utils.embeds import EmbedBuilder

class DuelScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.embed_builder = EmbedBuilder()
        self.reminder_sent = set()  # Track sent reminders to avoid duplicates
    
    async def check_reminders(self):
        """Check for upcoming duels and send reminders"""
        try:
            current_time = datetime.utcnow()
            upcoming_duels = self.db.get_upcoming_duels()
            
            for duel in upcoming_duels:
                duel_time = datetime.fromisoformat(duel['scheduled_time'])
                time_until_duel = duel_time - current_time
                
                # Send reminder 5 minutes before duel
                if (timedelta(minutes=4, seconds=30) <= time_until_duel <= timedelta(minutes=5, seconds=30) 
                    and duel['id'] not in self.reminder_sent):
                    
                    await self._send_duel_reminder(duel)
                    self.reminder_sent.add(duel['id'])
                
                # Clean up old reminders
                elif time_until_duel <= timedelta(0):
                    if duel['id'] in self.reminder_sent:
                        self.reminder_sent.remove(duel['id'])
                    
                    # Optionally mark duel as started/completed
                    duel['status'] = 'in_progress'
                    self.db.update_duel(duel['id'], duel)
        
        except Exception as e:
            print(f"❌ Scheduler error: {e}")
    
    async def _send_duel_reminder(self, duel: dict):
        """Send luxury reminder message to duel participants"""
        try:
            # Get players
            player1 = self.bot.get_user(duel['player1_id'])
            player2 = self.bot.get_user(duel['player2_id'])
            
            if not player1 or not player2:
                return
            
            # Get player stats for reminder
            p1_data = self.db.get_player(player1.id)
            p2_data = self.db.get_player(player2.id)
            
            # Create luxury reminder embed
            reminder_embed = self.embed_builder.duel_reminder_embed(
                "⚡ FINAL WARNING - DUEL STARTING SOON!",
                "🔥 **Your epic battle begins in 5 minutes!** 🔥"
            )
            
            reminder_embed.add_field(
                name="⚔️ Battle Details",
                value=f"**{player1.display_name}** 🆚 **{player2.display_name}**\n"
                      f"**Starts:** <t:{duel['timestamp']}:t>\n"
                      f"**In:** <t:{duel['timestamp']}:R>\n\n"
                      f"🎯 **This is it - the moment of truth!**",
                inline=False
            )
            
            reminder_embed.add_field(
                name="🎮 Connection Info",
                value=f"**Server IP:** {self.bot.server_ip}\n"
                      f"**Port:** {self.bot.server_port}\n"
                      f"**Full Address:** {self.bot.server_ip}:{self.bot.server_port}\n\n"
                      f"🚨 **CONNECT NOW!**",
                inline=True
            )
            
            reminder_embed.add_field(
                name="📋 Pre-Battle Checklist",
                value="✅ Connect to server\n"
                      "✅ Check your internet connection\n"
                      "✅ Close other applications\n"
                      "✅ Prepare for victory!\n"
                      "✅ May the best fighter win!",
                inline=True
            )
            
            # Add opponent stats for strategy
            reminder_embed.add_field(
                name="🎯 Know Your Enemy",
                value=f"**Opponent Record:** {p2_data['wins'] if p2_data else 0}W-{p2_data['losses'] if p2_data else 0}L\n"
                      f"**K/D Ratio:** {(p2_data['kills'] / max(1, p2_data['deaths']) if p2_data else 0):.2f}\n"
                      f"**Threat Level:** {'🔥 HIGH' if (p2_data and p2_data['wins'] > 5) else '⚡ MODERATE'}\n"
                      f"**Strategy:** Fight smart, stay focused!",
                inline=False
            )
            
            # Add motivational quotes
            motivational_quotes = [
                "*\"I fear not the man who has practiced 10,000 kicks once, but I fear the man who has practiced one kick 10,000 times.\"* - Bruce Lee",
                "*\"Victory is reserved for those who are willing to pay its price.\"* - Sun Tzu", 
                "*\"The way to get started is to quit talking and begin doing.\"* - Walt Disney",
                "*\"Champions train, losers complain.\"* - Unknown",
                "*\"It's not whether you get knocked down, it's whether you get up.\"* - Vince Lombardi"
            ]
            
            import random
            quote = random.choice(motivational_quotes)
            
            reminder_embed.add_field(
                name="💪 Battle Inspiration",
                value=quote,
                inline=False
            )
            
            # Create personalized messages for each player
            
            # Message for Player 1
            p1_embed = reminder_embed.copy()
            p1_embed.add_field(
                name=f"🥊 Your Stats vs {player2.display_name}",
                value=f"**Your Record:** {p1_data['wins'] if p1_data else 0}W-{p1_data['losses'] if p1_data else 0}L\n"
                      f"**Your K/D:** {(p1_data['kills'] / max(1, p1_data['deaths']) if p1_data else 0):.2f}\n"
                      f"**Confidence Level:** {'🔥 READY TO DOMINATE!' if (p1_data and p1_data['wins'] >= p2_data['wins']) else '⚡ HUNGRY FOR VICTORY!'}",
                inline=False
            )
            
            # Message for Player 2
            p2_embed = reminder_embed.copy()
            p2_embed.add_field(
                name=f"🥊 Your Stats vs {player1.display_name}",
                value=f"**Your Record:** {p2_data['wins'] if p2_data else 0}W-{p2_data['losses'] if p2_data else 0}L\n"
                      f"**Your K/D:** {(p2_data['kills'] / max(1, p2_data['deaths']) if p2_data else 0):.2f}\n"
                      f"**Confidence Level:** {'🔥 READY TO DOMINATE!' if (p2_data and p2_data['wins'] >= p1_data['wins']) else '⚡ HUNGRY FOR VICTORY!'}",
                inline=False
            )
            
            # Send reminders
            try:
                await player1.send(embed=p1_embed)
                print(f"📨 Reminder sent to {player1.display_name}")
            except discord.Forbidden:
                print(f"❌ Cannot send DM to {player1.display_name}")
            
            try:
                await player2.send(embed=p2_embed)
                print(f"📨 Reminder sent to {player2.display_name}")
            except discord.Forbidden:
                print(f"❌ Cannot send DM to {player2.display_name}")
            
            # Mark reminder as sent in database
            duel['reminder_sent'] = True
            self.db.update_duel(duel['id'], duel)
            
            print(f"⏰ Duel reminder sent: {player1.display_name} vs {player2.display_name}")
        
        except Exception as e:
            print(f"❌ Error sending duel reminder: {e}")
    
    async def send_immediate_duel_notification(self, duel: dict):
        """Send immediate notification when duel starts"""
        try:
            player1 = self.bot.get_user(duel['player1_id'])
            player2 = self.bot.get_user(duel['player2_id'])
            
            if not player1 or not player2:
                return
            
            # Create "duel starting now" embed
            now_embed = self.embed_builder.duel_reminder_embed(
                "🚨 DUEL STARTING NOW!",
                "⚔️ **The battle begins! Connect to the server immediately!** ⚔️"
            )
            
            now_embed.add_field(
                name="🎮 CONNECT NOW!",
                value=f"**Server:** {self.bot.server_ip}:{self.bot.server_port}\n"
                      f"**Players:** {player1.mention} 🆚 {player2.mention}\n"
                      f"**Time:** RIGHT NOW!\n\n"
                      f"🔥 **THE FIGHT IS ON!**",
                inline=False
            )
            
            # Send to both players
            try:
                await player1.send(embed=now_embed)
                await player2.send(embed=now_embed)
            except discord.Forbidden:
                pass
            
        except Exception as e:
            print(f"❌ Error sending immediate duel notification: {e}")
    
    def cleanup_old_reminders(self):
        """Clean up reminder tracking for old duels"""
        try:
            current_time = datetime.utcnow()
            completed_duels = []
            
            # Find duels that are over
            for duel_id in list(self.reminder_sent):
                duel = self.db.get_duel(duel_id)
                if duel:
                    duel_time = datetime.fromisoformat(duel['scheduled_time'])
                    if duel_time < current_time - timedelta(hours=1):  # 1 hour after duel
                        completed_duels.append(duel_id)
            
            # Remove from tracking
            for duel_id in completed_duels:
                self.reminder_sent.discard(duel_id)
            
            if completed_duels:
                print(f"🧹 Cleaned up {len(completed_duels)} old duel reminders")
        
        except Exception as e:
            print(f"❌ Error cleaning up reminders: {e}")
