# CP5102

```
# Install skaffold, kubectl and minikube binaries
# Optiional, set up Wiregard / Tailscale for extended access

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip /usr/local/bin/kubectl

minikube start --profile dev
minikube profile dev
minikube addons enable ingress
skaffold config set --global local-cluster true
eval $(minikube -p dev docker-env)

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
