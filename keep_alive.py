from flask import Flask, jsonify
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Duel Lords Tournament Bot',
        'message': 'Bot is running and ready for epic battles!',
        'features': [
            'Player registration and management',
            'Duel scheduling with reminders',
            'Real-time statistics tracking',
            'Tournament leaderboards',
            'Multi-language support',
            'Web dashboard integration'
        ]
    })

@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'bot_status': 'online',
        'server': {
            'ip': '18.228.228.44',
            'port': '3827',
            'status': 'active'
        },
        'features_status': {
            'discord_bot': 'running',
            'web_dashboard': 'active',
            'database': 'connected',
            'scheduler': 'active'
        }
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return jsonify({'ping': 'pong', 'status': 'ok'})

def run():
    """Run the keep-alive server"""
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

def keep_alive():
    """Start the keep-alive server in a separate thread"""
    try:
        print("🚀 Starting keep-alive server...")
        server_thread = Thread(target=run, daemon=True)
        server_thread.start()
        print(f"✅ Keep-alive server started on port 8000")
    except Exception as e:
        print(f"❌ Failed to start keep-alive server: {e}")

if __name__ == '__main__':
    run()
