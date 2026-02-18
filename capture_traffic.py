import pyshark
from queue import Queue
import threading
import time

packet_queue = Queue()

def capture_traffic_once(interface="wlan0", duration=5):
    """
    Capture HTTP/HTTPS traffic for a specific duration (seconds)
    and push packets to packet_queue.
    """
    try:
        capture = pyshark.LiveCapture(interface=interface, bpf_filter="tcp port 80 or tcp port 443")
        print(f"[INFO] Capturing network traffic for {duration}s on {interface}...")
        start_time = time.time()

        for packet in capture.sniff_continuously():
            elapsed = time.time() - start_time
            if elapsed >= duration:
                print(f"[INFO] Stopping capture after {elapsed:.1f}s")
                break
            try:
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst
                protocol = "HTTP" if packet.tcp.dstport == "80" else "HTTPS"
                timestamp = str(packet.sniff_time)
                packet_queue.put({
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "protocol": protocol,
                    "timestamp": timestamp
                })
            except AttributeError:
                continue
    except Exception as e:
        print(f"[ERROR] Capture failed: {e}")
    finally:
        capture.close()


def start_capture(interface="wlan0"):
    """
    Continuously capture packets in a background thread.
    Internally calls capture_traffic_once() repeatedly.
    """
    def capture_thread():
        print("[INFO] Starting continuous live capture...")
        while True:
            capture_traffic_once(interface=interface, duration=5)
            time.sleep(0.5)  # slight delay between captures

    t = threading.Thread(target=capture_thread, daemon=True)
    t.start()
