import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.embeds import EmbedBuilder
from bot.utils.database import Database

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.embed_builder = EmbedBuilder()
    
    def is_admin(self, interaction: discord.Interaction) -> bool:
        """Check if user has administrator permissions"""
        if hasattr(interaction.user, 'guild_permissions'):
            return interaction.user.guild_permissions.administrator
        return False
    
    @app_commands.command(name="register", description="Register a new player (Admin only)")
    @app_commands.describe(
        user="The Discord user to register",
        display_name="Display name for the player (optional)"
    )
    async def register_player(
        self, 
        interaction: discord.Interaction, 
        user: discord.Member,
        display_name: str = ""
    ):
        """Register a new player for the tournament"""
        if not self.is_admin(interaction):
            await interaction.response.send_message(
                "❌ Only administrators can register players!", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Use display name or username
        player_name = display_name or user.display_name
        
        # Check if player already exists
        if self.db.get_player(user.id):
            embed = self.embed_builder.error_embed(
                "Player Already Registered",
                f"{user.mention} is already registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Register the player
        player_data = {
            "user_id": user.id,
            "username": user.name,
            "display_name": player_name,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "kills": 0,
            "deaths": 0,
            "kill_count": 0,
            "registered_at": discord.utils.utcnow().isoformat(),
            "registered_by": interaction.user.id
        }
        
        self.db.add_player(user.id, player_data)
        
        # Create success embed
        embed = self.embed_builder.success_embed(
            "🎯 Player Registered Successfully!",
            f"Welcome to Duel Lords Tournament, {user.mention}!"
        )
        embed.add_field(
            name="📊 Player Stats",
            value=f"**Display Name:** {player_name}\n"
                  f"**Wins:** 0\n"
                  f"**Losses:** 0\n"
                  f"**Draws:** 0\n"
                  f"**Kills:** 0\n"
                  f"**Deaths:** 0",
            inline=True
        )
        embed.add_field(
            name="🏆 Tournament Info",
            value=f"**Total Players:** {len(self.db.get_all_players())}\n"
                  f"**Registered By:** {interaction.user.mention}\n"
                  f"**Registration Date:** <t:{int(discord.utils.utcnow().timestamp())}:F>",
            inline=True
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text="Use /stats to view detailed player statistics")
        
        await interaction.followup.send(embed=embed)
        
        # Send welcome message to the registered player
        try:
            welcome_embed = self.embed_builder.info_embed(
                "🎉 Welcome to Duel Lords Tournament!",
                f"You have been registered by {interaction.user.mention}"
            )
            welcome_embed.add_field(
                name="🎮 BombSquad Server",
                value=f"**IP:** {self.bot.server_ip}\n**Port:** {self.bot.server_port}",
                inline=False
            )
            welcome_embed.add_field(
                name="📋 Available Commands",
                value="• `/stats` - View your statistics\n"
                      "• `/leaderboard` - View tournament rankings\n"
                      "• `/ip` - Get server connection info\n"
                      "• `/fighters` - View all tournament fighters",
                inline=False
            )
            await user.send(embed=welcome_embed)
        except discord.Forbidden:
            pass  # User has DMs disabled
    
    @app_commands.command(name="remove", description="Remove a player from tournament (Admin only)")
    @app_commands.describe(user="The Discord user to remove")
    async def remove_player(self, interaction: discord.Interaction, user: discord.Member):
        """Remove a player from the tournament"""
        if not self.is_admin(interaction):
            await interaction.response.send_message(
                "❌ Only administrators can remove players!", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Check if player exists
        player = self.db.get_player(user.id)
        if not player:
            embed = self.embed_builder.error_embed(
                "Player Not Found",
                f"{user.mention} is not registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Remove the player
        self.db.remove_player(user.id)
        
        # Create success embed
        embed = self.embed_builder.warning_embed(
            "🗑️ Player Removed",
            f"{user.mention} has been removed from the tournament!"
        )
        embed.add_field(
            name="📊 Player's Final Stats",
            value=f"**Wins:** {player['wins']}\n"
                  f"**Losses:** {player['losses']}\n"
                  f"**Draws:** {player['draws']}\n"
                  f"**Kills:** {player['kills']}\n"
                  f"**Deaths:** {player['deaths']}",
            inline=True
        )
        embed.add_field(
            name="🏆 Tournament Info",
            value=f"**Remaining Players:** {len(self.db.get_all_players())}\n"
                  f"**Removed By:** {interaction.user.mention}\n"
                  f"**Removal Date:** <t:{int(discord.utils.utcnow().timestamp())}:F>",
            inline=True
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="update", description="Update player statistics (Admin only)")
    @app_commands.describe(
        user="The player to update",
        wins="Number of wins to add",
        losses="Number of losses to add",
        draws="Number of draws to add",
        kills="Number of kills to add",
        deaths="Number of deaths to add"
    )
    async def update_stats(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        wins: int = 0,
        losses: int = 0,
        draws: int = 0,
        kills: int = 0,
        deaths: int = 0
    ):
        """Update player statistics"""
        if not self.is_admin(interaction):
            await interaction.response.send_message(
                "❌ Only administrators can update player stats!", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Check if player exists
        player = self.db.get_player(user.id)
        if not player:
            embed = self.embed_builder.error_embed(
                "Player Not Found",
                f"{user.mention} is not registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Update stats
        old_stats = player.copy()
        player['wins'] += wins
        player['losses'] += losses
        player['draws'] += draws
        player['kills'] += kills
        player['deaths'] += deaths
        player['kill_count'] = player['kills']  # Update kill count
        
        self.db.update_player(user.id, player)
        
        # Create success embed
        embed = self.embed_builder.success_embed(
            "📈 Player Statistics Updated!",
            f"Successfully updated stats for {user.mention}"
        )
        embed.add_field(
            name="📊 Previous Stats",
            value=f"**Wins:** {old_stats['wins']}\n"
                  f"**Losses:** {old_stats['losses']}\n"
                  f"**Draws:** {old_stats['draws']}\n"
                  f"**Kills:** {old_stats['kills']}\n"
                  f"**Deaths:** {old_stats['deaths']}",
            inline=True
        )
        embed.add_field(
            name="📊 New Stats",
            value=f"**Wins:** {player['wins']} (+{wins})\n"
                  f"**Losses:** {player['losses']} (+{losses})\n"
                  f"**Draws:** {player['draws']} (+{draws})\n"
                  f"**Kills:** {player['kills']} (+{kills})\n"
                  f"**Deaths:** {player['deaths']} (+{deaths})",
            inline=True
        )
        embed.add_field(
            name="🏆 Performance",
            value=f"**Total Matches:** {player['wins'] + player['losses'] + player['draws']}\n"
                  f"**Win Rate:** {(player['wins'] / max(1, player['wins'] + player['losses'] + player['draws']) * 100):.1f}%\n"
                  f"**K/D Ratio:** {(player['kills'] / max(1, player['deaths'])):.2f}",
            inline=False
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text=f"Updated by {interaction.user.display_name}")
        
        await interaction.followup.send(embed=embed)
