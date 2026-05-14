import { Simulator } from "@/components/Simulator";

export default function Page() {
  return (
    <main className="min-h-screen p-8 max-w-6xl mx-auto">
      <header className="mb-6">
        <h1 className="text-2xl font-bold">생활 맥락 로봇청소기 시뮬레이터</h1>
        <p className="text-sm text-gray-600 mt-1">
          럭키 금성 · LG전자 가전 멘토링 트랙 · AI Intensive Project
        </p>
      </header>
      <Simulator />
    </main>
  );
}
