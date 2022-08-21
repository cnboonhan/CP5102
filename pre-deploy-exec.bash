#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

RESULTS_FILEPATH="$SCRIPT_DIR/k8s/results.json"
mkdir -p "$SCRIPT_DIR/kics_scan_results" 

docker run -t -u $(id -u ${USER}):$(id -g ${USER}) -v "$SCRIPT_DIR/k8s":/path checkmarx/kics scan -p "/path" -o "/path/" 
mv "$RESULTS_FILEPATH" "$SCRIPT_DIR/kics_scan_results"
