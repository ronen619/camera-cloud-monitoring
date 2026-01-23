# 🚀 Cloud-Native IoT & Camera Monitoring System

A high-performance, distributed monitoring solution designed to simulate, store, and alert on real-time camera detection events. This project demonstrates full-stack architecture, container orchestration, and cloud-native deployment strategies.

---

## 🏗 System Architecture
The system follows a microservices-inspired design, ensuring scalability and isolation between components:

| Service | Responsibility | Tech Stack |
| :--- | :--- | :--- |
| **Web Dashboard** | Real-time visualization of camera status | Flask, JavaScript (AJAX), HTML5/CSS3 |
| **Intelligent Bot** | Multi-threaded alerting & user interaction | Python (Telebot), Threading |
| **Simulator** | High-frequency data ingestion simulation | Python, Redis-py |
| **Database** | High-speed persistence & state management | Redis (NoSQL) |


---

## ✨ Key Features

### 🖥 Real-Time Web Interface
* **Asynchronous Updates:** Uses AJAX to fetch live data from Redis every 2 seconds, providing a seamless experience without page refreshes.
* **Localized UI:** Fully designed with RTL (Right-to-Left) support for Hebrew-speaking environments.

### 🤖 Intelligent Telegram Bot
* **Smart Alerting Engine:** A dedicated background thread monitors data thresholds (e.g., 200+ detections) to send automated status summaries.
* **Detailed History:** On-demand retrieval of the last 10 detection events, including unique Sequence IDs and precise timestamps.

### ☁️ Cloud & Infrastructure
* **GCP Optimized:** Deployed on Google Cloud Platform (Compute Engine) using a hardened Linux environment.
* **Self-Healing:** Configured with Docker restart policies to ensure maximum uptime (Proven 48h+ continuous stability).

---

## 🛠 Technical Stack

* **Infrastructure:** Google Cloud Platform (GCP), Ubuntu 22.04 LTS.
* **Orchestration:** Docker & Docker Compose.
* **Backend:** Python 3.9 (Flask, Telebot, Redis-py).
* **Database:** Redis (Key-Value & Lists for chronological logging).
* **Frontend:** HTML5, CSS3, JavaScript (AJAX).

---

## 🔧 Challenges & Engineering Solutions

> **Challenge:** Telegram's `long-polling` is a blocking operation, which prevented the bot from monitoring Redis data in real-time.
> **Solution:** Implemented Python `threading` to decouple the Bot UI from the Monitoring Logic, allowing concurrent execution of user commands and automated alerts.

> **Challenge:** Maintaining a "Single Source of Truth" across multiple containers.
> **Solution:** Leveraged Redis as a centralized state-store, ensuring the Simulator, Web App, and Bot always operate on synchronized data.

---

## 🚦 Getting Started

### Prerequisites
* Docker and Docker Compose installed.
* A Telegram Bot Token (via BotFather).

### Deployment
1. Clone the repository to your GCP instance.
2. Create a `.env` file with your `TELEGRAM_TOKEN`.
3. Launch the system:
   ```bash
   docker compose up -d --build