import type { Mode } from "./types";

export function scoreToFill(score: number, mode: Mode): string {
  if (mode === "excluded") return "url(#hatch)";
  if (score <= 0) return "#e5e7eb";
  const clamped = Math.min(80, Math.max(0, score));
  const hue = 60 - (clamped / 80) * 60;          // 60(yellow) → 0(red)
  const lightness = 88 - (clamped / 80) * 28;    // 88% → 60%
  return `hsl(${hue}, 85%, ${lightness}%)`;
}

export const MODE_BADGE: Record<Mode, { label: string; cls: string }> = {
  normal:   { label: "일반",    cls: "bg-blue-100 text-blue-800" },
  quiet:    { label: "저소음",  cls: "bg-purple-100 text-purple-800" },
  delayed:  { label: "지연",    cls: "bg-orange-100 text-orange-800" },
  excluded: { label: "제외",    cls: "bg-gray-200 text-gray-600" },
};
