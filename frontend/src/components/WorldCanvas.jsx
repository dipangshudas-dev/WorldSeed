import { useRef, useEffect, useState } from 'react';
import { useFps } from '../hooks/useFps';

/**
 * Biome color palette — matches backend BIOME_COLORS and
 * the UI/UX design doc's muted terrain colors.
 */
const BIOME_COLORS = {
  grass:    '#2d5a3f',
  forest:   '#1b4332',
  water:    '#1a3a5c',
  mountain: '#52525b',
};

/**
 * Resource node colors — distinct but harmonious with the terrain palette.
 *   Food:  warm yellow-green
 *   Wood:  rich forest green
 *   Stone: neutral gray
 */
const RESOURCE_COLORS = {
  food:  '#a3be5a',
  wood:  '#2d6a30',
  stone: '#8a8a8a',
};

/**
 * Grid-line color (subtle separation between cells)
 */
const GRID_LINE_COLOR = 'rgba(255, 255, 255, 0.04)';

/**
 * WorldCanvas — renders the 50×50 world grid on an HTML5 Canvas.
 *
 * Milestone 1:
 *  - Fills cells with biome colors (procedural terrain)
 *  - Draws resource node indicators as small circles
 *  - Draws subtle grid lines
 *  - Overlays FPS counter and world size HUD
 *  - Resizes with the window
 */
export default function WorldCanvas({ worldData }) {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const { fpsRef, tick } = useFps();
  const [displayFps, setDisplayFps] = useState(0);

  useEffect(() => {
    if (!worldData) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width: gridW, height: gridH, cells } = worldData;

    // Use biome_colors from server if available, fallback to local
    const colors = worldData.biome_colors || BIOME_COLORS;

    // Resource list from server (Milestone 1)
    const resources = worldData.resources || [];

    function resize() {
      const parent = canvas.parentElement;
      canvas.width = parent.clientWidth;
      canvas.height = parent.clientHeight;
    }

    function render() {
      tick();

      const cw = canvas.width;
      const ch = canvas.height;

      // Calculate cell size to fit the grid within the canvas
      const cellSize = Math.floor(Math.min(cw / gridW, ch / gridH));
      const offsetX = Math.floor((cw - cellSize * gridW) / 2);
      const offsetY = Math.floor((ch - cellSize * gridH) / 2);

      // Clear background
      ctx.fillStyle = '#09090b';
      ctx.fillRect(0, 0, cw, ch);

      // Draw cells
      for (let y = 0; y < gridH; y++) {
        for (let x = 0; x < gridW; x++) {
          const biome = cells[y][x];
          ctx.fillStyle = colors[biome] || BIOME_COLORS[biome] || '#09090b';
          ctx.fillRect(
            offsetX + x * cellSize,
            offsetY + y * cellSize,
            cellSize,
            cellSize,
          );
        }
      }

      // Draw grid lines
      if (cellSize > 4) {
        ctx.strokeStyle = GRID_LINE_COLOR;
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let x = 0; x <= gridW; x++) {
          const px = offsetX + x * cellSize + 0.5;
          ctx.moveTo(px, offsetY);
          ctx.lineTo(px, offsetY + gridH * cellSize);
        }
        for (let y = 0; y <= gridH; y++) {
          const py = offsetY + y * cellSize + 0.5;
          ctx.moveTo(offsetX, py);
          ctx.lineTo(offsetX + gridW * cellSize, py);
        }
        ctx.stroke();
      }

      // Draw resource nodes (Milestone 1)
      if (resources.length > 0) {
        const radius = Math.max(2, cellSize * 0.28);
        for (let i = 0; i < resources.length; i++) {
          const r = resources[i];
          const color = RESOURCE_COLORS[r.type];
          if (!color) continue;

          const cx_r = offsetX + r.x * cellSize + cellSize / 2;
          const cy_r = offsetY + r.y * cellSize + cellSize / 2;

          // Filled circle
          ctx.beginPath();
          ctx.arc(cx_r, cy_r, radius, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();

          // Subtle glow ring for visibility
          ctx.beginPath();
          ctx.arc(cx_r, cy_r, radius + 1, 0, Math.PI * 2);
          ctx.strokeStyle = color + '60';  // 37% opacity
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }

      // Draw subtle outer border around the grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      ctx.strokeRect(
        offsetX + 0.5,
        offsetY + 0.5,
        gridW * cellSize,
        gridH * cellSize,
      );

      // FPS counter update (every frame we tick, but display updates are throttled)
      setDisplayFps(fpsRef.current);

      animFrameRef.current = requestAnimationFrame(render);
    }

    resize();
    window.addEventListener('resize', resize);
    animFrameRef.current = requestAnimationFrame(render);

    return () => {
      window.removeEventListener('resize', resize);
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [worldData, tick, fpsRef]);

  return (
    <div className="relative w-full h-full">
      <canvas
        ref={canvasRef}
        id="world-canvas"
        className="block w-full h-full"
      />

      {/* HUD Overlay */}
      <div className="absolute top-3 left-3 flex gap-3">
        {/* FPS Badge */}
        <div className="flex items-center gap-1.5 rounded-md bg-zinc-panel/80 border border-charcoal px-2.5 py-1 backdrop-blur-sm">
          <div
            className={`w-2 h-2 rounded-full ${
              displayFps >= 50
                ? 'bg-emerald shadow-[0_0_6px_rgba(16,185,129,0.5)]'
                : displayFps >= 30
                ? 'bg-amber shadow-[0_0_6px_rgba(245,158,11,0.5)]'
                : 'bg-ruby shadow-[0_0_6px_rgba(239,68,68,0.5)]'
            }`}
          />
          <span className="text-xs font-medium text-cool-gray font-mono">
            {displayFps} <span className="text-cool-gray/60">FPS</span>
          </span>
        </div>

        {/* World Size Badge */}
        {worldData && (
          <div className="flex items-center gap-1.5 rounded-md bg-zinc-panel/80 border border-charcoal px-2.5 py-1 backdrop-blur-sm">
            <svg
              className="w-3 h-3 text-sky"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              />
            </svg>
            <span className="text-xs font-medium text-cool-gray font-mono">
              {worldData.width}×{worldData.height}
            </span>
          </div>
        )}

        {/* Resource Count Badge (Milestone 1) */}
        {worldData && worldData.resources && (
          <div className="flex items-center gap-1.5 rounded-md bg-zinc-panel/80 border border-charcoal px-2.5 py-1 backdrop-blur-sm">
            <div className="w-2 h-2 rounded-full bg-amber/80" />
            <span className="text-xs font-medium text-cool-gray font-mono">
              {worldData.resources.length} <span className="text-cool-gray/60">resources</span>
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
