# 🏆 Duel Lords - BombSquad Tournament Bot

![Duel Lords](https://img.shields.io/badge/Duel%20Lords-Tournament%20Bot-gold?style=for-the-badge&logo=discord)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-purple?style=for-the-badge&logo=discord)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-green?style=for-the-badge&logo=flask)

The ultimate Discord bot for BombSquad tournaments featuring luxury embeds, comprehensive player management, intelligent duel scheduling, automatic reminders, and a premium web dashboard.

## ✨ Premium Features

### 🔥 **Core Tournament Management**
- **Admin-Only Registration**: Secure player registration system with administrator controls
- **Complete Statistics Tracking**: Wins, losses, draws, kills, deaths, K/D ratios, and performance analytics
- **Intelligent Duel Scheduling**: Advanced scheduling with Discord timestamps and conflict detection
- **Smart Reminder System**: 5-minute automatic reminders with personalized motivational messages
- **Real-Time Leaderboards**: Dynamic rankings with multiple sorting options and achievement system

### ⚡ **Advanced Bot Features**
- **Luxury Embed Design**: Premium visual experience with exceptional aesthetic appeal
- **Private Message System**: Non-repetitive DM notifications for duel participants
- **Multi-Language Support**: Full English and Portuguese language support
- **24/7 Operation**: Keep-alive system for continuous uptime on hosting platforms
- **Comprehensive Commands**: 15+ slash commands for complete tournament management

### 🌐 **Web Dashboard Integration**
- **Live Tournament Dashboard**: Real-time statistics and player information
- **Interactive Leaderboard**: Beautiful web interface with sorting and filtering
- **Mobile-Responsive Design**: Perfect experience on all devices
- **API Endpoints**: RESTful API for data integration and external tools

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9 or higher
- Discord Bot Token
- Basic knowledge of Discord bot setup

### 1. Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy the bot token (you'll need this later)
4. Invite bot to your server with these permissions:
   - Send Messages
   - Use Slash Commands  
   - Send Messages in Threads
   - Embed Links
   - Read Message History
   - Add Reactions

### 2. Local Development Setup

```bash
# Clone or download the bot files
# Navigate to the bot directory
cd duel-lords-bot

# Install required packages
pip install discord.py flask python-dateutil pytz

# Set your Discord bot token as environment variable
export DISCORD_TOKEN="your_bot_token_here"

# Run the bot
python main.py
