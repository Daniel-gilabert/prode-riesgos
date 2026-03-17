import { NextRequest, NextResponse } from 'next/server';

// Canonical RBAC: expose per-tenant permissions inferred from headers.
export async function GET(req: NextRequest) {
  const tenantId = req.headers.get('x-tenant-id') ?? 'default';
  const userId = req.headers.get('x-user-id') ?? 'anonymous';
  const rolesHeader = req.headers.get('x-roles') ?? '';
  const roles = rolesHeader.split(',').map(r => r.trim()).filter(r => r);

  // Simple canonical mapping (could be extended to pull from DB or supabase)
  const canonical = {
    tenant: tenantId,
    user: userId,
    roles,
    permissions: Array.from(new Set(roles.flatMap(r => {
      switch (r) {
        case 'admin':
          return ['rbac.read', 'rbac.write', 'capital_humano.read', 'capital_humano.write', 'worktime.read'];
        case 'reader':
          return ['capital_humano.read', 'worktime.read'];
        default:
          return ['capital_humano.read'];
      }
    })))
  };

  return NextResponse.json(canonical);
}
