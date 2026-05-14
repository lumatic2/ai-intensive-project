"use client";
import { ROOMS_SEED, type RoomScore } from "@/lib/types";
import { scoreToFill } from "@/lib/colors";

type Props = { rooms?: RoomScore[]; userLocation?: string | null };

export function HouseMap({ rooms, userLocation }: Props) {
  const scoreMap = new Map(rooms?.map((r) => [r.room_id, r]) ?? []);
  return (
    <svg
      viewBox="0 0 420 280"
      className="w-full h-auto border rounded-lg bg-white shadow-sm"
    >
      <defs>
        <pattern id="hatch" patternUnits="userSpaceOnUse" width="6" height="6">
          <path d="M0 6 L6 0" stroke="#9ca3af" strokeWidth="1" />
        </pattern>
      </defs>
      {ROOMS_SEED.map((room) => {
        const s = scoreMap.get(room.id);
        const score = s?.final ?? room.base_score;
        const mode = s?.mode ?? "normal";
        return (
          <g key={room.id}>
            <rect
              x={room.bbox.x}
              y={room.bbox.y}
              width={room.bbox.w}
              height={room.bbox.h}
              fill={scoreToFill(score, mode)}
              stroke="#374151"
              strokeWidth={1.5}
            />
            <text
              x={room.bbox.x + room.bbox.w / 2}
              y={room.bbox.y + room.bbox.h / 2 - 4}
              textAnchor="middle"
              className="fill-gray-900 text-sm font-medium"
            >
              {room.name_ko}
            </text>
            <text
              x={room.bbox.x + room.bbox.w / 2}
              y={room.bbox.y + room.bbox.h / 2 + 14}
              textAnchor="middle"
              className="fill-gray-700 text-xs"
            >
              {score}
            </text>
            {userLocation === room.id && (
              <circle
                cx={room.bbox.x + room.bbox.w - 14}
                cy={room.bbox.y + 14}
                r={6}
                fill="#ef4444"
              />
            )}
          </g>
        );
      })}
    </svg>
  );
}
