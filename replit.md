# Duel Lords - BombSquad Tournament Bot

## Overview

Duel Lords is a comprehensive Discord bot designed for managing BombSquad tournaments. The system features luxury-themed embeds, automated duel scheduling with intelligent reminders, player statistics tracking, and a premium web dashboard. The bot provides complete tournament management capabilities including player registration, leaderboards, multi-language support, and real-time tournament analytics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Architecture
- **Discord.py Framework**: Uses discord.py 2.0+ with slash commands for modern Discord interaction
- **Cog-based Command Structure**: Commands organized into logical modules (admin, tournament, duel, stats)
- **Event-driven Design**: Async/await pattern for handling Discord events and scheduled tasks
- **Component-based Architecture**: Modular utilities for embeds, database, scheduling, and translations

### Data Management
- **JSON File Storage**: Lightweight file-based storage using players.json and duels.json
- **Database Abstraction Layer**: Centralized Database class handling all data operations
- **In-memory Caching**: Bot maintains active state for scheduled duels and reminders

### Scheduling System
- **Automated Reminder System**: Background task checking for upcoming duels every interval
- **Smart Conflict Detection**: Prevents scheduling conflicts and validates duel times
- **Private Message Integration**: Direct message notifications to participants with motivational content

### Web Dashboard
- **Flask Web Framework**: Separate web application providing tournament visualization
- **RESTful API Endpoints**: JSON APIs for statistics, leaderboard data, and health checks
- **Responsive Frontend**: Bootstrap-based UI with luxury theming and mobile support
- **Real-time Data Integration**: Web dashboard pulls live data from the same JSON storage

### Multi-language Support
- **Translation System**: Centralized Translator class supporting English and Portuguese
- **Localized Embeds**: All bot responses support multiple languages through translation keys

### Keep-alive System
- **Health Monitoring**: Flask server providing uptime endpoints for hosting platforms
- **Threading Architecture**: Keep-alive server runs in separate thread from main bot process

## External Dependencies

### Discord Integration
- **Discord Bot API**: Primary interface through discord.py library
- **Slash Commands**: Modern Discord command system with parameter validation
- **Embed System**: Rich message formatting with luxury visual design
- **Member Management**: Discord user and guild permission integration

### Web Technologies
- **Flask Framework**: Lightweight web server for dashboard and API endpoints
- **Bootstrap 5**: Frontend CSS framework for responsive design
- **Font Awesome**: Icon library for enhanced visual elements
- **JSON Storage**: File-based persistence without external database dependencies

### Hosting Platform Support
- **Environment Variables**: Configuration through DISCORD_TOKEN and FLASK_SECRET_KEY
- **Port Configuration**: Dynamic port assignment for hosting platform compatibility
- **Health Check Endpoints**: Multiple endpoints for monitoring and uptime services

### BombSquad Game Integration
- **Server Connection Info**: Hardcoded game server details (IP: 18.228.228.44, Port: 3827)
- **Tournament Mode**: Bot designed specifically for BombSquad tournament management
- **Player Statistics**: Tracks game-specific metrics (kills, deaths, K/D ratios)