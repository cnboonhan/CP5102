#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

RESULTS_FILEPATH="$SCRIPT_DIR/kube_infra/k8s/results.json"
mkdir -p "$SCRIPT_DIR/kics_scan_results" 

docker run -t -u $(id -u ${USER}):$(id -g ${USER}) -v "$SCRIPT_DIR/kube_infra/k8s":/path checkmarx/kics scan -p "/path" -o "/path/"  || true
mv "$RESULTS_FILEPATH" "$SCRIPT_DIR/kics_scan_results"
