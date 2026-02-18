🌍 RTNVIS — Real-Time Network Traffic Visualization

A real-time cybersecurity visualization dashboard that captures live HTTP/HTTPS traffic and displays global packet flows on an interactive 3D globe.

This project demonstrates practical skills in:

- Network traffic capture
- Threaded backend processing
- IP geolocation
- Data persistence
- API design
- Real-time frontend visualization
- 3D rendering with Three.js

---

## 📸 Overview

RTNVIS captures live outbound traffic from your machine, processes packet metadata, geolocates destination IP addresses, and visualizes global flows originating from Nairobi, Kenya.

The visualization includes:

- 🌍 Animated arcs from Nairobi to destination countries
- 💥 Pulsing rings at destination endpoints
- 🔴 Glowing Nairobi origin node
- 🔄 20-second refresh cycle for performance stability
- 📊 Sidebar traffic summary
- ⏸ Pause/Resume functionality

---

## 🧠 Architecture Overview

Live Network Traffic
│
▼
capture_traffic.py
(PyShark + TShark)
│
▼
traffic_processor.py

Threaded processing

IP geolocation (IPinfo API)

SQLite storage
│
▼
Flask API (app.py)
│
▼
Globe.gl Frontend
(Three.js rendering)

## 🛠 Technology Stack

### Backend
- Python 3
- Flask
- PyShark (TShark)
- SQLite
- IPinfo API
- Threading
- Requests

### Frontend
- Globe.gl
- Three.js
- HTML5
- CSS3
- Vanilla JavaScript

---

## 🔥 Features

- Live HTTP/HTTPS packet capture
- Real-time IP geolocation
- Public IP filtering
- SQLite-based packet persistence
- Animated 3D globe rendering
- Dynamic arc altitude scaling
- Pulsing impact rings
- Nairobi hardcoded as origin node
- 20-second controlled refresh cycle
- Thread-safe database operations
- API key protected endpoint

---

## 📁 Project Structure

RTNVS-CODE/
│
├── app.py
├── capture_traffic.py
├── traffic_processor.py
│
├── templates/
│ └── index.html
│
├── static/
│ └── style.css
│
├── requirements.txt
└── README.md

## ⚙️ Installation & Setup

 1️⃣ Clone the Repository

git clone https://github.com/death10101/RTNVIS.git
cd RTNVIS

2️⃣ Create Virtual Environment (Recommended)
python3 -m venv venv

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Install TShark (Required for PyShark)
On Debian/Kali/Ubuntu:

sudo apt install tshark

5️⃣ Configure IPinfo Token
In file ( traffic_processor.py ) replace:

token = "your_ipinfo_token_here"

With your IPInfo token

6️⃣ Run the Application
python3 app.py

Open:
http://127.0.0.1:5000

How It Works

- capture_traffic.py
Uses PyShark to capture TCP traffic on ports 80 and 443.
Pushes packet metadata into a queue.

- traffic_processor.py
Processes packets in a background thread.

- Filters private IPs.

- Geolocates public IP addresses.

 -Stores results in SQLite.

app.py

 -Serves Flask backend.

- Provides /api/traffic endpoint.

- Launches background capture thread.

index.html

- Fetches data every 20 seconds.

- Renders animated arcs.

- Displays pulsing destination rings.

- Highlights Nairobi origin node.

🔐 Security Considerations

- API key required for /api/traffic

- SQLite database excluded from GitHub

- Public IP filtering implemented

- Thread locking used for safe DB writes

📊 Performance Optimizations

- 20-second refresh interval

- Batched packet processing

- IP geolocation caching

- Limited result set (latest 100 packets)

- Dynamic arc altitude to prevent clipping

🎯 Use Cases

- Cybersecurity demonstrations

- Network behavior visualization

- Educational network traffic mapping

- Portfolio project for SOC / Blue Team roles

- Visualization of outbound traffic flows

🚀 Future Improvements

- Real-time WebSocket streaming

- Traffic heatmap visualization

- Attack pattern detection

- Packet rate analytics dashboard

- Docker containerization

- Cloud deployment

- Authentication & access control

- Historical traffic playback mode

Author
---------  Kinyanjui
---------- Cybersecurity | Networking | Visualization Engineering

SCREENSHOTS

<img width="1920" height="1080" alt="Screenshot From 2026-02-18 17-10-59" src="https://github.com/user-attachments/assets/c58344c3-a84b-49df-88af-b0162597f444" />
<img width="1920" height="1080" alt="Screenshot From 2026-02-18 17-19-25" src="https://github.com/user-attachments/assets/75c8159b-287e-4d9a-a186-f1828021b0c6" />
<img width="1920" height="1080" alt="Screenshot From 2026-02-18 17-11-07" src="https://github.com/user-attachments/assets/6437ae37-0c47-407d-9c9b-52f2544111d2" />
