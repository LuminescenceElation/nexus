# Nexus: Ansible Infrastructure-as-Code

Automated deployment of a production-ready multi-tier application stack using Ansible configuration management.

## What It Does

Nexus orchestrates the complete setup of:
- **Nginx** — Reverse proxy and web server (port 80)
- **FastAPI** — Python web application (port 8000, proxied through Nginx)
- **PostgreSQL** — Relational database with application schema and user

All services are configured to auto-start and auto-recover on failure.

## Why Nexus?

This project demonstrates core DevOps practices:
- **Infrastructure as Code** — Declarative, reproducible deployments
- **Configuration Management** — Idempotent, version-controlled infrastructure
- **Service Orchestration** — Multi-tier stack with dependency management
- **Production Readiness** — Auto-recovery, systemd integration, health checks

It answers the question: *"How do you reliably deploy a full application stack without manual steps?"*

## Architecture

```
User (HTTP:80)
↓
Nginx (Reverse Proxy)
↓
FastAPI App (127.0.0.1:8000)
↓
PostgreSQL (nexus_db)
```

## Quick Start

### Prerequisites
- Ansible 2.16+
- Target Ubuntu 22.04+ server with SSH access
- SSH key-based authentication configured

### Deploy

```bash
cd ~/nexus
ansible-playbook -i inventory.ini playbooks/deploy.yml -K
# Enter BECOME password when prompted
```

### Verify

```bash
# SSH into target server
ssh ubuntu@<server-ip>

# Check services
sudo systemctl status nginx
sudo systemctl status fastapi
sudo systemctl status postgresql

# Test API
curl http://localhost/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-06-27T11:13:24.827499"
}
```

## Project Structure

```
nexus/
├── README.md
├── ansible.cfg              # Ansible configuration
├── inventory.ini            # Target hosts
├── playbooks/
│   └── deploy.yml           # Main deployment playbook
├── roles/
│   ├── common/tasks/main.yml
│   ├── postgresql/tasks/main.yml
│   ├── fastapi/tasks/main.yml
│   └── nginx/tasks/main.yml
├── files/
│   └── app.py               # FastAPI application
└── app.py                   # FastAPI application
```

## Roles Explained

**common** — System-level setup: package updates, timezone configuration, base tools (git, curl, build-essential)

**postgresql** — Database layer: installs PostgreSQL, creates application database (`nexus_db`), application user (`app_user`), and schema with `items` table for the API

**fastapi** — Application layer: creates isolated Python venv, installs dependencies (FastAPI, Uvicorn, psycopg2), copies application code, creates systemd service for auto-start/auto-recovery

**nginx** — Reverse proxy layer: installs Nginx, configures upstream proxy to FastAPI (port 8000), handles HTTP headers, removes default site

## Key Features

✅ **Idempotent** — Safe to run multiple times  
✅ **Reproducible** — Same deployment every time  
✅ **Auto-recovery** — Services restart on failure  
✅ **Database integrated** — Full stack working together  

## Technologies

- **Ansible** — Infrastructure orchestration
- **FastAPI** — Python async web framework
- **PostgreSQL** — Relational database
- **Nginx** — High-performance web server
- **systemd** — Service management

## Interview Talking Points

**Key concepts demonstrated:**
- Ansible roles for modularity and reusability
- Idempotent task design (safe to run multiple times)
- Systemd integration for service management and auto-recovery
- Reverse proxy configuration (Nginx upstream)
- Multi-tier architecture: web server → app → database
- Environment isolation (venv, dedicated app user paths)
- Declarative vs. imperative infrastructure

**Why this architecture:**
- Nginx handles HTTP concerns (headers, SSL in production, caching)
- Separation of concerns keeps each layer focused
- systemd handles service lifecycle (start on boot, restart on crash)
- Virtual environment isolates app dependencies from system Python
- PostgreSQL as separate tier allows independent scaling

**What I'd improve in production:**
- Dedicated service user (not root) for FastAPI
- SSL/TLS termination in Nginx
- Environment variables for database credentials (not hardcoded)
- Separate database host (not localhost)
- Health checks and monitoring (Prometheus/Grafana)
- Logging aggregation (ELK stack or cloud provider logs)
- Load balancing for high availability
- Database backups and recovery strategy

**What this taught me:**
- Ansible's idempotency principle (tasks are safe to repeat)
- The importance of service dependencies and ordering
- How reverse proxies abstract application details
- Systemd as the modern init system
- Testing infrastructure code before production use

## Author

Leonidas John Patsalides