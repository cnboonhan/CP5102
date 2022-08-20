# CP5102

```
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube start --profile dev
minikube addons enable ingress
skaffold config set --global local-cluster true
eval $(minikube -p dev docker-env)

skaffold dev

lt --port 443
```

## TODO
```
# Add DB and Authentication
# Assume vulnerable K8S configuration
# Implement scans in test phase
# Detect Vulnerabilities
```
