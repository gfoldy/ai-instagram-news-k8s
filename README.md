🧠 AI Instagram News – Cloud Native Kubernetes App
🚀 What This Is
AI Instagram News is a cloud-native, Kubernetes-based web application that:
Collects content
Generates AI-enhanced summaries and images
Stores content in Postgres
Provides a dashboard to review and approve posts
Optionally publishes to Instagram
Runs fully inside Kubernetes (k3s compatible)
Is installable with a single bootstrap script
This project is designed to demonstrate:
Cloud-native architecture
Microservices design
Kubernetes deployments
Ingress routing
CronJobs
Secrets management
Production-ready containerization
GitHub Container Registry integration
🏗 Architecture Overview
The system consists of:
🧩 Microservices
Service	Purpose
review-ui	Web dashboard (Streamlit)
publisher	AI image + post generation
summarizer	AI content summarization
ai-ingestor	Content ingestion pipeline
postgres	Database
🌐 Networking
Services are ClusterIP
Access is handled via Ingress
No port-forwarding required
Designed for VPS deployment
Flow:
Browser
   ↓
Ingress (80)
   ↓
review-ui service (80)
   ↓
review-ui container (8501)
⚙️ What It Does
1️⃣ Ingest Content
A CronJob ingests content from configured sources.
2️⃣ Generate AI Content
Uses OpenAI API to:
Summarize text
Generate captions
Create image prompts
3️⃣ Store Data
Posts are saved in Postgres.
4️⃣ Review Dashboard
User logs into dashboard to:
Review generated posts
Approve or reject content
5️⃣ Optional Publishing
If Instagram credentials are provided, posts can be published automatically.
🧰 Requirements
Before installing, you need:
Linux machine (Ubuntu recommended)
Internet access
Sudo access
OpenAI API key
Optional:
Instagram credentials
🛠 Installation (One Command)
Step 1 — Clone Repo
git clone https://github.com/gfoldy/ai-instagram-news-k8s.git
cd ai-instagram-news-k8s
Step 2 — Run Bootstrap Script
sudo ./scripts/bootstrap.sh
The script will:
Install k3s
Create namespace
Install all manifests
Set up Postgres
Deploy all services
Create Ingress
🔐 When You Will Be Prompted
During installation, you will be asked to enter:
OpenAI API Key
Postgres password (you create this)
Instagram credentials (optional)
⚠️ You do NOT need a Postgres account.
The database runs inside Kubernetes.
You simply create a password for your internal database.
🌐 Accessing The App
After installation completes:
Find your server IP:
ip addr
Then open in browser:
http://<server-ip>
If deployed on VPS:
http://<public-ip>
You should see the Review Dashboard.
📂 File Structure
.
├── infra/k8s/base
│   ├── ai-ingestor.yaml
│   ├── image-generator.yaml
│   ├── ingress.yaml
│   ├── postgres.yaml
│   ├── publisher.yaml
│   ├── review-ui.yaml
│   ├── summarizer.yaml
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
🧪 Verifying Installation
Check pods:
kubectl -n ai-news get pods
You should see:
review-ui   Running
publisher   Running
postgres    Running
Check ingress:
kubectl -n ai-news get ingress
🔁 CronJobs Behavior
The system includes scheduled jobs for:
Content ingestion
AI processing
Publishing
They are configured to:
Run on schedule
Complete
Not create infinite pods
Respect resource limits
🔧 How To Update The App
Pull latest changes:
git pull
Reapply manifests:
kubectl apply -f infra/k8s/base/
Or re-run:
sudo ./scripts/bootstrap.sh
🛡 Security Model
Secrets stored in Kubernetes secrets
No credentials hardcoded
Services isolated via namespace
Ingress controls public access
📈 Production Deployment
For real-world deployment:
Use a VPS
Point DNS to server IP
Add TLS certificate (Cert-Manager)
Use external Postgres (optional)
Add authentication to dashboard
Configure rate limits
🧠 Why This Project Matters
This project demonstrates:
Real Kubernetes architecture
Multi-service orchestration
CI/CD integration
Container registry usage
Production thinking
Infrastructure as Code
Cloud-native design
This is not a toy Docker app.
This is a real cloud-native deployment.
🔥 Future Improvements
Dashboard authentication
Role-based access
External Postgres support
Observability (Prometheus/Grafana)
Horizontal pod autoscaling
Production TLS
👨‍💻 Author
Garrett Foldy
Cloud-Native / DevOps / Kubernetes Portfolio Project
