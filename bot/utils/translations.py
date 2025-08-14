class Translator:
    def __init__(self):
        self.translations = {
            'en': {
                # Common terms
                'wins': 'Wins',
                'losses': 'Losses', 
                'draws': 'Draws',
                'kills': 'Kills',
                'deaths': 'Deaths',
                'player': 'Player',
                'tournament': 'Tournament',
                'duel': 'Duel',
                'leaderboard': 'Leaderboard',
                'statistics': 'Statistics',
                'rank': 'Rank',
                'match': 'Match',
                'fighter': 'Fighter',
                
                # Commands
                'register_success': 'Player registered successfully!',
                'register_exists': 'Player is already registered!',
                'player_not_found': 'Player not found in tournament!',
                'duel_scheduled': 'Duel scheduled successfully!',
                'invalid_date': 'Invalid date/time provided!',
                'admin_only': 'Only administrators can use this command!',
                
                # Duel messages
                'duel_reminder': 'Your duel starts in 5 minutes!',
                'duel_notification': 'You have been challenged to a duel!',
                'prepare_battle': 'Prepare for battle!',
                'good_luck': 'Good luck in your duel!',
                
                # Server info
                'server_info': 'BombSquad Server Information',
                'connection_details': 'Connection Details',
                'how_to_connect': 'How to Connect',
                'server_status': 'Server Status',
                
                # Tournament info
                'total_players': 'Total Players',
                'registered_fighters': 'Registered Fighters',
                'completed_duels': 'Completed Duels',
                'scheduled_duels': 'Scheduled Duels',
                'win_rate': 'Win Rate',
                'kd_ratio': 'K/D Ratio',
                
                # Achievements
                'veteran_achievement': 'Veteran (10+ wins)',
                'master_achievement': 'Master (25+ wins)',
                'eliminator_achievement': 'Eliminator (50+ kills)',
                'dominator_achievement': 'Dominator (2.0+ K/D)',
                'elite_achievement': 'Elite (80%+ win rate)',
                'survivor_achievement': 'Survivor (5+ draws)',
            },
            
            'pt': {  # Portuguese
                # Common terms
                'wins': 'Vitórias',
                'losses': 'Derrotas',
                'draws': 'Empates', 
                'kills': 'Eliminações',
                'deaths': 'Mortes',
                'player': 'Jogador',
                'tournament': 'Torneio',
                'duel': 'Duelo',
                'leaderboard': 'Classificação',
                'statistics': 'Estatísticas',
                'rank': 'Classificação',
                'match': 'Partida',
                'fighter': 'Lutador',
                
                # Commands
                'register_success': 'Jogador registrado com sucesso!',
                'register_exists': 'Jogador já está registrado!',
                'player_not_found': 'Jogador não encontrado no torneio!',
                'duel_scheduled': 'Duelo agendado com sucesso!',
                'invalid_date': 'Data/hora inválida fornecida!',
                'admin_only': 'Apenas administradores podem usar este comando!',
                
                # Duel messages
                'duel_reminder': 'Seu duelo começa em 5 minutos!',
                'duel_notification': 'Você foi desafiado para um duelo!',
                'prepare_battle': 'Prepare-se para a batalha!',
                'good_luck': 'Boa sorte no seu duelo!',
                
                # Server info
                'server_info': 'Informações do Servidor BombSquad',
                'connection_details': 'Detalhes da Conexão',
                'how_to_connect': 'Como Conectar',
                'server_status': 'Status do Servidor',
                
                # Tournament info
                'total_players': 'Total de Jogadores',
                'registered_fighters': 'Lutadores Registrados',
                'completed_duels': 'Duelos Completados',
                'scheduled_duels': 'Duelos Agendados',
                'win_rate': 'Taxa de Vitória',
                'kd_ratio': 'Taxa E/M',
                
                # Achievements
                'veteran_achievement': 'Veterano (10+ vitórias)',
                'master_achievement': 'Mestre (25+ vitórias)',
                'eliminator_achievement': 'Eliminador (50+ eliminações)',
                'dominator_achievement': 'Dominador (2.0+ E/M)',
                'elite_achievement': 'Elite (80%+ taxa de vitória)',
                'survivor_achievement': 'Sobrevivente (5+ empates)',
            }
        }
        
        self.default_language = 'en'
    
    def get_text(self, key: str, language: str = None) -> str:
        """Get translated text for a given key"""
        if language is None:
            language = self.default_language
        
        if language not in self.translations:
            language = self.default_language
        
        return self.translations[language].get(key, key)
    
    def set_default_language(self, language: str):
        """Set the default language for translations"""
        if language in self.translations:
            self.default_language = language
    
    def get_available_languages(self) -> list:
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def get_language_name(self, code: str) -> str:
        """Get display name for language code"""
        names = {
            'en': 'English',
            'pt': 'Português'
        }
        return names.get(code, code)
