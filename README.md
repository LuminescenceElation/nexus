# Nexus: Ansible Infrastructure-as-Code

Automated deployment of a production-ready multi-tier application stack using Ansible configuration management.

## What It Does

Nexus orchestrates the complete setup of:
- **Nginx** — Reverse proxy and web server (port 80)
- **FastAPI** — Python web application (port 8000, proxied through Nginx)
- **PostgreSQL** — Relational database with application schema and user

All services are configured to auto-start and auto-recover on failure.

## Architecture

User (HTTP:80)

↓

Nginx (Reverse Proxy)

↓

FastAPI App (127.0.0.1:8000)

↓

PostgreSQL (nexus_db)

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

nexus/

├── README.md

├── ansible.cfg           # Ansible configuration

├── inventory.ini         # Target hosts

├── playbooks/

│   └── deploy.yml        # Main deployment playbook

├── roles/

│   ├── common/tasks/main.yml

│   ├── postgresql/tasks/main.yml

│   ├── fastapi/tasks/main.yml

│   └── nginx/tasks/main.yml

└── files/

└── app.py            # FastAPI application

## Roles Explained

**common** — Updates system packages, sets timezone

**postgresql** — Installs PostgreSQL, creates database and application user

**fastapi** — Creates venv, installs dependencies, sets up systemd service

**nginx** — Installs Nginx, configures reverse proxy to FastAPI

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

## Author

Leo Patsalides | [GitHub](https://github.com/LuminescenceElation)