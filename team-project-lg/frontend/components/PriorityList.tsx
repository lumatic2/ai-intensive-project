import type { RoomScore } from "@/lib/types";
import { MODE_BADGE } from "@/lib/colors";
import { ROOMS_SEED } from "@/lib/types";

const ROOM_NAMES = Object.fromEntries(ROOMS_SEED.map((r) => [r.id, r.name_ko]));

export function PriorityList({ rooms }: { rooms: RoomScore[] }) {
  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm">
      <h2 className="font-semibold mb-3">청소 우선순위</h2>
      <ul className="space-y-2">
        {rooms.map((r) => {
          const badge = MODE_BADGE[r.mode];
          return (
            <li
              key={r.room_id}
              className={`flex items-start justify-between p-2 rounded
                ${r.mode === "excluded" ? "opacity-60" : ""}`}
            >
              <div>
                <span
                  className={`font-medium ${r.mode === "excluded" ? "line-through" : ""}`}
                >
                  {ROOM_NAMES[r.room_id] ?? r.room_id}
                </span>
                <span className="ml-2 text-sm text-gray-500">{r.final}점</span>
                {r.exclusion_reason && r.mode === "excluded" && (
                  <div className="text-xs text-gray-500 mt-0.5">{r.exclusion_reason}</div>
                )}
              </div>
              <span className={`px-2 py-0.5 rounded text-xs whitespace-nowrap ${badge.cls}`}>
                {badge.label}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
