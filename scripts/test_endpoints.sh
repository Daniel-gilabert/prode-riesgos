#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:3000}

echo "=== RBAC Permissions (canonical) ==="
curl -sS -H "x-tenant-id: t1" -H "x-user-id: u1" -H "x-roles: admin" "$BASE_URL/api/rbac/permissions" | sed 's/.*/&/g'

echo "\n=== BC/Power BI Readiness (canónico) ==="
curl -sS -H "x-tenant-id: t1" "$BASE_URL/api/bc_powerbi/readiness" | sed 's/.*/&/g'

echo "\n=== BC/Power BI Model (canónico) ==="
curl -sS "$BASE_URL/api/bc_powerbi/model" | sed 's/.*/&/g'
