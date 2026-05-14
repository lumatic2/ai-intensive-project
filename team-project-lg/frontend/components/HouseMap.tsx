"use client";
import { ROOMS_SEED, type Mode, type RoomId, type RoomScore } from "@/lib/types";
import { scoreToFill } from "@/lib/colors";

type Props = { rooms?: RoomScore[]; userLocation?: RoomId | null };

type Furniture = { d: string; transform?: string };

const FURNITURE: Partial<Record<RoomId, Furniture[]>> = {
  living: [
    { d: "M 0 0 h 80 v 16 h -80 z", transform: "translate(160 130)" },
    { d: "M 0 0 h 80 v 4 h -80 z", transform: "translate(160 124)" },
    { d: "M 0 0 h 14 v 14 h -14 z", transform: "translate(252 122)" },
  ],
  bedroom: [
    { d: "M 0 0 h 70 v 50 h -70 z", transform: "translate(140 210)" },
    { d: "M 0 0 h 28 v 10 h -28 z", transform: "translate(144 214)" },
    { d: "M 0 0 h 28 v 10 h -28 z", transform: "translate(178 214)" },
  ],
  kitchen: [
    { d: "M 0 0 h 80 v 18 h -80 z", transform: "translate(320 22)" },
    { d: "M 0 0 v -8 h 12", transform: "translate(354 22)" },
  ],
  bathroom: [
    {
      d: "M 6 0 h 68 a 6 6 0 0 1 6 6 v 28 a 6 6 0 0 1 -6 6 h -68 a 6 6 0 0 1 -6 -6 v -28 a 6 6 0 0 1 6 -6 z",
      transform: "translate(320 110)",
    },
  ],
  entrance: [
    {
      d: "M 0 0 a 8 4 0 1 0 16 0 a 8 4 0 1 0 -16 0",
      transform: "translate(20 50)",
    },
    {
      d: "M 0 0 a 8 4 0 1 0 16 0 a 8 4 0 1 0 -16 0",
      transform: "translate(40 50)",
    },
  ],
};

// 흰색 사각형으로 벽 끊기 (문 표시)
const DOORS = [
  { x: 92, y: 78, w: 16, h: 4 },
  { x: 298, y: 60, w: 4, h: 16 },
  { x: 184, y: 158, w: 16, h: 4 },
  { x: 358, y: 80, w: 4, h: 16 },
];

function scoreTextColor(score: number, mode: Mode): string {
  if (mode === "excluded") return "#8A8A8A";
  if (score >= 50) return "#1A1A1A";
  return "#4B4B4B";
}

function PersonIcon({ x, y }: { x: number; y: number }) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      <circle cx={0} cy={-8} r={4} fill="#A50034" />
      <path
        d="M -6 0 q 6 -4 12 0 v 10 q -6 4 -12 0 z"
        fill="#A50034"
      />
      <text
        x={0}
        y={22}
        textAnchor="middle"
        style={{
          font: "500 10px var(--font-sans)",
          fill: "#A50034",
        }}
      >
        사용자
      </text>
    </g>
  );
}

export function HouseMap({ rooms, userLocation }: Props) {
  const scoreMap = new Map(rooms?.map((r) => [r.room_id, r]) ?? []);
  return (
    <svg
      viewBox="0 0 420 280"
      className="w-full h-auto border border-line rounded-xl bg-white shadow-sm"
    >
      <defs>
        <pattern
          id="hatch"
          patternUnits="userSpaceOnUse"
          width="6"
          height="6"
        >
          <path d="M0 6 L6 0" stroke="#9ca3af" strokeWidth="1" />
        </pattern>
      </defs>

      {/* Layer 1: 방 채우기 + 외벽 */}
      {ROOMS_SEED.map((room) => {
        const s = scoreMap.get(room.id);
        const score = s?.final ?? room.base_score;
        const mode = (s?.mode ?? "normal") as Mode;
        return (
          <rect
            key={`fill-${room.id}`}
            x={room.bbox.x}
            y={room.bbox.y}
            width={room.bbox.w}
            height={room.bbox.h}
            fill={scoreToFill(score, mode)}
            stroke="#1A1A1A"
            strokeWidth={1.5}
          />
        );
      })}

      {/* Layer 2: 가구 힌트 */}
      {ROOMS_SEED.map((room) =>
        (FURNITURE[room.id] ?? []).map((f, i) => (
          <path
            key={`fur-${room.id}-${i}`}
            d={f.d}
            transform={f.transform}
            stroke="#8A8A8A"
            strokeWidth={1}
            fill="none"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
        )),
      )}

      {/* Layer 3: 외벽 강조 (방 5개 둘러싸는 외곽선) */}
      <rect
        x={0}
        y={0}
        width={420}
        height={280}
        fill="none"
        stroke="#1A1A1A"
        strokeWidth={3}
      />

      {/* Layer 4: 문 (벽 끊기) */}
      {DOORS.map((d, i) => (
        <rect
          key={`door-${i}`}
          x={d.x}
          y={d.y}
          width={d.w}
          height={d.h}
          fill="#FFFFFF"
        />
      ))}

      {/* Layer 5: 라벨 + 점수 */}
      {ROOMS_SEED.map((room) => {
        const s = scoreMap.get(room.id);
        const score = s?.final ?? room.base_score;
        const mode = (s?.mode ?? "normal") as Mode;
        const cx = room.bbox.x + room.bbox.w / 2;
        const cy = room.bbox.y + room.bbox.h / 2;
        const textFill = scoreTextColor(score, mode);
        return (
          <g key={`label-${room.id}`}>
            <text
              x={cx}
              y={cy - 4}
              textAnchor="middle"
              style={{
                font: "500 14px var(--font-sans)",
                fill: textFill,
              }}
            >
              {room.name_ko}
            </text>
            <text
              x={cx}
              y={cy + 14}
              textAnchor="middle"
              style={{
                font: "600 12px var(--font-mono)",
                fill: textFill,
              }}
            >
              {score}
            </text>
          </g>
        );
      })}

      {/* Layer 6: 사용자 아이콘 */}
      {userLocation && (() => {
        const room = ROOMS_SEED.find((r) => r.id === userLocation);
        if (!room) return null;
        const x = room.bbox.x + room.bbox.w - 22;
        const y = room.bbox.y + 22;
        return <PersonIcon x={x} y={y} />;
      })()}
    </svg>
  );
}
