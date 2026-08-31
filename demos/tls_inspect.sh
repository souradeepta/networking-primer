#!/usr/bin/env bash
# Read-only TLS/SNI inspection. Usage: ./demos/tls_inspect.sh [host] [port] [sni]
set -u

host="${1:-127.0.0.1}"
port="${2:-8443}"
sni="${3:-example.test}"
echo "Inspecting ${host}:${port} with SNI ${sni}"
echo "No certificate verification bypass is used."
if ! command -v openssl >/dev/null 2>&1; then
  echo "openssl is required." >&2
  exit 2
fi
openssl s_client -connect "${host}:${port}" -servername "$sni" \
  -showcerts -verify_return_error </dev/null
status=$?
if [[ $status -ne 0 ]]; then
  echo "TLS inspection failed with status ${status}; distinguish reachability from certificate evidence." >&2
fi
exit "$status"
