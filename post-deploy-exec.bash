#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

ROOT_IS_CREATED="$(kubectl exec services/gitea-svc -- su - git -c '/usr/local/bin/gitea admin user list')"
[[ "$ROOT_IS_CREATED" =~ "root" ]] || kubectl exec services/gitea-svc -- su - git -c "/usr/local/bin/gitea admin user create --admin --username root --password password --email admin@example.com" 
OAUTH_IS_CREATED="$(kubectl exec services/gitea-svc -- su - git -c '/usr/local/bin/gitea admin auth list')"
[[ "$OAUTH_IS_CREATED" =~ "gitea" ]] || kubectl exec services/gitea-svc -- su - git -c "/usr/local/bin/gitea admin auth add-oauth --name gitea --provider openidConnect -key gitea --secret 00000000-0000-0000-0000-000000000000 --auto-discover-url http://cluster.cp5102.edu/auth/realms/hello-world/.well-known/openid-configuration"

[ -n "$(docker container ls -aq --filter name=red_team)" ] && docker container rm red_team -f > /dev/null 2>&1
docker run --name red_team $(docker build . -q)
docker cp red_team:/usr/src/app/sso.gv.pdf .
