"use client";
import { useEffect, useRef, useState } from "react";

export default function useWebSocket() {
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/stream";

  const startStreaming = () => {
    if (!wsRef.current) {
      wsRef.current = new WebSocket(WS_URL);
      wsRef.current.binaryType = "blob";  // Tell WebSocket to receive binary data

      wsRef.current.onopen = () => {
        console.log("WebSocket connected");
        setIsStreaming(true);
      };

      wsRef.current.onmessage = async (event) => {
        const imgBlob = event.data;  // Receive Blob data
        const img = new Image();

        // Convert Blob to a URL and set it as an image source
        const imgUrl = URL.createObjectURL(imgBlob);
        img.src = imgUrl;

        img.onload = () => {
          const canvas = canvasRef.current;
          if (canvas) {
            const ctx = canvas.getContext("2d");
            ctx?.clearRect(0, 0, canvas.width, canvas.height);
            ctx?.drawImage(img, 0, 0, canvas.width, canvas.height);
          }
          URL.revokeObjectURL(imgUrl);  // Free memory after rendering
        };
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

  return { canvasRef, isStreaming, startStreaming, stopStreaming };
}
