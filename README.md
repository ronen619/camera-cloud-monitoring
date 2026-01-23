Cloud-Native IoT & Camera Monitoring System
A distributed monitoring solution designed to simulate, store, and alert on real-time camera detection events. This project demonstrates full-stack architecture, container orchestration, and cloud-native deployment.

🚀 Live Demo
[Insert Your Cloud IP here, e.g., http://34.165.24.21:5000] (Note: Instance may be paused to save costs)

🏗 Architecture
The system follows a microservices-inspired architecture, deployed on Google Cloud Platform (GCP):

App Service (Web): A Flask-based web server providing a real-time dashboard with RTL support and AJAX updates.

Intelligent Bot Service: A multi-threaded Python application handling Telegram interactions and background data monitoring.

Simulation Service: A Python background worker generating real-time camera detection events.

Database Service: A Redis (NoSQL) instance used for high-speed data persistence and state management.

✨ Key Features
Real-Time Web Updates: Uses asynchronous JavaScript (AJAX) to fetch updates from Redis every 2 seconds without page refreshes.

Smart Telegram Alerting: Background threads monitor Redis for threshold violations (e.g., 200+ detections) and send automated status summaries.

Chronological History: On-demand retrieval of the last 10 detection events with precise timestamps via the Bot interface.

Cloud-Native Deployment: Fully containerized via Docker Compose, ensuring a consistent environment between development and cloud.

RTL Support: Fully localized UI for Hebrew-speaking environments.

🛠 Tech Stack
Infrastructure: Google Cloud Platform (GCP) - Compute Engine.

Orchestration: Docker & Docker Compose.

Languages: Python 3.9 (Flask, Telebot, Threading), JavaScript (AJAX).

Database: Redis (NoSQL) for real-time data persistence.

OS: Ubuntu 22.04 LTS.

🔧 Challenges & Solutions
Concurrency: Implemented Python threading to allow the Telegram bot to listen for user commands while simultaneously monitoring Redis data for alerts.

Data Integrity: Leveraged Redis as a centralized state-store, ensuring the Simulator, Web App, and Bot always operate on synchronized "single source of truth" data.