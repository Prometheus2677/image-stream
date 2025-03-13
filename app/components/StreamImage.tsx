"use client";
import useWebSocket from "../hooks/useWebSocket";

export default function StreamImage() {
  const { imageSrc, isStreaming, startStreaming, stopStreaming } = useWebSocket();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-2xl font-bold mb-4">Streaming Images at 24 FPS</h1>

      {!isStreaming ? (
        <button
          onClick={startStreaming}
          className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded shadow-lg"
        >
          Start Streaming
        </button>
      ) : (
        <button
          onClick={stopStreaming}
          className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded shadow-lg"
        >
          Stop Streaming
        </button>
      )}

      {imageSrc && <img src={imageSrc} alt="Streamed Frame" className="rounded shadow-lg w-[640px] mt-4" />}
    </div>
  );
}
