#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

ROOT_IS_CREATED="$(kubectl exec services/gitea-svc -- su - git -c '/usr/local/bin/gitea admin user list')"
[[ "$ROOT_IS_CREATED" =~ "root" ]] || kubectl exec services/gitea-svc -- su - git -c "/usr/local/bin/gitea admin user create --admin --username root --password password --email admin@example.com" 
OAUTH_IS_CREATED="$(kubectl exec services/gitea-svc -- su - git -c '/usr/local/bin/gitea admin auth list')"
[[ "$OAUTH_IS_CREATED" =~ "gitea" ]] || kubectl exec services/gitea-svc -- su - git -c "/usr/local/bin/gitea admin auth add-oauth --name gitea --provider openidConnect -key gitea --secret 00000000-0000-0000-0000-000000000000 --auto-discover-url http://cluster.example.com/auth/realms/hello-world/.well-known/openid-configuration"

IAC_BLUE_TEAM_SOURCE_PATH="$SCRIPT_DIR/kube_infra"
IAC_RED_TEAM_DEST_PATH="$SCRIPT_DIR/red_team/.iac"
IAC_RED_TEAM_OUTPUT_FOLDER="$SCRIPT_DIR/red_team/.out"

[ -d "$IAC_RED_TEAM_DEST_PATH" ] && rm -r "$IAC_RED_TEAM_DEST_PATH"
[ -d "$IAC_RED_TEAM_OUTPUT_FOLDER" ] && rm -r "$IAC_RED_TEAM_OUTPUT_FOLDER"
mkdir -p "$IAC_RED_TEAM_DEST_PATH"
mkdir -p "$IAC_RED_TEAM_OUTPUT_FOLDER"

cp -r "$IAC_BLUE_TEAM_SOURCE_PATH" "$IAC_RED_TEAM_DEST_PATH"

[ -n "$(docker container ls -aq --filter name=red_team_extract_sso)" ] && docker container rm -f $(docker ps -aq --filter name=red_team_extract_sso) > /dev/null 2>&1
docker run --name red_team_extract_sso $(docker build red_team -f red_team/docker/extract_sso/Dockerfile -q) 
docker cp red_team_extract_sso:/usr/src/app/sso.json "$IAC_RED_TEAM_OUTPUT_FOLDER/sso.json"
