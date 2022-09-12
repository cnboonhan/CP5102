# CP5102

```
# Install jq skaffold, kubectl and minikube 

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which kubectl); sudo setcap CAP_NET_BIND_SERVICE=+eip $(which skaffold)
# Use this to port forward manually, if needed
kubectl port-forward -n ingress-nginx services/ingress-nginx-controller 443:443 --address 0.0.0.0

# First Time Infra Setup
bash setup-all.bash

# Teardown
bash teardown-all.bash
```

## TODO
```
# add instructions to modify realm file and setup-all.bash based on ip address / DNS changes
# Add DB and Authentication
# Assume vulnerable K8S configuration
# Implement scans in test phase
# Detect Vulnerabilities
```
