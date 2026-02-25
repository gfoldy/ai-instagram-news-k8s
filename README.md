🚀 AI Instagram News

A cloud-native Kubernetes web application that automatically ingests content, generates AI-enhanced summaries and images, and provides a dashboard for review and publishing.

---

## 🧠 Overview

AI Instagram News is a microservices-based application designed to demonstrate production-style Kubernetes architecture.

It:

- Ingests content on a schedule
- Uses OpenAI to generate summaries and captions
- Generates images (or image prompts) for posts
- Stores content in PostgreSQL
- Provides a Streamlit dashboard for review and approval
- Optionally publishes to Instagram
- Runs entirely inside Kubernetes (k3s compatible)

This project focuses on **cloud-native design, infrastructure as code, and real DevOps practices**.

---

## 🏗 Architecture

### Services

| Service | Type | Purpose |
|---|---|---|
| `review-ui` | Deployment | Web dashboard (Streamlit) |
| `publisher` | Deployment | Publishing logic + workflow control |
| `summarizer` | CronJob | Generates AI summaries and captions |
| `image-generator` | CronJob | Generates images for posts missing images |
| `ai-ingestor` | CronJob | Content ingestion pipeline |
| `postgres` | Deployment | Database |

### Networking

Public traffic flow:

```text
Browser
  ↓
Ingress (Port 80)
  ↓
review-ui Service (ClusterIP: 80)
  ↓
review-ui Pod (Container Port 8501)
```

- All services use `ClusterIP`
- Public access handled via Kubernetes Ingress (Traefik in k3s)
- No port-forwarding required

---

## ⚙️ What It Does

1. **Ingest content** (CronJob)  
   Pulls content from configured sources and stores it in the database.

2. **Generate AI content** (CronJob)  
   Uses OpenAI to generate summaries and captions for new posts.

3. **Generate images** (CronJob)  
   Generates images (or image data) for posts missing images.

4. **Store data** (PostgreSQL)  
   All posts and metadata are stored in a Postgres database inside the cluster.

5. **Review + approve** (Dashboard)  
   The `review-ui` dashboard lets a user review content and approve posts.

6. **Optional publishing**  
   If Instagram credentials are provided and publishing is enabled, the system can publish automatically.

---

## 🧰 Requirements

Before installing, you need:

- A Linux machine (Ubuntu recommended)
- Internet access
- Sudo privileges
- An OpenAI API key

Optional:

- Instagram credentials (only if you enable publishing)

You do **NOT** need a PostgreSQL account.  
PostgreSQL runs inside Kubernetes; you simply choose a password for the internal database user.

---

## 🛠 Install (One Command)

```bash
git clone https://github.com/gfoldy/ai-instagram-news-k8s.git
cd ai-instagram-news-k8s
sudo ./scripts/bootstrap.sh
```

---

## 🔐 Secrets / Prompts During Install

During `bootstrap.sh`, you will be prompted for:

- `OPENAI_API_KEY`
- `POSTGRES_PASSWORD` (internal database password you choose)
- Instagram credentials (optional, only if publishing is enabled)

Secrets are stored in Kubernetes Secrets and are **not committed** to GitHub.

---

## 🌐 Accessing The App

After install completes:

1. Find your server IP:

```bash
ip addr
```

2. Open the dashboard in your browser:

```text
http://<server-ip>
```

If deployed on a VPS:

```text
http://<public-ip>
```

---

## ✅ Verify Deployment

Check pods:

```bash
kubectl -n ai-news get pods
```

You should see (names will vary):

```text
review-ui-xxxxx     Running
publisher-xxxxx     Running
postgres-xxxxx      Running
```

Check services:

```bash
kubectl -n ai-news get svc
```

Check ingress:

```bash
kubectl -n ai-news get ingress
```

---

## 🔁 Updating The App

Pull the latest repo changes:

```bash
git pull
```

Re-apply Kubernetes manifests:

```bash
kubectl apply -f infra/k8s/base/
```

Or re-run the bootstrap script (safe for re-deploying):

```bash
sudo ./scripts/bootstrap.sh
```

---

## 📂 Project Structure

```text
.
├── infra/k8s/base/        # Kubernetes manifests (Deployments, Services, CronJobs, Ingress, Postgres)
├── scripts/bootstrap.sh   # One-command installer (k3s + secrets + deploy)
├── services/              # App source code + Dockerfiles for each service
└── .github/workflows/     # CI pipeline (build & push to GHCR)
```

---

## 🛡 Security Model

- No secrets are stored in the repo
- Secrets are created at install time and stored in Kubernetes Secrets
- Services are internal by default (ClusterIP)
- Ingress controls public access to the dashboard

---

## 🎯 Purpose / Why This Exists

This is a production-style DevOps portfolio project demonstrating:

- Kubernetes microservices architecture
- CronJobs for scheduled workers
- Ingress networking (k3s Traefik)
- GHCR-based container distribution
- Infrastructure as Code
- Cloud-native design principles

---

## 👨‍💻 Author

Garrett Foldy  
Cloud-Native / DevOps Portfolio Project
"""
