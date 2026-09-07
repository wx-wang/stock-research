#!/usr/bin/env bash
set -euo pipefail

# Read-only Tushare MCP transport helper.
# The endpoint/token must be provided by the runtime; never store credentials here.

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "usage: TUSHARE_MCP_URL='https://...' $0 <tool_name> [json_arguments]" >&2
  exit 2
fi

if [ -z "${TUSHARE_MCP_URL:-}" ]; then
  echo "TUSHARE_MCP_URL is required" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 2
fi

tool_name="$1"
if [ "$#" -eq 2 ]; then
  arguments="$2"
else
  arguments='{}'
fi

if ! printf '%s' "$arguments" | jq -e . >/dev/null 2>&1; then
  echo "json_arguments must be valid JSON" >&2
  exit 2
fi

request_body="$(jq -cn \
  --arg name "$tool_name" \
  --argjson arguments "$arguments" \
  '{jsonrpc:"2.0",id:1,method:"tools/call",params:{name:$name,arguments:$arguments}}')"

response="$(curl -fsS --max-time "${TUSHARE_MCP_TIMEOUT:-30}" \
  -X POST "$TUSHARE_MCP_URL" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d "$request_body")"

message="$(printf '%s\n' "$response" | sed -n 's/^data: //p' | tail -n 1)"
if [ -z "$message" ]; then
  echo "Tushare MCP returned no JSON-RPC message" >&2
  exit 1
fi

if printf '%s' "$message" | jq -e '.error' >/dev/null 2>&1; then
  printf '%s\n' "$message" | jq -c '.error' >&2
  exit 1
fi

if printf '%s' "$message" | jq -e '.result.isError == true' >/dev/null 2>&1; then
  printf '%s\n' "$message" | jq -r '.result.content[]?.text // "Tushare tool error"' >&2
  exit 1
fi

# Tushare MCP returns tabular data as JSON text in a text content block.
printf '%s\n' "$message" | jq -r '.result.content[]? | select(.type == "text") | .text'
