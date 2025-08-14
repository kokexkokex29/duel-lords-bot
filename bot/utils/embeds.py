import discord
from datetime import datetime
from typing import Optional

class EmbedBuilder:
    def __init__(self):
        # Luxury color scheme
        self.colors = {
            'primary': 0x7C4DFF,      # Deep Purple
            'success': 0x4CAF50,      # Green
            'warning': 0xFF9800,      # Orange
            'error': 0xF44336,        # Red
            'info': 0x2196F3,         # Blue
            'tournament': 0xE91E63,   # Pink
            'duel': 0xFF5722,         # Deep Orange
            'stats': 0x9C27B0,        # Purple
            'leaderboard': 0xFFD700,  # Gold
            'comparison': 0x00BCD4    # Cyan
        }
        
        # Luxury styling
        self.footer_icon = "https://cdn.discordapp.com/emojis/856550982005465108.png"
        self.thumbnail_url = "https://cdn.discordapp.com/emojis/856550982005465108.png"
    
    def base_embed(self, title: str, description: str, color: int) -> discord.Embed:
        """Create a base embed with luxury styling"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        
        # Add luxury branding
        embed.set_author(
            name="Duel Lords Tournament",
            icon_url=self.footer_icon
        )
        
        return embed
    
    def success_embed(self, title: str, description: str) -> discord.Embed:
        """Create a success embed"""
        embed = self.base_embed(title, description, self.colors['success'])
        embed.set_footer(text="✅ Success | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def error_embed(self, title: str, description: str) -> discord.Embed:
        """Create an error embed"""
        embed = self.base_embed(title, description, self.colors['error'])
        embed.set_footer(text="❌ Error | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def warning_embed(self, title: str, description: str) -> discord.Embed:
        """Create a warning embed"""
        embed = self.base_embed(title, description, self.colors['warning'])
        embed.set_footer(text="⚠️ Warning | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def info_embed(self, title: str, description: str) -> discord.Embed:
        """Create an info embed"""
        embed = self.base_embed(title, description, self.colors['info'])
        embed.set_footer(text="ℹ️ Information | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def tournament_embed(self, title: str, description: str) -> discord.Embed:
        """Create a tournament-themed embed"""
        embed = self.base_embed(title, description, self.colors['tournament'])
        embed.set_footer(text="🏆 Tournament | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def duel_embed(self, title: str, description: str) -> discord.Embed:
        """Create a luxury duel announcement embed"""
        embed = self.base_embed(title, description, self.colors['duel'])
        
        # Add luxury visual elements
        embed.set_footer(text="⚔️ Epic Duel | Duel Lords", icon_url=self.footer_icon)
        
        # Add visual separators
        embed.description += "\n\n" + "━" * 30 + "\n"
        
        return embed
    
    def duel_notification_embed(self, title: str, description: str) -> discord.Embed:
        """Create a luxury duel notification embed for DMs"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.colors['duel'],
            timestamp=datetime.utcnow()
        )
        
        # Luxury DM styling
        embed.set_author(
            name="🏆 Duel Lords Tournament",
            icon_url=self.footer_icon
        )
        
        embed.set_footer(
            text="⚔️ Prepare for battle! | Duel Lords",
            icon_url=self.footer_icon
        )
        
        # Add motivational element
        embed.add_field(
            name="💪 Battle Motivation",
            value="*\"Victory belongs to the most persevering.\"*\n"
                  "*- Napoleon Bonaparte*",
            inline=False
        )
        
        return embed
    
    def duel_reminder_embed(self, title: str, description: str) -> discord.Embed:
        """Create a luxury duel reminder embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xFF4500,  # Orange Red for urgency
            timestamp=datetime.utcnow()
        )
        
        # Urgent styling
        embed.set_author(
            name="🔔 Duel Reminder | Duel Lords",
            icon_url=self.footer_icon
        )
        
        embed.set_footer(
            text="⏰ 5 Minutes Warning! | Duel Lords",
            icon_url=self.footer_icon
        )
        
        return embed
    
    def duel_list_embed(self, title: str, description: str) -> discord.Embed:
        """Create a duel list embed"""
        embed = self.base_embed(title, description, self.colors['duel'])
        embed.set_footer(text="📅 Scheduled Duels | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def stats_embed(self, title: str, description: str) -> discord.Embed:
        """Create a luxury statistics embed"""
        embed = self.base_embed(title, description, self.colors['stats'])
        embed.set_footer(text="📊 Player Statistics | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def leaderboard_embed(self, title: str, description: str) -> discord.Embed:
        """Create a luxury leaderboard embed"""
        embed = self.base_embed(title, description, self.colors['leaderboard'])
        embed.set_footer(text="🏆 Tournament Leaderboard | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def comparison_embed(self, title: str, description: str) -> discord.Embed:
        """Create a player comparison embed"""
        embed = self.base_embed(title, description, self.colors['comparison'])
        embed.set_footer(text="⚔️ Player Comparison | Duel Lords", icon_url=self.footer_icon)
        return embed
    
    def help_embed(self) -> discord.Embed:
        """Create a comprehensive help embed"""
        embed = self.base_embed(
            "📚 Duel Lords Command Guide",
            "Complete list of available commands for the ultimate BombSquad tournament experience!"
        )
        
        # Admin Commands
        embed.add_field(
            name="👑 Admin Commands",
            value="`/register` - Register a new player\n"
                  "`/remove` - Remove a player\n"
                  "`/update` - Update player stats\n"
                  "`/duel` - Schedule a duel\n"
                  "`/cancel_duel` - Cancel a scheduled duel",
            inline=False
        )
        
        # Player Commands
        embed.add_field(
            name="🥊 Player Commands",
            value="`/stats` - View player statistics\n"
                  "`/compare` - Compare two players\n"
                  "`/fighters` - View all fighters\n"
                  "`/leaderboard` - Tournament rankings\n"
                  "`/kill` - Kill leaderboard",
            inline=False
        )
        
        # General Commands
        embed.add_field(
            name="🎮 General Commands",
            value="`/ip` - Server connection info\n"
                  "`/duels` - View upcoming duels\n"
                  "`/tournament_info` - Tournament details\n"
                  "`/help` - Show this help message",
            inline=False
        )
        
        # Features
        embed.add_field(
            name="✨ Premium Features",
            value="• Automatic duel reminders (5 min before)\n"
                  "• Private message notifications\n"
                  "• Real-time statistics tracking\n"
                  "• Luxury embed designs\n"
                  "• Multi-language support\n"
                  "• Web dashboard integration",
            inline=False
        )
        
        embed.set_footer(text="🏆 Become a Duel Lord! | Use commands to get started")
        
        return embed
    
    def web_dashboard_embed(self, leaderboard_url: str) -> discord.Embed:
        """Create web dashboard promotional embed"""
        embed = self.base_embed(
            "🌐 Web Dashboard Available!",
            "Access the complete tournament experience through our web interface!"
        )
        
        embed.add_field(
            name="🔗 Dashboard Features",
            value="• Live tournament leaderboard\n"
                  "• Detailed player statistics\n"
                  "• Match history tracking\n"
                  "• Real-time updates\n"
                  "• Mobile-friendly interface",
            inline=False
        )
        
        embed.add_field(
            name="🌟 Quick Access",
            value=f"[**🚀 Open Dashboard**]({leaderboard_url})\n"
                  f"[**📊 View Leaderboard**]({leaderboard_url})\n"
                  f"[**📈 Live Stats**]({leaderboard_url})",
            inline=False
        )
        
        embed.set_footer(text="🌐 Always stay connected to the tournament!")
        
        return embed
