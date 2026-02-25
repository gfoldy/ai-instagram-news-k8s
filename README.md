🚀 AI Instagram News
Cloud-Native Kubernetes Web Application
🧠 What This Project Is
AI Instagram News is a cloud-native Kubernetes application that:
Collects content
Generates AI-enhanced summaries and captions
Creates AI-based image prompts
Stores content in PostgreSQL
Provides a web dashboard for review
Optionally publishes to Instagram
Runs fully inside Kubernetes (k3s compatible)
It is designed as a production-style DevOps portfolio project demonstrating:
Kubernetes deployments
Microservices architecture
Ingress routing
CronJobs
Secrets management
GitHub Container Registry integration
Infrastructure as Code
🏗 Architecture Overview
Services
Service	Purpose
review-ui	Web dashboard (Streamlit)
publisher	AI caption + image prompt generation
summarizer	AI text summarization
ai-ingestor	Content ingestion pipeline
postgres	Database
🌐 Networking Flow
Browser
   ↓
Ingress (Port 80)
   ↓
review-ui Service (ClusterIP: 80)
   ↓
review-ui Container (8501)
All services use ClusterIP
External access is handled through Ingress
No port-forwarding required
⚙️ What The Application Does
Ingest Content
A Kubernetes CronJob collects content from configured sources.
Generate AI Content
Uses OpenAI API to:
Summarize text
Generate captions
Create image prompts
Store Data
Posts are stored in PostgreSQL inside the cluster.
Review Dashboard
The user accesses a web dashboard to:
Review generated posts
Approve or reject content
Optional Publishing
If Instagram credentials are provided, posts can be published automatically.
🧰 Requirements
Before installing:
Linux machine (Ubuntu recommended)
Internet access
Sudo privileges
OpenAI API key
Optional:
Instagram credentials
You do NOT need a PostgreSQL account.
The database runs inside Kubernetes.
🛠 Installation (One Command)
1️⃣ Clone the Repository
git clone https://github.com/gfoldy/ai-instagram-news-k8s.git
cd ai-instagram-news-k8s
2️⃣ Run the Bootstrap Script
sudo ./scripts/bootstrap.sh
The script will:
Install k3s
Create namespace
Deploy PostgreSQL
Deploy all microservices
Create Kubernetes secrets
Configure Ingress
Start CronJobs
🔐 During Installation You Will Be Prompted For:
OpenAI API key
PostgreSQL password (you create this)
Instagram credentials (optional)
Again — PostgreSQL runs inside the cluster.
You are just creating the internal database password.
🌐 Accessing The App
After installation:
Find your server IP:
ip addr
Then open in browser:
http://<server-ip>
If deployed on a VPS:
http://<public-ip>
You should see the Review Dashboard.
🧪 Verifying Installation
Check running pods:
kubectl -n ai-news get pods
Expected output:
review-ui     Running
publisher     Running
postgres      Running
Check ingress:
kubectl -n ai-news get ingress
📂 Project Structure
.
├── infra/k8s/base
│   ├── ai-ingestor.yaml
│   ├── image-generator.yaml
│   ├── ingress.yaml
│   ├── postgres.yaml
│   ├── publisher.yaml
│   ├── review-ui.yaml
│   └── summarizer.yaml
│
├── scripts
│   └── bootstrap.sh
│
├── services
│   ├── ai-ingestor/
│   ├── image-generator/
│   ├── publisher/
│   ├── review-ui/
│   └── summarizer/
│
└── .github/workflows
    └── build.yml
🔁 Updating The Application
Pull latest changes:
git pull
Reapply manifests:
kubectl apply -f infra/k8s/base/
Or re-run installer:
sudo ./scripts/bootstrap.sh
🛡 Security Model
Secrets stored in Kubernetes secrets
No credentials hardcoded
Namespace isolation
Ingress controls public access
📈 Production Deployment Recommendations
For real-world deployment:
Use a VPS
Add DNS pointing to server IP
Add TLS (Cert-Manager)
Add authentication to dashboard
Configure rate limiting
Add monitoring (Prometheus/Grafana)
💡 Why This Project Matters
This project demonstrates:
Real Kubernetes architecture
Multi-service orchestration
CI/CD container builds
Production-style networking
Cloud-native design principles
This is not a simple Docker demo.
It is a fully structured Kubernetes deployment.
👨‍💻 Author
Garrett Foldy
DevOps / Cloud-Native / Kubernetes Portfolio Project
