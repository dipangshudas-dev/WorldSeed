import { useRef, useCallback, useEffect } from 'react';

/**
 * Custom hook to track frames-per-second.
 * Returns a ref whose `.current` always holds the latest FPS value.
 */
export function useFps() {
  const fpsRef = useRef(0);
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(performance.now());

  const tick = useCallback(() => {
    frameCountRef.current++;
    const now = performance.now();
    const delta = now - lastTimeRef.current;

    if (delta >= 1000) {
      fpsRef.current = Math.round((frameCountRef.current * 1000) / delta);
      frameCountRef.current = 0;
      lastTimeRef.current = now;
    }
  }, []);

  return { fpsRef, tick };
}
