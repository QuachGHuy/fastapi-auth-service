# 🛡️ FastAPI Authentication Service

> A high-performance, secure, and dockerized Authentication Backend built with **Async Python**.

![Socialify Banner](https://socialify.git.ci/QuachGHuy/fastapi-auth-service/image?description=1&font=JetBrains+Mono&language=1&name=1&pattern=Formal+Invitation&theme=Dark)
<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-F04028?logo=alembic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Test](https://img.shields.io/badge/Tests-Passing-brightgreen)

## 🛠️ Tech Stack

Built with a modern stack focused on **Performance**, **Scalability**, and **Developer Experience**:

| Component | Technology | Key Features |
| :--- | :--- | :--- |
| **Core** | `FastAPI` | Async I/O, Auto Swagger UI |
| **Database** | `PostgreSQL` | Accessed via `asyncpg` |
| **ORM & Migrations** | `SQLAlchemy 2.0` + `Alembic` | Type-safe queries & Schema version control |
| **Validation** | `Pydantic V2` | Strict data validation (Rust-based core) |
| **Security** | `JWT` + `Argon2` | OAuth2 standard, Secure password hashing |
| **DevOps** | `Docker Compose` | Multi-stage build, Isolated environments |
| **Testing** | `Pytest` | Unit & Integration tests with `httpx` |

## ✅ Features

- [x] **Authentication:** Register & Login (supports JSON & OAuth2 Form).
- [x] **Authorization:** JWT Bearer Token protection via Dependency Injection.
- [x] **Database Migrations:** Managed schema changes using Alembic (No more manual SQL).
- [x] **Resilience:** Database health-checks to prevent startup race conditions.
- [x] **Architecture:** Clean/Layered Architecture (Router - Service - CRUD - Schema).
- [x] **Production Ready:** Dockerized with Dev/Prod environment separation.

## 🗺️ Roadmap

Future improvements:

- [ ] **API Key Management:** For Server-to-Server communication.
- [ ] **Social Login:** Google integration.
- [ ] **Refresh Token:** Long-lived sessions with rotation.
- [ ] **RBAC:** Role-based access control (Admin vs User).

## 🚀 Quick Start

Get the system running in **3 steps**:

### 1. Clone & Configure
```bash
git clone [https://github.com/QuachGHuy/fastapi-auth-service.git](https://github.com/QuachGHuy/fastapi-auth-service.git)
cd fastapi-auth-service

# Create environment variables from template
cp .env.example .env
```

### 2. Run with Docker (Recommended)

This will start the Database, apply migrations, and launch the API server.
Bash
```bash
docker compose up -d --build
```

### 3. Access API

Open your browser and navigate to:

    Docs: http://localhost:8000/docs

    Redoc: http://localhost:8000/redoc

📦 Database Migrations (Alembic)

This project uses Alembic to manage database schema changes.

Initialize DB (First run):
```Bash
# Apply all migrations to the database
docker compose exec api alembic upgrade head
```

Create a new migration (after modifying models):
```Bash
# Auto-generate migration file based on model changes
docker compose exec api alembic revision --autogenerate -m "Describe your change here"

# Apply the new migration
docker compose exec api alembic upgrade head
```
🧪 Development & Testing

To run the project manually (without Docker) for debugging or testing:

### 1. Setup Virtual Environment

```Bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
```
### 2. Install Dependencies

```Bash
pip install -r requirements_dev.txt
```
### 3. Run Migrations & Server

```Bash

# Apply migrations locally
alembic upgrade head

# Start Server
uvicorn app.main:app --reload --port 9000
```
### 4. Run Tests

```Bash
python -m pytest -v
```

👤 Author
Huy Quach
    Github: https://github.com/QuachGHuy
    LinkedIn: www.linkedin.com/in/gia-huy-quach
