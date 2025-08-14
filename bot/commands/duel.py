import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import re
from bot.utils.embeds import EmbedBuilder
from bot.utils.database import Database
from bot.utils.scheduler import DuelScheduler

class DuelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.embed_builder = EmbedBuilder()
        self.scheduler = DuelScheduler(bot)
    
    def is_admin(self, interaction: discord.Interaction) -> bool:
        """Check if user has administrator permissions"""
        if hasattr(interaction.user, 'guild_permissions'):
            return interaction.user.guild_permissions.administrator
        return False
    
    @app_commands.command(name="duel", description="Schedule a duel between two players (Admin only)")
    @app_commands.describe(
        player1="First player",
        player2="Second player", 
        day="Day (1-31)",
        hour="Hour (0-23)",
        minute="Minute (0-59)"
    )
    async def schedule_duel(
        self,
        interaction: discord.Interaction,
        player1: discord.Member,
        player2: discord.Member,
        day: int,
        hour: int,
        minute: int
    ):
        """Schedule a duel between two players"""
        if not self.is_admin(interaction):
            await interaction.response.send_message(
                "❌ Only administrators can schedule duels!", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Validate players are registered
        p1_data = self.db.get_player(player1.id)
        p2_data = self.db.get_player(player2.id)
        
        if not p1_data:
            embed = self.embed_builder.error_embed(
                "Player Not Registered",
                f"{player1.mention} is not registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        if not p2_data:
            embed = self.embed_builder.error_embed(
                "Player Not Registered", 
                f"{player2.mention} is not registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Validate same player
        if player1.id == player2.id:
            embed = self.embed_builder.error_embed(
                "Invalid Duel",
                "A player cannot duel themselves!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Validate date/time
        try:
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month
            
            # Handle month overflow
            if day < current_date.day and current_month == 12:
                duel_date = datetime(current_year + 1, 1, day, hour, minute)
            elif day < current_date.day:
                duel_date = datetime(current_year, current_month + 1, day, hour, minute)
            else:
                duel_date = datetime(current_year, current_month, day, hour, minute)
            
            # Ensure duel is in the future
            if duel_date <= current_date:
                embed = self.embed_builder.error_embed(
                    "Invalid Date",
                    "Duel must be scheduled for a future date and time!"
                )
                await interaction.followup.send(embed=embed)
                return
                
        except ValueError as e:
            embed = self.embed_builder.error_embed(
                "Invalid Date/Time",
                f"Please check your date and time values: {str(e)}"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Create duel record
        duel_id = f"{player1.id}_{player2.id}_{int(duel_date.timestamp())}"
        duel_data = {
            "id": duel_id,
            "player1_id": player1.id,
            "player2_id": player2.id,
            "player1_name": player1.display_name,
            "player2_name": player2.display_name,
            "scheduled_time": duel_date.isoformat(),
            "timestamp": int(duel_date.timestamp()),
            "status": "scheduled",
            "scheduled_by": interaction.user.id,
            "created_at": discord.utils.utcnow().isoformat(),
            "reminder_sent": False
        }
        
        self.db.add_duel(duel_id, duel_data)
        
        # Create luxury duel announcement embed
        embed = self.embed_builder.duel_embed(
            "⚔️ EPIC DUEL SCHEDULED!",
            "A legendary battle has been arranged!"
        )
        
        # Fighter information
        embed.add_field(
            name="🥊 Fighter 1",
            value=f"**{player1.mention}**\n"
                  f"🏆 **Wins:** {p1_data['wins']}\n"
                  f"💀 **Losses:** {p1_data['losses']}\n"
                  f"⚔️ **Kills:** {p1_data['kills']}\n"
                  f"📊 **K/D:** {(p1_data['kills'] / max(1, p1_data['deaths'])):.2f}",
            inline=True
        )
        
        embed.add_field(
            name="🆚",
            value="**VS**\n\n🔥⚡🔥\n\n**CLASH**",
            inline=True
        )
        
        embed.add_field(
            name="🥊 Fighter 2",
            value=f"**{player2.mention}**\n"
                  f"🏆 **Wins:** {p2_data['wins']}\n"
                  f"💀 **Losses:** {p2_data['losses']}\n"
                  f"⚔️ **Kills:** {p2_data['kills']}\n"
                  f"📊 **K/D:** {(p2_data['kills'] / max(1, p2_data['deaths'])):.2f}",
            inline=True
        )
        
        # Duel details
        embed.add_field(
            name="⏰ Duel Time",
            value=f"<t:{int(duel_date.timestamp())}:F>\n"
                  f"<t:{int(duel_date.timestamp())}:R>\n\n"
                  f"🌟 **Countdown:** <t:{int(duel_date.timestamp())}:t>",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Arena Details",
            value=f"**Server IP:** {self.bot.server_ip}\n"
                  f"**Port:** {self.bot.server_port}\n"
                  f"**Arena:** BombSquad Tournament\n"
                  f"**Mode:** 1v1 Elimination",
            inline=True
        )
        
        embed.add_field(
            name="📋 Duel Rules",
            value="• Be online 5 minutes early\n"
                  "• No cheating or exploits\n" 
                  "• Best of 3 rounds\n"
                  "• Admin will record results",
            inline=True
        )
        
        # Add rivalry stats if players have faced before
        previous_duels = [d for d in self.db.get_all_duels().values() 
                         if (d['player1_id'] == player1.id and d['player2_id'] == player2.id) or
                            (d['player1_id'] == player2.id and d['player2_id'] == player1.id)]
        
        if previous_duels:
            embed.add_field(
                name="📈 Head-to-Head History",
                value=f"**Previous Encounters:** {len(previous_duels)}\n"
                      f"**Series Record:** Coming soon!\n"
                      f"**Rivalry Level:** 🔥 HEATED",
                inline=False
            )
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/856550982005465108.png")
        embed.set_footer(text=f"Scheduled by {interaction.user.display_name} • Duel ID: {duel_id[:8]}")
        
        await interaction.followup.send(embed=embed)
        
        # Send private messages to both players
        try:
            # Message to player 1
            dm_embed1 = self.embed_builder.duel_notification_embed(
                "⚔️ You Have Been Challenged!",
                f"Your duel against {player2.mention} has been scheduled!"
            )
            dm_embed1.add_field(
                name="🥊 Your Opponent",
                value=f"**{player2.display_name}**\n"
                      f"Record: {p2_data['wins']}W-{p2_data['losses']}L\n"
                      f"K/D: {(p2_data['kills'] / max(1, p2_data['deaths'])):.2f}",
                inline=True
            )
            dm_embed1.add_field(
                name="⏰ Battle Time",
                value=f"<t:{int(duel_date.timestamp())}:F>\n"
                      f"<t:{int(duel_date.timestamp())}:R>",
                inline=True
            )
            dm_embed1.add_field(
                name="🎮 Connection Info",
                value=f"**Server:** {self.bot.server_ip}:{self.bot.server_port}\n"
                      f"**Be online 5 minutes early!**",
                inline=False
            )
            await player1.send(embed=dm_embed1)
            
            # Message to player 2
            dm_embed2 = self.embed_builder.duel_notification_embed(
                "⚔️ You Have Been Challenged!",
                f"Your duel against {player1.mention} has been scheduled!"
            )
            dm_embed2.add_field(
                name="🥊 Your Opponent", 
                value=f"**{player1.display_name}**\n"
                      f"Record: {p1_data['wins']}W-{p1_data['losses']}L\n"
                      f"K/D: {(p1_data['kills'] / max(1, p1_data['deaths'])):.2f}",
                inline=True
            )
            dm_embed2.add_field(
                name="⏰ Battle Time",
                value=f"<t:{int(duel_date.timestamp())}:F>\n"
                      f"<t:{int(duel_date.timestamp())}:R>",
                inline=True
            )
            dm_embed2.add_field(
                name="🎮 Connection Info", 
                value=f"**Server:** {self.bot.server_ip}:{self.bot.server_port}\n"
                      f"**Be online 5 minutes early!**",
                inline=False
            )
            await player2.send(embed=dm_embed2)
            
        except discord.Forbidden:
            # Add note about DM failure
            note_embed = self.embed_builder.warning_embed(
                "📬 DM Notification Issue",
                "One or both players may have DMs disabled. Please check the server for duel details."
            )
            await interaction.followup.send(embed=note_embed, ephemeral=True)
    
    @app_commands.command(name="duels", description="View upcoming scheduled duels")
    async def view_duels(self, interaction: discord.Interaction):
        """View all upcoming duels"""
        await interaction.response.defer()
        
        duels = self.db.get_all_duels()
        upcoming_duels = [d for d in duels.values() if d['status'] == 'scheduled']
        
        if not upcoming_duels:
            embed = self.embed_builder.info_embed(
                "No Scheduled Duels",
                "There are currently no upcoming duels scheduled.\nAdministrators can schedule duels using `/duel`."
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Sort by scheduled time
        upcoming_duels.sort(key=lambda x: x['timestamp'])
        
        embed = self.embed_builder.duel_list_embed(
            "📅 Upcoming Duels",
            f"{len(upcoming_duels)} epic battles await!"
        )
        
        for i, duel in enumerate(upcoming_duels[:10], 1):  # Show max 10 duels
            try:
                player1 = self.bot.get_user(duel['player1_id'])
                player2 = self.bot.get_user(duel['player2_id'])
                
                p1_name = player1.display_name if player1 else duel['player1_name']
                p2_name = player2.display_name if player2 else duel['player2_name']
                
                duel_time = f"<t:{duel['timestamp']}:F>"
                relative_time = f"<t:{duel['timestamp']}:R>"
                
                embed.add_field(
                    name=f"⚔️ Duel #{i}",
                    value=f"**{p1_name}** 🆚 **{p2_name}**\n"
                          f"⏰ {duel_time}\n"
                          f"📅 {relative_time}\n"
                          f"🆔 `{duel['id'][:8]}`",
                    inline=True
                )
            except:
                continue
        
        embed.add_field(
            name="🎮 Arena Information",
            value=f"**Server:** {self.bot.server_ip}:{self.bot.server_port}\n"
                  f"**Tournament Mode:** Active\n"
                  f"**Reminders:** 5 minutes before each duel",
            inline=False
        )
        
        embed.set_footer(text="🔔 You'll receive automatic reminders for your scheduled duels")
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="cancel_duel", description="Cancel a scheduled duel (Admin only)")
    @app_commands.describe(duel_id="The duel ID to cancel (first 8 characters)")
    async def cancel_duel(self, interaction: discord.Interaction, duel_id: str):
        """Cancel a scheduled duel"""
        if not self.is_admin(interaction):
            await interaction.response.send_message(
                "❌ Only administrators can cancel duels!", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Find duel by partial ID
        all_duels = self.db.get_all_duels()
        matching_duel = None
        
        for full_id, duel in all_duels.items():
            if full_id.startswith(duel_id):
                matching_duel = duel
                break
        
        if not matching_duel:
            embed = self.embed_builder.error_embed(
                "Duel Not Found",
                f"No scheduled duel found with ID starting with `{duel_id}`"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Remove the duel
        self.db.remove_duel(matching_duel['id'])
        
        # Create cancellation embed
        embed = self.embed_builder.warning_embed(
            "🚫 Duel Cancelled",
            "The scheduled duel has been cancelled."
        )
        
        try:
            player1 = self.bot.get_user(matching_duel['player1_id'])
            player2 = self.bot.get_user(matching_duel['player2_id'])
            
            p1_name = player1.display_name if player1 else matching_duel['player1_name']
            p2_name = player2.display_name if player2 else matching_duel['player2_name']
            
            embed.add_field(
                name="⚔️ Cancelled Duel",
                value=f"**{p1_name}** vs **{p2_name}**\n"
                      f"**Originally Scheduled:** <t:{matching_duel['timestamp']}:F>\n"
                      f"**Cancelled By:** {interaction.user.mention}",
                inline=False
            )
            
            # Notify players
            cancellation_embed = self.embed_builder.warning_embed(
                "🚫 Your Duel Has Been Cancelled",
                f"Your scheduled duel has been cancelled by an administrator."
            )
            
            try:
                if player1:
                    await player1.send(embed=cancellation_embed)
                if player2:
                    await player2.send(embed=cancellation_embed)
            except discord.Forbidden:
                pass
                
        except:
            embed.add_field(
                name="⚔️ Cancelled Duel",
                value=f"**Duel ID:** {matching_duel['id'][:8]}\n"
                      f"**Cancelled By:** {interaction.user.mention}",
                inline=False
            )
        
        await interaction.followup.send(embed=embed)
