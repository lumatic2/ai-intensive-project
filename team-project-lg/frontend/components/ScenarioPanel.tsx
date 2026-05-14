"use client";
import type { ScenarioMeta } from "@/lib/types";

type Props = {
  scenarios: ScenarioMeta[];
  selectedId: string | null;
  loading: boolean;
  onSelect: (id: string) => void;
};

export function ScenarioPanel({ scenarios, selectedId, loading, onSelect }: Props) {
  if (scenarios.length === 0) {
    return <div className="text-sm text-gray-500">시나리오를 불러오는 중…</div>;
  }
  return (
    <div className="grid grid-cols-2 gap-2">
      {scenarios.map((s) => {
        const active = s.id === selectedId;
        return (
          <button
            key={s.id}
            onClick={() => onSelect(s.id)}
            disabled={loading}
            className={`p-3 rounded border text-left transition
              ${active
                ? "bg-blue-600 text-white border-blue-700"
                : "bg-white hover:bg-gray-50 border-gray-300"}
              ${loading ? "opacity-50 cursor-wait" : ""}`}
          >
            <div className="font-medium text-sm">{s.name_ko}</div>
            <div className={`text-xs mt-1 ${active ? "text-blue-100" : "text-gray-500"}`}>
              {s.current_time} · {s.description}
            </div>
          </button>
        );
      })}
    </div>
  );
}
