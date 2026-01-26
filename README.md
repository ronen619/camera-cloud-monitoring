# 🚀 Cloud-Native IoT & Camera Monitoring System

A high-performance, distributed monitoring solution designed to simulate, store, and alert on real-time camera detection events. This project demonstrates full-stack architecture, container orchestration, and cloud-native deployment.

---

## 🏗 System Architecture
The system follows a microservices-inspired design, ensuring scalability and **Fault Isolation**. All services are synchronized via a centralized Redis state-store.

| Service | Responsibility | Tech Stack |
| :--- | :--- | :--- |
| **Web Dashboard** | Real-time visualization of camera status | Flask, JavaScript (AJAX), HTML5/CSS3 |
| **Intelligent Bot** | Multi-threaded alerting & user interaction | Python (Telebot), Threading |
| **Simulator** | High-frequency data ingestion simulation | Python, Redis-py |
| **Database** | High-speed persistence & state management | Redis (NoSQL) |

---

## ✨ Key Features

### 🖥 Real-Time Web Interface
* **Asynchronous Updates:** Uses AJAX to fetch live data from Redis every 2 seconds for a seamless experience.
* **Localized UI:** Fully designed with RTL support for Hebrew-speaking environments.

### 🤖 Intelligent Telegram Bot
* **Smart Alerting Engine:** A dedicated background thread monitors thresholds (200+ detections) to send automated status summaries.
* **Detailed History:** On-demand retrieval of the last 10 detection events with sequence IDs and timestamps.

### ☁️ Cloud & Infrastructure
* **GCP Optimized:** Deployed on Google Cloud Platform using a hardened Linux environment.
* **Docker Orchestration:** Fully managed via Docker Compose, ensuring "Infrastructure as Code" consistency.
* **Proven Stability:** Successfully tested for long-term continuous uptime (48h+ logs).

---

## 🛠 Technical Stack
* **Infrastructure:** Google Cloud Platform (GCP), Ubuntu 22.04 LTS.
* **Orchestration:** Docker & Docker Compose.
* **Backend:** Python 3.9 (Flask, Telebot, Redis-py).
* **Database:** Redis (Configured with `appendonly` for data persistence).

---

## 🔧 Challenges & Engineering Solutions

> **Challenge:** Telegram's `long-polling` is a blocking operation, preventing the bot from monitoring data in real-time.
> **Solution:** Implemented Python **Multithreading** to decouple the Bot UI from the Monitoring Logic, allowing concurrent execution of alerts and commands.

---

## 🚀 Future Roadmap: Phase 2 (AI-Powered Insights)

* **Vision AI Integration:** Upgrading the simulator to use Object Detection models (e.g., YOLO or OpenAI Vision) to analyze camera content in real-time.
* **Anomaly Detection:** Implementing Machine Learning to identify unusual patterns (e.g., sudden spikes in activity) and trigger priority alerts.
* **Advanced Analytics:** Integrating **Grafana & Prometheus** for professional visualization of system health and detection trends.
* **Security Hardening:** Implementing a Reverse Proxy (Nginx) and SSL/TLS encryption for the web dashboard.

---

## 🚦 Getting Started
1. Clone the repository to your GCP instance.
2. Set environment variables (`TELEGRAM_TOKEN`, `CHAT_ID`).
3. Run: `docker compose up -d --build`

## 🚀 Live Demo
**[http://34.165.24.21:5000]**