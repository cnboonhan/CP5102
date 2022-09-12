#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

kubectl exec services/gitea-svc -- su - git -c '/usr/local/bin/gitea admin user create --admin --username root --password password --email admin@example.com'
kubectl exec services/gitea-svc -- su - git -c "/usr/local/bin/gitea admin auth add-oauth --name gitea --provider openidConnect -key gitea --secret hJzobbxpUODhfBF6a3gHLk1TEp5o8cjK --auto-discover-url http://$(minikube ip)/auth/realms/hello-world/.well-known/openid-configuration"
