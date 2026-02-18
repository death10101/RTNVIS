import threading
import time
import sqlite3
import requests
from capture_traffic import packet_queue, capture_traffic_once
from datetime import datetime
import ipaddress

# Nairobi Coordinates (Hardcoded Source)
NAIROBI_LAT = -1.286389
NAIROBI_LON = 36.817223

# SQLite connection
conn = sqlite3.connect("traffic.db", check_same_thread=False, timeout=10)
cursor = conn.cursor()
db_lock = threading.Lock()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src_ip TEXT, dst_ip TEXT, 
    src_lat REAL, src_lon REAL,
    dst_lat REAL, dst_lon REAL,
    protocol TEXT, timestamp TEXT
)
""")
conn.commit()

# Cache for IP geolocation
geo_cache = {}

def is_public_ip(ip):
    """Return True if IP is public."""
    try:
        return not ipaddress.ip_address(ip).is_private
    except:
        return False

def get_geolocation(ip):
    if ip in geo_cache:
        return geo_cache[ip]

    token = "your_ipinfo_token_here"  # Replace with your actual token

    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json?token={token}", timeout=5)
        loc = res.json().get("loc", "0,0").split(",")
        lat, lon = float(loc[0]), float(loc[1])
    except:
        lat, lon = 0.0, 0.0

    geo_cache[ip] = (lat, lon)
    return lat, lon

def process_and_store():
    """Continuously process packets from the queue and store in SQLite."""
    while True:
        time.sleep(1)

        batch = []
        while not packet_queue.empty():
            pkt = packet_queue.get()
            pkt["timestamp"] = datetime.now().isoformat()
            batch.append(pkt)

        if batch:
            with db_lock:
                stored_count = 0

                for pkt in batch:

                    # Only process public destination IPs
                    if not is_public_ip(pkt["dst_ip"]):
                        continue

                    # Hardcoded Nairobi source
                    src_lat = NAIROBI_LAT
                    src_lon = NAIROBI_LON

                    # Real geolocation for destination
                    dst_lat, dst_lon = get_geolocation(pkt["dst_ip"])

                    # Skip invalid geolocation
                    if dst_lat == 0.0 and dst_lon == 0.0:
                        continue

                    cursor.execute("""
                        INSERT INTO traffic 
                        (src_ip, dst_ip, src_lat, src_lon, dst_lat, dst_lon, protocol, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        pkt["src_ip"],
                        pkt["dst_ip"],
                        src_lat,
                        src_lon,
                        dst_lat,
                        dst_lon,
                        pkt["protocol"],
                        pkt["timestamp"]
                    ))

                    stored_count += 1

                conn.commit()

            if stored_count > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Stored {stored_count} live packets.")

def start_live_capture(interface="wlan0"):
    """Continuously capture packets every 5 seconds in the background."""
    threading.Thread(target=process_and_store, daemon=True).start()

    print("[INFO] Live capture started...")

    while True:
        capture_traffic_once(interface=interface, duration=5)
        time.sleep(0.5)
