# Cloud-Native Real-Time Camera Monitoring System

A multi-service monitoring application built to simulate real-time camera data ingestion and visualization. This project demonstrates high-availability deployment, container orchestration, and cloud infrastructure management.

## 🚀 Live Demo
**[Insert Your Cloud IP here, e.g., http://10.208.0.2:9000]**
*(Note: Instance may be paused to save costs)*

## 🛠 Tech Stack
* **Cloud Infrastructure:** Google Cloud Platform (GCP) - Compute Engine.
* **Orchestration:** Docker & Docker Compose.
* **Backend:** Python (Flask).
* **Database:** Redis (NoSQL) for real-time data persistence.
* **Frontend:** HTML5, CSS3 (RTL support), and JavaScript (AJAX for real-time updates).
* **OS:** Ubuntu 22.04 LTS.

## 🏗 Architecture
The system follows a microservices architecture:
1. **App Service:** A Flask-based web server that processes camera samples and provides a RESTful API.
2. **Database Service:** A Redis instance used as a high-speed data store for counting and state management.
3. **Connectivity:** Services communicate over a private Docker network, isolated from the public internet, with only necessary ports exposed via GCP Firewall.

## ✨ Key Features
* **Real-Time Updates:** Uses asynchronous JavaScript (AJAX) to fetch updates from the Redis store every 2 seconds without page refreshes.
* **Cloud-Native Deployment:** Fully containerized and deployed on a virtualized Linux environment in the cloud.
* **Self-Healing:** Containers are configured with restart policies to ensure maximum uptime.
* **RTL Support:** Fully localized UI for Hebrew-speaking environments.

## 🔧 How to Run Locally
1. Clone the repository.
2. Ensure Docker and Docker Compose are installed.
3. Run:
   ```bash
   docker-compose up -d --build
