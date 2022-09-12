# CP5102

## Dependencies
```
# Install jq skaffold, kubectl and minikube 

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which kubectl); sudo setcap CAP_NET_BIND_SERVICE=+eip $(which skaffold)
# Use this to port forward manually, if needed
kubectl port-forward -n ingress-nginx services/ingress-nginx-controller 443:443 --address 0.0.0.0
```

## First Time Setup
```
bash setup-all.bash
# If Host for Keycloak IDP is not 192.168.49.1, you can set it manually:
KEYCLOAK_IDP_HOST=192.168.x.x bash setup-all.bash

# One-Time SSO IDP setup
# visit https://192.168.49.1:8443, log in with credentials idp_admin / password and load realms-idp.json
# Create Users
docker exec -it keycloak-idp bash 
/opt/keycloak/bin/kcadm.sh config credentials  --server http://127.0.0.1:8080 --realm SSO --user idp_admin --password password
/opt/keycloak/bin/kcadm.sh create users -r SSO -s username=user1 -s enabled=true
/opt/keycloak/bin/kcadm.sh set-password -r SSO --username user1 --new-password password
```

## TearDown
```
bash teardown-all.bash
```

## TODO
```
# Assume vulnerable K8S configuration
# Implement scans in test phase
# Detect Vulnerabilities
```
