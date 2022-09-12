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
KEYCLOAK_IDP_HOST=192.168.x.x bash setup-all.bash  # If Keycloak IDP is different

# One-Time SSO IDP setup
docker exec -it keycloak-idp bash 
/opt/keycloak/bin/kcadm.sh config credentials  --server http://127.0.0.1:8080 --realm master --user idp_admin --password password

## Create IDP SSO Realm and Client
/opt/keycloak/bin/kcadm.sh create realms -s realm=SSO -s enabled=true -o
/opt/keycloak/bin/kcadm.sh create clients -r SSO -s clientId=cp5102 -s 'redirectUris=["*"]' -s directAccessGrantsEnabled=true -s publicClient=true

## Create IDP Users
/opt/keycloak/bin/kcadm.sh create users -r SSO -s username=user1 -s enabled=true
/opt/keycloak/bin/kcadm.sh set-password -r SSO --username user1 --new-password password

# One-Time Gitea Setup ( Note that the secret has been hardcoded for automation purposes )
kubectl exec services/gitea-svc -- su - git -c "gitea admin user create --admin --username root --password password --email admin@example.com"
## Create Authentication Provider ( Set ip address to minikube IP if different )
gitea admin auth add-oauth --name gitea --provider openidConnect -key gitea --secret hJzobbxpUODhfBF6a3gHLk1TEp5o8cjK --auto-discover-url "http://192.168.49.2/auth/realms/hello-world/.well-known/openid-configuration"
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
