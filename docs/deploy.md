# Deploy guide (MVP)

- Prerequisites: Node.js, PNPM/Yarn, Next.js project dependencies installed.
- Start the app: run the dev server and navigate to admin and capital_humano dashboards.
- Verify patch 6 endpoints: /api/rbac/permissions and /api/bc_powerbi/readiness
- Verify patch 8 model endpoint: /api/bc_powerbi/model
- Basic sanity checks for multi-tenant headers in requests.

Next steps: implement additional tests, CI, and push a PR with patches 6-9.
