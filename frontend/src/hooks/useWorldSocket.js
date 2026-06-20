import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for WebSocket connection to the backend.
 *
 * Milestone 0: Connects on mount, receives world_init payload,
 * and stores it in state. Handles reconnection with backoff.
 */
export function useWorldSocket() {
  const [worldData, setWorldData] = useState(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    // Determine WS URL based on current location
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = 'ws://127.0.0.1:8000/ws';

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('[WorldSeed] WebSocket connected');
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'world_init') {
          setWorldData(message.payload);
        }
        // Future: handle 'tick_update', 'event', etc.
      } catch (err) {
        console.error('[WorldSeed] Failed to parse WS message:', err);
      }
    };

    ws.onclose = () => {
      console.log('[WorldSeed] WebSocket disconnected, reconnecting in 2s...');
      setConnected(false);
      reconnectTimeoutRef.current = setTimeout(connect, 2000);
    };

    ws.onerror = (err) => {
      console.error('[WorldSeed] WebSocket error:', err);
      ws.close();
    };
  }, []);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  return { worldData, connected };
}
