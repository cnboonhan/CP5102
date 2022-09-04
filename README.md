# CP5102

```
# Clone and make tests executable
git clone https://github.com/cnboonhan/CP5102

# Install skaffold, kubectl and minikube binaries
# Optiional, set up Wiregard / Tailscale for extended access

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which kubectl)
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which skaffold)
# Use this to port forward manually, if needed
kubectl port-forward -n ingress-nginx services/ingress-nginx-controller 443:443 --address 0.0.0.0

# Infra Setup
bash setup-all.bash

# Teardown
bash teardown-all.bash
```

## TODO
```
# Add DB and Authentication
# Assume vulnerable K8S configuration
# Implement scans in test phase
# Detect Vulnerabilities
```
