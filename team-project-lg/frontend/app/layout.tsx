import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "생활 맥락 로봇청소기 시뮬레이터",
  description: "AI가 청소 우선순위를 결정하고 그 이유를 설명합니다.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body className="font-sans antialiased bg-gray-50 text-gray-900">
        {children}
      </body>
    </html>
  );
}
