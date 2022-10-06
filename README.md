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
# configure external-infra/coredns-config/Corefile and kube-infra/k8s/coredns with DNS configurations
# Set up local /etc/resolv.conf with nameserver 172.28.0.4
bash setup-all.bash

# One-Time SSO IDP setup
docker exec -it keycloak-idp bash 
/opt/keycloak/bin/kcadm.sh config credentials  --server http://127.0.0.1:8080/auth --realm master --user idp_admin --password password

## Create IDP SSO Realm and Client
/opt/keycloak/bin/kcadm.sh create realms -s realm=SSO -s enabled=true -o
/opt/keycloak/bin/kcadm.sh create clients -r SSO -s clientId=cp5102 -s 'redirectUris=["*"]' -s directAccessGrantsEnabled=true -s publicClient=false -s clientAuthenticatorType=client-secret -s secret=00000000-0000-0000-0000-000000000000

## Create IDP Users
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
