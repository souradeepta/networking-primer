#!/usr/bin/env bash
# Read-only DNS observation. Usage: ./demos/dns_observe.sh [name] [resolver]
set -u

name="${1:-example.invalid}"
resolver="${2:-}"
echo "Query: ${name} A"
echo "Timestamp (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
if command -v dig >/dev/null 2>&1; then
  if [[ -n "$resolver" ]]; then
    dig +noall +answer +authority +comments "@${resolver}" "$name" A
  else
    dig +noall +answer +authority +comments "$name" A
  fi
else
  echo "dig is required; install approved DNS utilities or run the equivalent nslookup command." >&2
  exit 2
fi
