"use client";
import { useEffect, useRef, useState } from "react";

export default function useWebSocket() {
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/stream";

  const startStreaming = () => {
    if (!wsRef.current) {
      wsRef.current = new WebSocket(WS_URL);

      wsRef.current.onmessage = (event) => {
        const imgSrc = `data:image/jpeg;base64,${event.data}`;
        setImageSrc(imgSrc);
      };

      wsRef.current.onerror = () => {
        console.error("WebSocket Error");
      };

      wsRef.current.onclose = () => {
        console.log("WebSocket closed");
        setIsStreaming(false);
      };

      setIsStreaming(true);
    }
  };

  const stopStreaming = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
      setImageSrc(null);
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

  return { imageSrc, isStreaming, startStreaming, stopStreaming };
}
