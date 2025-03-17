"use client";
import useWebSocket from "../hooks/useWebSocket";

export default function StreamImage() {
  const { canvasRef, isStreaming, startStreaming, stopStreaming } = useWebSocket();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-2xl font-bold mb-4">Real-Time Streaming at 24 FPS</h1>

      {!isStreaming ? (
        <button onClick={startStreaming} className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded shadow-lg cursor-pointer">
          Start Streaming
        </button>
      ) : (
        <button onClick={stopStreaming} className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded shadow-lg cursor-pointer">
          Stop Streaming
        </button>
      )}

      <canvas ref={canvasRef} className="rounded shadow-lg mt-4" width={640} height={480} />
    </div>
  );
}
