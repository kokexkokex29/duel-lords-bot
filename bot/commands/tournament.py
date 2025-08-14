import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.embeds import EmbedBuilder
from bot.utils.database import Database
from bot.utils.translations import Translator

class TournamentCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.embed_builder = EmbedBuilder()
        self.translator = Translator()
    
    @app_commands.command(name="ip", description="Get BombSquad server connection info")
    async def server_ip(self, interaction: discord.Interaction):
        """Display server IP and port information"""
        embed = self.embed_builder.info_embed(
            "🎮 BombSquad Server Information",
            "Connect to our official tournament server!"
        )
        embed.add_field(
            name="🌐 Connection Details",
            value=f"**IP Address:** `{self.bot.server_ip}`\n"
                  f"**Port:** `{self.bot.server_port}`\n"
                  f"**Full Address:** `{self.bot.server_ip}:{self.bot.server_port}`",
            inline=False
        )
        embed.add_field(
            name="📋 How to Connect",
            value="1. Open BombSquad\n"
                  "2. Go to Play → Network → Connect by Address\n"
                  "3. Enter the IP address above\n"
                  "4. Click Connect and join the tournament!",
            inline=False
        )
        embed.add_field(
            name="⚡ Server Status",
            value="🟢 **Online** - Ready for duels!\n"
                  "🏆 Tournament Mode Active\n"
                  "👥 Players Welcome",
            inline=False
        )
        embed.set_footer(text="Good luck in your duels!")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="fighters", description="View all tournament fighters")
    async def fighters(self, interaction: discord.Interaction):
        """Display all registered tournament fighters"""
        await interaction.response.defer()
        
        players = self.db.get_all_players()
        
        if not players:
            embed = self.embed_builder.warning_embed(
                "No Fighters Found",
                "No players are currently registered for the tournament.\nAdministrators can register players using `/register`."
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Sort players by total wins
        sorted_players = sorted(players.values(), key=lambda x: x['wins'], reverse=True)
        
        embed = self.embed_builder.tournament_embed(
            "⚔️ Tournament Fighters",
            f"Currently {len(players)} brave warriors are registered!"
        )
        
        # Add players in chunks of 10
        for i in range(0, len(sorted_players), 10):
            chunk = sorted_players[i:i+10]
            fighter_list = ""
            
            for j, player in enumerate(chunk, i+1):
                try:
                    user = self.bot.get_user(player['user_id'])
                    name = user.mention if user else player['display_name']
                    wins = player['wins']
                    losses = player['losses']
                    kd_ratio = player['kills'] / max(1, player['deaths'])
                    
                    fighter_list += f"{j}. {name}\n"
                    fighter_list += f"   🏆 {wins}W-{losses}L | K/D: {kd_ratio:.1f}\n\n"
                except:
                    fighter_list += f"{j}. {player['display_name']}\n"
                    fighter_list += f"   🏆 {player['wins']}W-{player['losses']}L\n\n"
            
            field_name = f"🥊 Fighters {i+1}-{min(i+10, len(sorted_players))}"
            embed.add_field(name=field_name, value=fighter_list, inline=True)
        
        # Add tournament stats
        total_wins = sum(p['wins'] for p in players.values())
        total_kills = sum(p['kills'] for p in players.values())
        
        embed.add_field(
            name="📊 Tournament Statistics",
            value=f"**Total Matches:** {total_wins}\n"
                  f"**Total Eliminations:** {total_kills}\n"
                  f"**Active Fighters:** {len(players)}\n"
                  f"**Server:** {self.bot.server_ip}:{self.bot.server_port}",
            inline=False
        )
        
        embed.set_footer(text="Use /stats @user to view detailed player statistics")
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="leaderboard", description="View tournament leaderboard")
    @app_commands.describe(sort_by="Sort leaderboard by specific stat")
    @app_commands.choices(sort_by=[
        app_commands.Choice(name="Wins", value="wins"),
        app_commands.Choice(name="Win Rate", value="win_rate"),
        app_commands.Choice(name="Kills", value="kills"),
        app_commands.Choice(name="K/D Ratio", value="kd_ratio"),
        app_commands.Choice(name="Total Matches", value="matches")
    ])
    async def leaderboard(self, interaction: discord.Interaction, sort_by: str = "wins"):
        """Display the tournament leaderboard"""
        await interaction.response.defer()
        
        players = self.db.get_all_players()
        
        if not players:
            embed = self.embed_builder.warning_embed(
                "Empty Leaderboard",
                "No players are registered yet!\nAdministrators can register players using `/register`."
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Calculate additional stats and sort
        player_stats = []
        for player in players.values():
            total_matches = player['wins'] + player['losses'] + player['draws']
            win_rate = (player['wins'] / max(1, total_matches)) * 100
            kd_ratio = player['kills'] / max(1, player['deaths'])
            
            player_stats.append({
                **player,
                'total_matches': total_matches,
                'win_rate': win_rate,
                'kd_ratio': kd_ratio
            })
        
        # Sort by selected criteria
        if sort_by == "win_rate":
            sorted_players = sorted(player_stats, key=lambda x: x['win_rate'], reverse=True)
        elif sort_by == "kd_ratio":
            sorted_players = sorted(player_stats, key=lambda x: x['kd_ratio'], reverse=True)
        elif sort_by == "matches":
            sorted_players = sorted(player_stats, key=lambda x: x['total_matches'], reverse=True)
        else:
            sorted_players = sorted(player_stats, key=lambda x: x[sort_by], reverse=True)
        
        embed = self.embed_builder.leaderboard_embed(
            "🏆 Tournament Leaderboard",
            f"Top fighters sorted by {sort_by.replace('_', ' ').title()}"
        )
        
        # Add top 10 players
        leaderboard_text = ""
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        
        for i, player in enumerate(sorted_players[:10]):
            try:
                user = self.bot.get_user(player['user_id'])
                name = user.display_name if user else player['display_name']
                medal = medals[i] if i < len(medals) else "🏅"
                
                leaderboard_text += f"{medal} **{name}**\n"
                leaderboard_text += f"   🏆 {player['wins']}W-{player['losses']}L-{player['draws']}D"
                leaderboard_text += f" | Win Rate: {player['win_rate']:.1f}%\n"
                leaderboard_text += f"   ⚔️ {player['kills']} kills | K/D: {player['kd_ratio']:.2f}\n\n"
            except:
                continue
        
        embed.add_field(
            name="📊 Top Fighters",
            value=leaderboard_text or "No data available",
            inline=False
        )
        
        # Add tournament summary
        total_players = len(players)
        total_matches = sum(p['wins'] + p['losses'] + p['draws'] for p in players.values())
        total_kills = sum(p['kills'] for p in players.values())
        
        embed.add_field(
            name="🎯 Tournament Summary",
            value=f"**Total Players:** {total_players}\n"
                  f"**Matches Played:** {total_matches // 2}\n"
                  f"**Total Eliminations:** {total_kills}\n"
                  f"**Most Active Player:** {sorted_players[0]['display_name'] if sorted_players else 'N/A'}",
            inline=True
        )
        
        embed.add_field(
            name="🎮 Server Info",
            value=f"**IP:** {self.bot.server_ip}\n"
                  f"**Port:** {self.bot.server_port}\n"
                  f"**Status:** 🟢 Online",
            inline=True
        )
        
        embed.set_footer(text="🔄 Leaderboard updates in real-time | Use /stats for detailed player info")
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="tournament_info", description="Display comprehensive tournament information")
    async def tournament_info(self, interaction: discord.Interaction):
        """Display detailed tournament information"""
        await interaction.response.defer()
        
        players = self.db.get_all_players()
        duels = self.db.get_all_duels()
        
        embed = self.embed_builder.tournament_embed(
            "🏆 Duel Lords Tournament",
            "Welcome to the ultimate BombSquad tournament experience!"
        )
        
        # Tournament statistics
        total_players = len(players)
        total_duels = len(duels)
        completed_duels = len([d for d in duels.values() if d.get('status') == 'completed'])
        pending_duels = len([d for d in duels.values() if d.get('status') == 'scheduled'])
        
        embed.add_field(
            name="📊 Tournament Statistics",
            value=f"**Registered Fighters:** {total_players}\n"
                  f"**Total Duels:** {total_duels}\n"
                  f"**Completed:** {completed_duels}\n"
                  f"**Scheduled:** {pending_duels}",
            inline=True
        )
        
        # Server information
        embed.add_field(
            name="🎮 BombSquad Server",
            value=f"**IP:** {self.bot.server_ip}\n"
                  f"**Port:** {self.bot.server_port}\n"
                  f"**Status:** 🟢 Active\n"
                  f"**Mode:** Tournament",
            inline=True
        )
        
        # Available commands
        embed.add_field(
            name="⚡ Quick Commands",
            value="• `/fighters` - View all fighters\n"
                  "• `/leaderboard` - Tournament rankings\n"
                  "• `/stats @user` - Player statistics\n"
                  "• `/duel` - Schedule a duel (Admin)\n"
                  "• `/ip` - Server connection info",
            inline=False
        )
        
        # Top performer
        if players:
            top_player = max(players.values(), key=lambda x: x['wins'])
            try:
                user = self.bot.get_user(top_player['user_id'])
                top_name = user.display_name if user else top_player['display_name']
                embed.add_field(
                    name="👑 Current Champion",
                    value=f"**{top_name}**\n"
                          f"🏆 {top_player['wins']} wins\n"
                          f"⚔️ {top_player['kills']} kills\n"
                          f"📈 {(top_player['wins'] / max(1, top_player['wins'] + top_player['losses'] + top_player['draws']) * 100):.1f}% win rate",
                    inline=True
                )
            except:
                pass
        
        embed.add_field(
            name="🎯 How to Participate",
            value="1. Get registered by an admin using `/register`\n"
                  "2. Connect to the BombSquad server\n"
                  "3. Wait for duel scheduling\n"
                  "4. Fight and earn your place on the leaderboard!",
            inline=False
        )
        
        embed.set_footer(text="May the best warrior win! Good luck in your duels.")
        
        await interaction.followup.send(embed=embed)
