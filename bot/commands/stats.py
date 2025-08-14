import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.embeds import EmbedBuilder
from bot.utils.database import Database

class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.embed_builder = EmbedBuilder()
    
    @app_commands.command(name="stats", description="View detailed player statistics")
    @app_commands.describe(user="The player to view stats for (defaults to yourself)")
    async def player_stats(self, interaction: discord.Interaction, user: discord.Member = None):
        """Display detailed player statistics"""
        if user is None:
            user = interaction.user
        
        await interaction.response.defer()
        
        # Get player data
        player = self.db.get_player(user.id)
        
        if not player:
            embed = self.embed_builder.error_embed(
                "Player Not Found",
                f"{user.mention} is not registered in the tournament!\n"
                f"Administrators can register players using `/register`."
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Calculate advanced statistics
        total_matches = player['wins'] + player['losses'] + player['draws']
        win_rate = (player['wins'] / max(1, total_matches)) * 100
        kd_ratio = player['kills'] / max(1, player['deaths'])
        
        # Create luxury stats embed
        embed = self.embed_builder.stats_embed(
            f"📊 {user.display_name}'s Statistics",
            "Complete tournament performance breakdown"
        )
        
        # Set user avatar
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        
        # Basic Stats
        embed.add_field(
            name="🏆 Match Record",
            value=f"**Wins:** {player['wins']} 🟢\n"
                  f"**Losses:** {player['losses']} 🔴\n"
                  f"**Draws:** {player['draws']} 🟡\n"
                  f"**Total Matches:** {total_matches}",
            inline=True
        )
        
        # Combat Stats
        embed.add_field(
            name="⚔️ Combat Statistics",
            value=f"**Eliminations:** {player['kills']}\n"
                  f"**Deaths:** {player['deaths']}\n"
                  f"**Kill Count:** {player['kill_count']}\n"
                  f"**K/D Ratio:** {kd_ratio:.2f}",
            inline=True
        )
        
        # Performance Metrics
        embed.add_field(
            name="📈 Performance",
            value=f"**Win Rate:** {win_rate:.1f}%\n"
                  f"**Avg Kills/Match:** {(player['kills'] / max(1, total_matches)):.1f}\n"
                  f"**Survival Rate:** {((total_matches - player['deaths']) / max(1, total_matches) * 100):.1f}%\n"
                  f"**Efficiency:** {(player['kills'] / max(1, player['kills'] + player['deaths']) * 100):.1f}%",
            inline=False
        )
        
        # Rank calculation
        all_players = list(self.db.get_all_players().values())
        sorted_by_wins = sorted(all_players, key=lambda x: x['wins'], reverse=True)
        
        try:
            rank = next(i for i, p in enumerate(sorted_by_wins, 1) if p['user_id'] == user.id)
            
            if rank == 1:
                rank_emoji = "👑"
                rank_title = "Champion"
            elif rank <= 3:
                rank_emoji = "🥉" if rank == 3 else "🥈"
                rank_title = f"#{rank} Elite Fighter"
            elif rank <= 10:
                rank_emoji = "🏅"
                rank_title = f"#{rank} Top Fighter"
            else:
                rank_emoji = "⚔️"
                rank_title = f"#{rank} Fighter"
            
            embed.add_field(
                name="🏆 Tournament Ranking",
                value=f"{rank_emoji} **{rank_title}**\n"
                      f"**Position:** {rank} of {len(all_players)}\n"
                      f"**Percentile:** {(100 - (rank/len(all_players))*100):.1f}%",
                inline=True
            )
        except:
            embed.add_field(
                name="🏆 Tournament Ranking",
                value="**Position:** Unranked\n"
                      f"**Total Players:** {len(all_players)}",
                inline=True
            )
        
        # Recent activity
        recent_duels = [d for d in self.db.get_all_duels().values() 
                       if d['player1_id'] == user.id or d['player2_id'] == user.id]
        
        embed.add_field(
            name="📅 Recent Activity",
            value=f"**Total Duels:** {len(recent_duels)}\n"
                  f"**Last Active:** <t:{int(discord.utils.utcnow().timestamp())}:R>\n"
                  f"**Registration:** <t:{int(discord.utils.parse_time(player.get('registered_at', discord.utils.utcnow().isoformat())).timestamp())}:D>",
            inline=True
        )
        
        # Achievement system
        achievements = []
        if player['wins'] >= 10:
            achievements.append("🏆 Veteran (10+ wins)")
        if player['wins'] >= 25:
            achievements.append("💎 Master (25+ wins)")
        if player['kills'] >= 50:
            achievements.append("⚔️ Eliminator (50+ kills)")
        if kd_ratio >= 2.0:
            achievements.append("🔥 Dominator (2.0+ K/D)")
        if win_rate >= 80 and total_matches >= 5:
            achievements.append("⭐ Elite (80%+ win rate)")
        if player['draws'] >= 5:
            achievements.append("🛡️ Survivor (5+ draws)")
        
        if achievements:
            embed.add_field(
                name="🏅 Achievements",
                value="\n".join(achievements[:6]),  # Show max 6 achievements
                inline=False
            )
        
        # Progress to next milestone
        next_milestone_wins = ((player['wins'] // 5) + 1) * 5
        wins_needed = next_milestone_wins - player['wins']
        
        embed.add_field(
            name="🎯 Next Milestone",
            value=f"**Target:** {next_milestone_wins} wins\n"
                  f"**Progress:** {player['wins']}/{next_milestone_wins}\n"
                  f"**Wins Needed:** {wins_needed}",
            inline=True
        )
        
        embed.add_field(
            name="🎮 Server Connection",
            value=f"**IP:** {self.bot.server_ip}\n"
                  f"**Port:** {self.bot.server_port}\n"
                  f"**Status:** 🟢 Online",
            inline=True
        )
        
        # Add player comparison
        if total_matches > 0:
            avg_player = {
                'wins': sum(p['wins'] for p in all_players) / len(all_players),
                'kills': sum(p['kills'] for p in all_players) / len(all_players),
                'win_rate': sum((p['wins'] / max(1, p['wins'] + p['losses'] + p['draws']) * 100) for p in all_players) / len(all_players)
            }
            
            embed.add_field(
                name="📊 vs Tournament Average",
                value=f"**Wins:** {player['wins']} (avg: {avg_player['wins']:.1f})\n"
                      f"**Kills:** {player['kills']} (avg: {avg_player['kills']:.1f})\n"
                      f"**Win Rate:** {win_rate:.1f}% (avg: {avg_player['win_rate']:.1f}%)",
                inline=False
            )
        
        embed.set_footer(
            text=f"🔄 Stats update in real-time • Use /leaderboard to see rankings"
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="compare", description="Compare two players' statistics")
    @app_commands.describe(
        player1="First player to compare",
        player2="Second player to compare"
    )
    async def compare_players(
        self, 
        interaction: discord.Interaction, 
        player1: discord.Member, 
        player2: discord.Member
    ):
        """Compare statistics between two players"""
        await interaction.response.defer()
        
        # Get both players' data
        p1_data = self.db.get_player(player1.id)
        p2_data = self.db.get_player(player2.id)
        
        if not p1_data:
            embed = self.embed_builder.error_embed(
                "Player Not Found",
                f"{player1.mention} is not registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        if not p2_data:
            embed = self.embed_builder.error_embed(
                "Player Not Found",
                f"{player2.mention} is not registered in the tournament!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Calculate stats for both players
        def calc_stats(player_data):
            total = player_data['wins'] + player_data['losses'] + player_data['draws']
            return {
                'total_matches': total,
                'win_rate': (player_data['wins'] / max(1, total)) * 100,
                'kd_ratio': player_data['kills'] / max(1, player_data['deaths'])
            }
        
        p1_stats = calc_stats(p1_data)
        p2_stats = calc_stats(p2_data)
        
        # Create comparison embed
        embed = self.embed_builder.comparison_embed(
            f"⚔️ {player1.display_name} vs {player2.display_name}",
            "Head-to-head statistical comparison"
        )
        
        # Player 1 Stats
        embed.add_field(
            name=f"🥊 {player1.display_name}",
            value=f"🏆 **Wins:** {p1_data['wins']}\n"
                  f"💀 **Losses:** {p1_data['losses']}\n"
                  f"🟡 **Draws:** {p1_data['draws']}\n"
                  f"⚔️ **Kills:** {p1_data['kills']}\n"
                  f"💀 **Deaths:** {p1_data['deaths']}\n"
                  f"📊 **Win Rate:** {p1_stats['win_rate']:.1f}%\n"
                  f"📈 **K/D:** {p1_stats['kd_ratio']:.2f}",
            inline=True
        )
        
        # Comparison column
        def get_winner(val1, val2, higher_better=True):
            if val1 == val2:
                return "🟡"
            if higher_better:
                return "🟢" if val1 > val2 else "🔴"
            else:
                return "🔴" if val1 > val2 else "🟢"
        
        embed.add_field(
            name="📊 Comparison",
            value=f"**Wins:** {get_winner(p1_data['wins'], p2_data['wins'])}\n"
                  f"**Losses:** {get_winner(p1_data['losses'], p2_data['losses'], False)}\n"
                  f"**Draws:** {get_winner(p1_data['draws'], p2_data['draws'])}\n"
                  f"**Kills:** {get_winner(p1_data['kills'], p2_data['kills'])}\n"
                  f"**Deaths:** {get_winner(p1_data['deaths'], p2_data['deaths'], False)}\n"
                  f"**Win Rate:** {get_winner(p1_stats['win_rate'], p2_stats['win_rate'])}\n"
                  f"**K/D Ratio:** {get_winner(p1_stats['kd_ratio'], p2_stats['kd_ratio'])}",
            inline=True
        )
        
        # Player 2 Stats
        embed.add_field(
            name=f"🥊 {player2.display_name}",
            value=f"🏆 **Wins:** {p2_data['wins']}\n"
                  f"💀 **Losses:** {p2_data['losses']}\n"
                  f"🟡 **Draws:** {p2_data['draws']}\n"
                  f"⚔️ **Kills:** {p2_data['kills']}\n"
                  f"💀 **Deaths:** {p2_data['deaths']}\n"
                  f"📊 **Win Rate:** {p2_stats['win_rate']:.1f}%\n"
                  f"📈 **K/D:** {p2_stats['kd_ratio']:.2f}",
            inline=True
        )
        
        # Head-to-head history
        all_duels = self.db.get_all_duels()
        h2h_duels = [d for d in all_duels.values() 
                    if (d['player1_id'] == player1.id and d['player2_id'] == player2.id) or
                       (d['player1_id'] == player2.id and d['player2_id'] == player1.id)]
        
        if h2h_duels:
            embed.add_field(
                name="🔥 Head-to-Head History",
                value=f"**Total Encounters:** {len(h2h_duels)}\n"
                      f"**Series Status:** Under Development\n"
                      f"**Rivalry Level:** {'🔥 INTENSE' if len(h2h_duels) >= 3 else '⚡ DEVELOPING'}",
                inline=False
            )
        
        # Overall comparison summary
        p1_advantages = sum([
            p1_data['wins'] > p2_data['wins'],
            p1_data['kills'] > p2_data['kills'],
            p1_stats['win_rate'] > p2_stats['win_rate'],
            p1_stats['kd_ratio'] > p2_stats['kd_ratio'],
            p1_data['losses'] < p2_data['losses'],
            p1_data['deaths'] < p2_data['deaths']
        ])
        
        if p1_advantages > 3:
            advantage_text = f"🏆 **{player1.display_name}** has the statistical advantage"
        elif p1_advantages < 3:
            advantage_text = f"🏆 **{player2.display_name}** has the statistical advantage"
        else:
            advantage_text = "🤝 **Evenly Matched** - This will be an epic battle!"
        
        embed.add_field(
            name="🎯 Prediction",
            value=f"{advantage_text}\n\n"
                  f"**Suggested Matchup:** {'🔥 MUST WATCH' if abs(p1_advantages - 3) <= 1 else '⚡ EXCITING'}\n"
                  f"**Battle Intensity:** {min(10, max(1, abs(p1_data['wins'] - p2_data['wins']) + 5))}/10",
            inline=False
        )
        
        embed.set_footer(text="🎮 Schedule a duel with /duel to see who's truly better!")
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="kill", description="View kill leaderboard")
    async def kill_leaderboard(self, interaction: discord.Interaction):
        """Display kill leaderboard"""
        await interaction.response.defer()
        
        players = self.db.get_all_players()
        
        if not players:
            embed = self.embed_builder.warning_embed(
                "No Data Available",
                "No players are registered yet!"
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Sort by kills
        sorted_players = sorted(players.values(), key=lambda x: x['kills'], reverse=True)
        
        embed = self.embed_builder.leaderboard_embed(
            "💀 Kill Leaderboard",
            "Most deadly fighters in the tournament"
        )
        
        leaderboard_text = ""
        medals = ["🥇", "🥈", "🥉"] + ["💀"] * 7
        
        for i, player in enumerate(sorted_players[:10]):
            try:
                user = self.bot.get_user(player['user_id'])
                name = user.display_name if user else player['display_name']
                medal = medals[i] if i < len(medals) else "💀"
                kd_ratio = player['kills'] / max(1, player['deaths'])
                
                leaderboard_text += f"{medal} **{name}**\n"
                leaderboard_text += f"   ⚔️ {player['kills']} kills | K/D: {kd_ratio:.2f}\n"
                leaderboard_text += f"   💀 {player['deaths']} deaths | Matches: {player['wins'] + player['losses'] + player['draws']}\n\n"
            except:
                continue
        
        embed.add_field(
            name="🏆 Top Eliminators",
            value=leaderboard_text or "No data available",
            inline=False
        )
        
        # Tournament kill stats
        total_kills = sum(p['kills'] for p in players.values())
        total_deaths = sum(p['deaths'] for p in players.values())
        
        embed.add_field(
            name="📊 Tournament Kill Statistics",
            value=f"**Total Eliminations:** {total_kills}\n"
                  f"**Total Deaths:** {total_deaths}\n"
                  f"**Average Kills per Player:** {(total_kills / len(players)):.1f}\n"
                  f"**Most Deadly:** {sorted_players[0]['display_name'] if sorted_players else 'N/A'}",
            inline=False
        )
        
        embed.set_footer(text="💀 Become the ultimate eliminator!")
        
        await interaction.followup.send(embed=embed)
