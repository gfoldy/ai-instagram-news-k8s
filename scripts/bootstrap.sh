#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="ai-news"
MANIFEST_PATH="infra/k8s/base"
KUBECONFIG_PATH="/etc/rancher/k3s/k3s.yaml"

# -----------------------------
# 1. Ensure root
# -----------------------------
if [[ "${EUID}" -ne 0 ]]; then
  echo "❌ Please run with sudo."
  exit 1
fi

# -----------------------------
# 2. Install k3s if needed
# -----------------------------
if ! command -v k3s >/dev/null 2>&1; then
  echo "🚀 Installing k3s..."
  curl -sfL https://get.k3s.io | sh -
else
  echo "✅ k3s already installed"
fi

export KUBECONFIG="$KUBECONFIG_PATH"

# -----------------------------
# 3. Wait for node
# -----------------------------
echo "⏳ Waiting for Kubernetes node..."
kubectl wait --for=condition=Ready node --all --timeout=180s

# -----------------------------
# 4. Create namespace
# -----------------------------
kubectl create namespace $NAMESPACE 2>/dev/null || true

# -----------------------------
# 5. Prompt for secrets
# -----------------------------
echo "🔐 Enter OpenAI API Key:"
read -s OPENAI_API_KEY
echo

echo "🔐 Enter Postgres Password:"
read -s POSTGRES_PASSWORD
echo

echo "🔐 Instagram Username (optional):"
read INSTAGRAM_USERNAME

if [[ -n "$INSTAGRAM_USERNAME" ]]; then
  echo "🔐 Instagram Password:"
  read -s INSTAGRAM_PASSWORD
  echo
fi

# -----------------------------
# 6. Create secrets
# -----------------------------
DATABASE_URL="postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/posts"

kubectl -n $NAMESPACE create secret generic openai-secret \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n $NAMESPACE create secret generic database-secret \
  --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --dry-run=client -o yaml | kubectl apply -f -

if [[ -n "$INSTAGRAM_USERNAME" ]]; then
  kubectl -n $NAMESPACE create secret generic instagram-secret \
    --from-literal=INSTAGRAM_USERNAME="$INSTAGRAM_USERNAME" \
    --from-literal=INSTAGRAM_PASSWORD="$INSTAGRAM_PASSWORD" \
    --dry-run=client -o yaml | kubectl apply -f -
fi

echo "✅ Secrets created"

# -----------------------------
# 7. Apply manifests
# -----------------------------
echo "📦 Deploying infrastructure + services..."
kubectl -n $NAMESPACE apply -f $MANIFEST_PATH

# -----------------------------
# 8. Wait for Postgres
# -----------------------------
echo "⏳ Waiting for Postgres..."
kubectl -n $NAMESPACE rollout status deploy/postgres --timeout=180s

# -----------------------------
# 9. Final status
# -----------------------------
echo
echo "🎉 Deployment complete!"
kubectl -n $NAMESPACE get pods -o wide
kubectl -n $NAMESPACE get svc
