export type Mode = "normal" | "quiet" | "delayed" | "excluded";

export type RoomId =
  | "entrance"
  | "living"
  | "kitchen"
  | "bedroom"
  | "bathroom";

export const ROOM_IDS: readonly RoomId[] = [
  "entrance",
  "living",
  "kitchen",
  "bedroom",
  "bathroom",
] as const;

export const ROOM_LABEL: Record<RoomId, string> = {
  entrance: "현관",
  living: "거실",
  kitchen: "주방",
  bedroom: "침실",
  bathroom: "욕실",
};

export type ScoreContribution = {
  source: string;
  label_ko: string;
  delta: number;
};

export type RoomScore = {
  room_id: RoomId;
  base: number;
  breakdown: ScoreContribution[];
  final: number;
  mode: Mode;
  exclusion_reason: string | null;
};

export type SimulateResponse = {
  scenario_id: string;
  context_summary: string;
  rooms: RoomScore[];
  explanation: string;
  fallback: boolean;
  duration_ms: number;
};

export type ScenarioMeta = {
  id: string;
  name_ko: string;
  description: string;
  current_time: string;
  sleep_time: string;
  user_location: RoomId | null;
  active_events: string[];
};

export type EventMeta = {
  id: string;
  name_ko: string;
  effects: { room_id: RoomId | "*"; delta: number }[];
};

export type CustomRequest = {
  current_time: string;
  sleep_time: string;
  user_location: RoomId | null;
  active_events: string[];
  gap_rooms?: string[];
};

export type RoomBbox = {
  id: RoomId;
  name_ko: string;
  base_score: number;
  bbox: { x: number; y: number; w: number; h: number };
};

// 백엔드 미연결 fallback. backend/app/data/rooms.json과 동기 유지 필요.
export const ROOMS_SEED: RoomBbox[] = [
  { id: "entrance", name_ko: "현관", base_score: 30, bbox: { x: 0, y: 0, w: 100, h: 80 } },
  { id: "living", name_ko: "거실", base_score: 25, bbox: { x: 100, y: 0, w: 200, h: 160 } },
  { id: "kitchen", name_ko: "주방", base_score: 20, bbox: { x: 300, y: 0, w: 120, h: 80 } },
  { id: "bedroom", name_ko: "침실", base_score: 15, bbox: { x: 100, y: 160, w: 200, h: 120 } },
  { id: "bathroom", name_ko: "욕실", base_score: 10, bbox: { x: 300, y: 80, w: 120, h: 80 } },
];

export const HHMM = /^([01]\d|2[0-3]):[0-5]\d$/;
