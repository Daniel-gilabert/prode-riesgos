import { NextRequest, NextResponse } from 'next/server';
import { performance } from 'perf_hooks';

export async function GET(req: NextRequest) {
  // Read tenant if provided for multi-tenant readiness checks
  const tenant = req.headers.get('x-tenant-id') ?? 'default';
  const started = performance.now();

  // In a real scenario, we'd ping dependencies, connected data models, etc.
  // Here we provide a lightweight readiness contract.
  const payload = {
    status: 'ok',
    tenant,
    timestamp: new Date().toISOString(),
    latencyMs: Math.round((performance.now() - started))
  };

  return NextResponse.json(payload);
}
