import { useWorldSocket } from './hooks/useWorldSocket';
import TopBar from './components/TopBar';
import WorldCanvas from './components/WorldCanvas';

/**
 * App root — Milestone 0
 *
 * Layout: TopBar (thin nav) + full-bleed WorldCanvas.
 * No sidebar, no chronicle feed — those come in later milestones.
 */
export default function App() {
  const { worldData, connected } = useWorldSocket();

  return (
    <div className="flex flex-col w-full h-screen bg-obsidian">
      <TopBar connected={connected} />

      <main className="flex-1 min-h-0 relative">
        {worldData ? (
          <WorldCanvas worldData={worldData} />
        ) : (
          <div className="flex items-center justify-center w-full h-full">
            <div className="flex flex-col items-center gap-4">
              {/* Loading spinner */}
              <div className="w-8 h-8 border-2 border-charcoal border-t-emerald rounded-full animate-spin" />
              <p className="text-sm text-cool-gray">
                {connected
                  ? 'Loading world…'
                  : 'Connecting to simulation engine…'}
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
