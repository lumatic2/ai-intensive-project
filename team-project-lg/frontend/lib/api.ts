import type { ScenarioMeta, SimulateResponse } from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export async function fetchScenarios(): Promise<ScenarioMeta[]> {
  const r = await fetch(`${BASE}/api/scenarios`, { cache: "no-store" });
  if (!r.ok) throw new Error(`scenarios ${r.status}`);
  return r.json();
}

export async function simulate(scenarioId: string): Promise<SimulateResponse> {
  const r = await fetch(`${BASE}/api/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario_id: scenarioId }),
  });
  if (!r.ok) throw new Error(`simulate ${r.status}`);
  return r.json();
}
