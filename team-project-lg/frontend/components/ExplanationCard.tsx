"use client";
import { useState } from "react";
import type { SimulateResponse } from "@/lib/types";
import { ROOMS_SEED } from "@/lib/types";

const ROOM_NAMES = Object.fromEntries(ROOMS_SEED.map((r) => [r.id, r.name_ko]));

export function ExplanationCard({ response }: { response: SimulateResponse }) {
  const [showWhy, setShowWhy] = useState(false);
  const [showExcluded, setShowExcluded] = useState(false);
  const top = response.rooms[0];
  const excluded = response.rooms.filter((r) => r.mode === "excluded");

  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold">AI 설명</h2>
        {response.fallback && (
          <span className="text-xs px-2 py-0.5 bg-yellow-100 text-yellow-800 rounded">
            폴백 모드
          </span>
        )}
      </div>
      <p className="text-sm leading-relaxed text-gray-800 whitespace-pre-wrap">
        {response.explanation || "(설명 없음)"}
      </p>

      {top && (
        <div>
          <button
            onClick={() => setShowWhy(!showWhy)}
            className="text-xs text-blue-700 underline"
          >
            {showWhy ? "닫기" : `왜 ${ROOM_NAMES[top.room_id] ?? top.room_id}부터?`}
          </button>
          {showWhy && (
            <table className="w-full text-xs mt-2">
              <tbody>
                {top.breakdown.map((c, i) => (
                  <tr key={i} className="border-t">
                    <td className="py-1">{c.label_ko}</td>
                    <td className="py-1 text-right font-mono">
                      {c.delta >= 0 ? `+${c.delta}` : c.delta}
                    </td>
                  </tr>
                ))}
                <tr className="border-t font-semibold">
                  <td className="py-1">최종</td>
                  <td className="py-1 text-right font-mono">{top.final}</td>
                </tr>
              </tbody>
            </table>
          )}
        </div>
      )}

      {excluded.length > 0 && (
        <div>
          <button
            onClick={() => setShowExcluded(!showExcluded)}
            className="text-xs text-gray-600 underline"
          >
            {showExcluded ? "닫기" : `왜 ${excluded.length}개 공간을 제외?`}
          </button>
          {showExcluded && (
            <ul className="text-xs text-gray-700 space-y-1 mt-2">
              {excluded.map((r) => (
                <li key={r.room_id}>
                  <strong>{ROOM_NAMES[r.room_id] ?? r.room_id}</strong>:{" "}
                  {r.exclusion_reason ?? "사유 없음"}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="text-[10px] text-gray-400 pt-1 border-t">
        응답 시간 {response.duration_ms}ms · {response.context_summary}
      </div>
    </div>
  );
}
