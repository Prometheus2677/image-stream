"use client";
import { useEffect, useRef, useState } from "react";

export default function StreamImage() {
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/stream";

  const startStreaming = () => {
    if (!wsRef.current) {
      wsRef.current = new WebSocket(WS_URL);

      wsRef.current.onopen = () => {
        console.log("WebSocket connected");
        setIsStreaming(true);
      };

      wsRef.current.onmessage = (event) => {
        const img = new Image();
        img.src = `data:image/jpeg;base64,${event.data}`;

        img.onload = () => {
          const canvas = canvasRef.current;
          if (canvas) {
            const ctx = canvas.getContext("2d");
            if (ctx) {
              ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear previous frame
              ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            }
          }
        };
      };

      wsRef.current.onerror = (error) => {
        console.error("WebSocket Error:", error);
      };

      wsRef.current.onclose = () => {
        console.log("WebSocket closed");
        setIsStreaming(false);
      };
    }
  };

  const stopStreaming = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
      setIsStreaming(false);
    }
  };

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-2xl font-bold mb-4">Real-Time Streaming at 24 FPS</h1>

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

      <canvas
        ref={canvasRef}
        className="rounded shadow-lg mt-4"
        width={640}
        height={480}
      />
    </div>
  );
}
