"use client";
import { useEffect, useState } from "react";
import { fetchScenarios, simulate } from "@/lib/api";
import type { ScenarioMeta, SimulateResponse } from "@/lib/types";
import { HouseMap } from "./HouseMap";
import { ScenarioPanel } from "./ScenarioPanel";
import { PriorityList } from "./PriorityList";
import { ExplanationCard } from "./ExplanationCard";

type State = {
  scenarios: ScenarioMeta[];
  selectedId: string | null;
  response: SimulateResponse | null;
  loading: boolean;
  error: string | null;
};

export function Simulator() {
  const [state, setState] = useState<State>({
    scenarios: [],
    selectedId: null,
    response: null,
    loading: false,
    error: null,
  });

  useEffect(() => {
    fetchScenarios()
      .then((scenarios) => setState((s) => ({ ...s, scenarios })))
      .catch((e) =>
        setState((s) => ({ ...s, error: `시나리오 로딩 실패: ${String(e)}` }))
      );
  }, []);

  const handleSelect = async (id: string) => {
    setState((s) => ({ ...s, selectedId: id, loading: true, error: null }));
    try {
      const response = await simulate(id);
      setState((s) => ({ ...s, response, loading: false }));
    } catch (e) {
      setState((s) => ({
        ...s,
        loading: false,
        error: `시뮬레이션 실패: ${String(e)}`,
      }));
    }
  };

  const selected = state.scenarios.find((s) => s.id === state.selectedId);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <div className="lg:col-span-3">
        <HouseMap
          rooms={state.response?.rooms}
          userLocation={selected?.user_location}
        />
      </div>
      <div className="lg:col-span-2 space-y-4">
        <ScenarioPanel
          scenarios={state.scenarios}
          selectedId={state.selectedId}
          loading={state.loading}
          onSelect={handleSelect}
        />
        {state.error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
            <div>{state.error}</div>
            {state.selectedId && (
              <button
                onClick={() => state.selectedId && handleSelect(state.selectedId)}
                className="mt-1 underline"
              >
                재시도
              </button>
            )}
          </div>
        )}
        {state.loading && (
          <div className="text-sm text-gray-500">시뮬레이션 중…</div>
        )}
        {state.response && !state.loading && (
          <>
            <PriorityList rooms={state.response.rooms} />
            <ExplanationCard response={state.response} />
          </>
        )}
      </div>
    </div>
  );
}
