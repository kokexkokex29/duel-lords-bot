from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
from bot.utils.database import Database

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'duel-lords-secret-key')

# Initialize database
db = Database()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    """Tournament leaderboard page"""
    # Get tournament statistics
    stats = db.get_tournament_stats()
    
    # Get top players
    top_players = db.get_leaderboard(sort_by='wins', limit=20)
    
    # Get recent duels
    all_duels = db.get_all_duels()
    recent_duels = sorted(
        [d for d in all_duels.values() if d.get('status') == 'completed'], 
        key=lambda x: x.get('created_at', ''), 
        reverse=True
    )[:10]
    
    return render_template('leaderboard.html', 
                         tournament_stats=stats,
                         leaderboard=top_players,
                         recent_duels=recent_duels)

@app.route('/api/stats')
def api_stats():
    """API endpoint for tournament statistics"""
    stats = db.get_tournament_stats()
    return jsonify(stats)

@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data"""
    sort_by = request.args.get('sort', 'wins')
    limit = int(request.args.get('limit', 10))
    
    leaderboard = db.get_leaderboard(sort_by=sort_by, limit=limit)
    return jsonify(leaderboard)

@app.route('/api/players')
def api_players():
    """API endpoint for all players"""
    players = db.get_all_players()
    
    # Convert to list format with calculated stats
    player_list = []
    for user_id, player in players.items():
        total_matches = player.get('wins', 0) + player.get('losses', 0) + player.get('draws', 0)
        win_rate = (player.get('wins', 0) / max(1, total_matches)) * 100
        kd_ratio = player.get('kills', 0) / max(1, player.get('deaths', 1))
        
        player_data = {
            'user_id': int(user_id),
            'display_name': player.get('display_name', 'Unknown'),
            'wins': player.get('wins', 0),
            'losses': player.get('losses', 0),
            'draws': player.get('draws', 0),
            'kills': player.get('kills', 0),
            'deaths': player.get('deaths', 0),
            'total_matches': total_matches,
            'win_rate': round(win_rate, 1),
            'kd_ratio': round(kd_ratio, 2),
            'registered_at': player.get('registered_at', '')
        }
        player_list.append(player_data)
    
    return jsonify(player_list)

@app.route('/api/duels')
def api_duels():
    """API endpoint for duels data"""
    duels = db.get_all_duels()
    
    # Convert to list format
    duel_list = []
    for duel_id, duel in duels.items():
        duel_data = {
            'id': duel_id,
            'player1_name': duel.get('player1_name', 'Unknown'),
            'player2_name': duel.get('player2_name', 'Unknown'),
            'scheduled_time': duel.get('scheduled_time', ''),
            'status': duel.get('status', 'unknown'),
            'created_at': duel.get('created_at', '')
        }
        duel_list.append(duel_data)
    
    return jsonify(duel_list)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Duel Lords Tournament Bot is running!',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong. Please try again later.'
    }), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
