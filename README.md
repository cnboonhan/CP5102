# CP5102

```
# Clone and make tests executable
git clone https://github.com/cnboonhan/CP5102
chmod +x pre-deploy-exec.bash

# Install skaffold, kubectl and minikube binaries
# Optiional, set up Wiregard / Tailscale for extended access

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip /usr/local/bin/kubectl

# Infra Setup
minikube start --profile dev
minikube profile dev
minikube addons enable ingress
skaffold config set --global local-cluster true
eval $(minikube -p dev docker-env)
docker pull checkmarx/kics:latest

skaffold dev

kubectl port-forward -n ingress-nginx services/ingress-nginx-controller 443:443 --address 0.0.0.0
```

## TODO
```
# Add DB and Authentication
# Assume vulnerable K8S configuration
# Implement scans in test phase
# Detect Vulnerabilities
```
