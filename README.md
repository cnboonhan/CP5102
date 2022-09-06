# CP5102

```
# Install jq, skaffold, kubectl and minikube 

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which kubectl); sudo setcap CAP_NET_BIND_SERVICE=+eip $(which skaffold)
# Use this to port forward manually, if needed
kubectl port-forward -n ingress-nginx services/ingress-nginx-controller 443:443 --address 0.0.0.0

# First Time Infra Setup
bash setup-all.bash
# Create root user
docker exec -u 1000 gitea gitea admin user create --admin --username root --password password --email admin@example.com 
# Login to Gitea at 192.168.49.1:8443 and create an Oauth Application under Settings > Applications 
# Set Application Name: keycloak, Redirect URI: https://192.168.49.1/auth/realms/hello-world/broker/gitea/endpoint, Submit
# Note the client ID and client secret, used next time

# Subsequent Launches
GITEA_CLIENT_ID=[gitea oauth client id] GITEA_CLIENT_SECRET=[gitea oauth client secret] bash setup-all.bash

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
