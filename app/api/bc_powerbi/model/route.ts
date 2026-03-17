import { NextRequest, NextResponse } from 'next/server';

// Canonical data model for BC/Power BI connectors
export async function GET(req: NextRequest) {
  const model = {
    capital_humano: {
      id: 'integer',
      score: 'float',
      tenant: 'string',
      created_at: 'timestamp'
    },
    worktime: {
      id: 'integer',
      hours: 'float',
      date: 'date',
      tenant: 'string'
    }
  };
  return NextResponse.json({ models: model, version: '1.0.0' });
}
