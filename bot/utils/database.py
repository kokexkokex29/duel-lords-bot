import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class Database:
    def __init__(self):
        self.players_file = "data/players.json"
        self.duels_file = "data/duels.json"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Initialize files if they don't exist
        self._init_file(self.players_file, {})
        self._init_file(self.duels_file, {})
    
    def _init_file(self, filename: str, default_data: dict):
        """Initialize a JSON file with default data if it doesn't exist"""
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def _load_data(self, filename: str) -> dict:
        """Load data from a JSON file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, filename: str, data: dict):
        """Save data to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
    
    # Player management
    def add_player(self, user_id: int, player_data: dict):
        """Add a new player to the database"""
        players = self._load_data(self.players_file)
        players[str(user_id)] = player_data
        self._save_data(self.players_file, players)
    
    def get_player(self, user_id: int) -> Optional[dict]:
        """Get a player's data"""
        players = self._load_data(self.players_file)
        return players.get(str(user_id))
    
    def update_player(self, user_id: int, player_data: dict):
        """Update a player's data"""
        players = self._load_data(self.players_file)
        if str(user_id) in players:
            players[str(user_id)] = player_data
            self._save_data(self.players_file, players)
    
    def remove_player(self, user_id: int):
        """Remove a player from the database"""
        players = self._load_data(self.players_file)
        if str(user_id) in players:
            del players[str(user_id)]
            self._save_data(self.players_file, players)
    
    def get_all_players(self) -> dict:
        """Get all players data"""
        return self._load_data(self.players_file)
    
    def update_player_stats(self, user_id: int, wins: int = 0, losses: int = 0, 
                           draws: int = 0, kills: int = 0, deaths: int = 0):
        """Update player statistics"""
        player = self.get_player(user_id)
        if player:
            player['wins'] += wins
            player['losses'] += losses
            player['draws'] += draws
            player['kills'] += kills
            player['deaths'] += deaths
            player['kill_count'] = player['kills']  # Update kill count
            player['last_updated'] = datetime.utcnow().isoformat()
            self.update_player(user_id, player)
    
    # Duel management
    def add_duel(self, duel_id: str, duel_data: dict):
        """Add a new duel to the database"""
        duels = self._load_data(self.duels_file)
        duels[duel_id] = duel_data
        self._save_data(self.duels_file, duels)
    
    def get_duel(self, duel_id: str) -> Optional[dict]:
        """Get a duel's data"""
        duels = self._load_data(self.duels_file)
        return duels.get(duel_id)
    
    def update_duel(self, duel_id: str, duel_data: dict):
        """Update a duel's data"""
        duels = self._load_data(self.duels_file)
        if duel_id in duels:
            duels[duel_id] = duel_data
            self._save_data(self.duels_file, duels)
    
    def remove_duel(self, duel_id: str):
        """Remove a duel from the database"""
        duels = self._load_data(self.duels_file)
        if duel_id in duels:
            del duels[duel_id]
            self._save_data(self.duels_file, duels)
    
    def get_all_duels(self) -> dict:
        """Get all duels data"""
        return self._load_data(self.duels_file)
    
    def get_upcoming_duels(self) -> list:
        """Get all upcoming scheduled duels"""
        duels = self._load_data(self.duels_file)
        upcoming = []
        current_timestamp = datetime.utcnow().timestamp()
        
        for duel in duels.values():
            if (duel.get('status') == 'scheduled' and 
                duel.get('timestamp', 0) > current_timestamp):
                upcoming.append(duel)
        
        return sorted(upcoming, key=lambda x: x.get('timestamp', 0))
    
    def get_player_duels(self, user_id: int) -> list:
        """Get all duels for a specific player"""
        duels = self._load_data(self.duels_file)
        player_duels = []
        
        for duel in duels.values():
            if (duel.get('player1_id') == user_id or 
                duel.get('player2_id') == user_id):
                player_duels.append(duel)
        
        return sorted(player_duels, key=lambda x: x.get('timestamp', 0), reverse=True)
    
    # Tournament statistics
    def get_tournament_stats(self) -> dict:
        """Get overall tournament statistics"""
        players = self._load_data(self.players_file)
        duels = self._load_data(self.duels_file)
        
        if not players:
            return {
                'total_players': 0,
                'total_duels': 0,
                'completed_duels': 0,
                'total_matches': 0,
                'total_kills': 0,
                'total_deaths': 0
            }
        
        total_wins = sum(p.get('wins', 0) for p in players.values())
        total_losses = sum(p.get('losses', 0) for p in players.values())
        total_draws = sum(p.get('draws', 0) for p in players.values())
        total_kills = sum(p.get('kills', 0) for p in players.values())
        total_deaths = sum(p.get('deaths', 0) for p in players.values())
        
        completed_duels = len([d for d in duels.values() if d.get('status') == 'completed'])
        
        return {
            'total_players': len(players),
            'total_duels': len(duels),
            'completed_duels': completed_duels,
            'scheduled_duels': len(duels) - completed_duels,
            'total_matches': total_wins + total_losses + total_draws,
            'total_wins': total_wins,
            'total_losses': total_losses,
            'total_draws': total_draws,
            'total_kills': total_kills,
            'total_deaths': total_deaths,
            'average_kills_per_player': total_kills / len(players) if players else 0,
            'average_matches_per_player': (total_wins + total_losses + total_draws) / len(players) if players else 0
        }
    
    def get_leaderboard(self, sort_by: str = 'wins', limit: int = 10) -> list:
        """Get tournament leaderboard"""
        players = self._load_data(self.players_file)
        
        if not players:
            return []
        
        # Convert to list and add calculated stats
        player_list = []
        for user_id, player in players.items():
            total_matches = player.get('wins', 0) + player.get('losses', 0) + player.get('draws', 0)
            win_rate = (player.get('wins', 0) / max(1, total_matches)) * 100
            kd_ratio = player.get('kills', 0) / max(1, player.get('deaths', 1))
            
            player_data = {
                **player,
                'user_id': int(user_id),
                'total_matches': total_matches,
                'win_rate': win_rate,
                'kd_ratio': kd_ratio
            }
            player_list.append(player_data)
        
        # Sort by specified criteria
        if sort_by == 'win_rate':
            player_list.sort(key=lambda x: x['win_rate'], reverse=True)
        elif sort_by == 'kd_ratio':
            player_list.sort(key=lambda x: x['kd_ratio'], reverse=True)
        elif sort_by == 'kills':
            player_list.sort(key=lambda x: x.get('kills', 0), reverse=True)
        elif sort_by == 'matches':
            player_list.sort(key=lambda x: x['total_matches'], reverse=True)
        else:  # Default to wins
            player_list.sort(key=lambda x: x.get('wins', 0), reverse=True)
        
        return player_list[:limit]
    
    def backup_data(self):
        """Create a backup of all tournament data"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"data/backups/{timestamp}"
        
        os.makedirs(backup_dir, exist_ok=True)
        
        try:
            # Backup players
            players = self._load_data(self.players_file)
            with open(f"{backup_dir}/players.json", 'w') as f:
                json.dump(players, f, indent=2)
            
            # Backup duels
            duels = self._load_data(self.duels_file)
            with open(f"{backup_dir}/duels.json", 'w') as f:
                json.dump(duels, f, indent=2)
            
            print(f"✅ Data backed up to {backup_dir}")
            return backup_dir
        
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
