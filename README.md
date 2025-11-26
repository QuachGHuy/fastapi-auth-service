# 🛡️ FastAPI Authentication Service

> A high-performance, secure, and dockerized Authentication Backend built with **Async Python**.

![Socialify Banner](https://socialify.git.ci/QuachGHuy/fastapi-auth-service/image?description=1&font=JetBrains+Mono&language=1&name=1&pattern=Formal+Invitation&theme=Dark)
<br>
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Test](https://img.shields.io/badge/Tests-Passing-brightgreen)

## 🛠️ Tech Stack

Built with a modern stack focused on **Performance** and **Developer Experience**:

| Component | Technology | Key Features |
| :--- | :--- | :--- |
| **Core** | `FastAPI` | Async I/O, Auto Swagger UI |
| **Database** | `PostgreSQL` | Accessed via `asyncpg` & `SQLAlchemy 2.0` |
| **Validation** | `Pydantic V2` | Strict data validation (Rust-based core) |
| **Security** | `JWT` + `Argon2` | OAuth2 standard, Secure password hashing |
| **DevOps** | `Docker Compose` | Multi-stage build, Isolated environments |
| **Testing** | `Pytest` | Unit & Integration tests with `httpx` |

## ✅ Features

- [x] **Authentication:** Register & Login (supports JSON & OAuth2 Form).
- [x] **Authorization:** JWT Bearer Token protection via Dependency Injection.
- [x] **Resilience:** Database health-checks to prevent startup race conditions.
- [x] **Architecture:** Layered Architecture (Router - Controller - Service - Data).
- [x] **Production Ready:** Dockerized with Dev/Prod environment separation.

## 🗺️ Roadmap

Future improvements:

- [ ] **API Key Management:** For Server-to-Server communication.
- [ ] **Social Login:** Google integration.
- [ ] **Refresh Token:** Long-lived sessions.
- [ ] **RBAC:** Role-based access control (Admin vs User).

## 🚀 Quick Start

Get the system running in **3 commands**:

### 1. Clone & Configure
```bash
git clone [https://github.com/YOUR_USERNAME/REPO_NAME.git](https://github.com/YOUR_USERNAME/REPO_NAME.git)
cd REPO_NAME

# Create environment variables from template
cp .env.example .env
```

### 2. Run with Docker (Recommended)

This will start both the Database and the API server.
Bash
```
docker compose up -d --build
```
### 3. Access API

Open your browser and navigate to:

    Docs: http://localhost:8000/docs

## 🧪 Development & Testing

To run the project manually (without Docker) for debugging or testing:
Bash

# 1. Setup Virtual Environment
```
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
```
# 2. Install Dev Dependencies
```
pip install -r requirements-dev.txt
```
# 3. Run Tests
```
python -m pytest -v
```
## 👤 Author

**Huy Quach**
* Github: https://github.com/QuachGHuy
* LinkedIn: www.linkedin.com/in/gia-huy-quach
