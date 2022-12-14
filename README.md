# Red Team Automation Demo

## Dependencies
```
# Install docker, docker-compose, jq, skaffold, kubectl, yamale and minikube 

# For privileged port-forwarding
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which kubectl); sudo setcap CAP_NET_BIND_SERVICE=+eip $(which skaffold)
# Use this to port forward manually, if needed
kubectl port-forward -n ingress-nginx services/ingress-nginx-controller 443:443 --address 0.0.0.0
```

## First Time Setup
```
# configure external_infra/coredns-config/Corefile and kube_infra/k8s/coredns with DNS configurations
# Set up local /etc/systemd/resolved.conf with the following:
[Resolve]
DNS=172.28.0.53
Domains=example.com,cluster.example.com

# Then run
sudo service systemd-resolved restart

# Setup script:
bash setup-all.bash

# One-Time SSO IDP setup
docker exec -it keycloak-idp bash 
/opt/keycloak/bin/kcadm.sh config credentials  --server http://127.0.0.1:8080/auth --realm master --user idp_admin --password password

## Create IDP SSO Realm and Client
/opt/keycloak/bin/kcadm.sh create realms -s realm=SSO -s enabled=true -o
/opt/keycloak/bin/kcadm.sh create clients -r SSO -s clientId=example -s 'redirectUris=["*"]' -s directAccessGrantsEnabled=true -s publicClient=false -s clientAuthenticatorType=client-secret -s secret=00000000-0000-0000-0000-000000000000

## Create IDP Users
/opt/keycloak/bin/kcadm.sh create users -r SSO -s username=user1 -s enabled=true
/opt/keycloak/bin/kcadm.sh set-password -r SSO --username user1 --new-password password
```

## TearDown
```
bash teardown-all.bash
```
