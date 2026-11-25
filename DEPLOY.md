# Deploying to AWS (EC2 + Docker Compose)

The `.github/workflows/deploy.yml` workflow is **manual**: trigger it from the
**Actions** tab → "Deploy to AWS EC2" → **Run workflow**. It SSHes into an EC2
box, pulls the latest `master`, and runs `docker compose up --build -d`.

This repo has no Terraform/CloudFormation, so the EC2 instance and its one-time
setup need to be done by hand first.

## 1. Create the EC2 instance

1. Launch an EC2 instance (Amazon Linux 2023 or Ubuntu 22.04, `t3.small` or
   bigger — `t3.micro` is tight once Postgres + backend + frontend are all
   running).
2. Security group inbound rules:
   - `22` (SSH) from your IP (or GitHub Actions' IP range if you lock it down)
   - `5173` (frontend) from `0.0.0.0/0`
   - `8000` (backend) from `0.0.0.0/0` — or skip this and have the frontend
     call the backend over a reverse proxy/same host instead of exposing it
     publicly
3. Allocate/associate an Elastic IP so the host address doesn't change.
4. Create (or reuse) an SSH key pair for connecting to the instance.

## 2. One-time server setup

SSH into the instance and install Docker + Compose:

```bash
# Amazon Linux 2023
sudo dnf install -y docker git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# log out/in so the group change takes effect, then:
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
  -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

Clone the repo once, and seed the database once:

```bash
git clone https://github.com/<your-org-or-user>/booking-management-system.git
cd booking-management-system
docker compose up --build -d
docker compose exec backend uv run python -m app.seed
```

Note the absolute path you cloned into (e.g. `/home/ec2-user/booking-management-system`)
— you'll need it for the `EC2_PROJECT_PATH` secret below.

## 3. GitHub repo secrets

In **Settings → Secrets and variables → Actions**, add:

| Secret               | Value                                                            |
| --------------------- | ----------------------------------------------------------------- |
| `EC2_HOST`            | Public IP or DNS of the instance                                  |
| `EC2_USERNAME`        | SSH user (e.g. `ec2-user` for Amazon Linux, `ubuntu` for Ubuntu) |
| `EC2_SSH_KEY`         | Contents of the **private** key (`.pem`) matching the instance's key pair |
| `EC2_PROJECT_PATH`    | Absolute path to the cloned repo on the instance                  |
| `EC2_SSH_PORT`        | Optional, only needed if SSH isn't on port 22                     |

## 4. Running it

Go to **Actions → Deploy to AWS EC2 → Run workflow**. Each run pulls the
latest `master` on the box and rebuilds/restarts the containers in place.

## Notes / limitations

- This deploys exactly what `docker-compose.yml` runs locally: Postgres,
  FastAPI with `--reload`, and the Vite dev server. That's fine for an
  educational project, but it is **not** a production-grade setup (no HTTPS,
  no process supervision beyond Docker's restart policy, dev servers instead
  of built/optimized assets, Postgres data lives only on the instance's disk).
- The seed step is intentionally **not** part of the workflow so re-running
  the deploy doesn't duplicate sample data; only run `app.seed` once.
