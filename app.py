from flask import Flask, jsonify, request, render_template
import threading
from traffic_processor import start_live_capture, db_lock, conn

app = Flask(__name__)
API_KEY = "secret_key_123"

# Serve the homepage
@app.route("/")
def home():
    return render_template("index.html")  # Flask looks in templates/ folder

# API endpoint for traffic
@app.route("/api/traffic")
def api_traffic():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    with db_lock:
        cursor = conn.cursor()
        # Fetch the 100 most recent packets for live visualization
        cursor.execute("""
            SELECT src_ip, dst_ip, src_lat, src_lon, dst_lat, dst_lon, protocol, timestamp 
            FROM traffic 
            ORDER BY id DESC LIMIT 100
        """)
        rows = cursor.fetchall()
        data = [{
            "src_ip": r[0], "dst_ip": r[1],
            "src_lat": r[2], "src_lon": r[3],
            "dst_lat": r[4], "dst_lon": r[5],
            "protocol": r[6], "timestamp": r[7]
        } for r in rows]

    return jsonify(data)

if __name__ == "__main__":
    # Start live traffic capture in the background
    threading.Thread(target=start_live_capture, daemon=True).start()
    print("[INFO] Live traffic capture started. Flask server running...")
    app.run(host="0.0.0.0", port=5000, debug=True)
