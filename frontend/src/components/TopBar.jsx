/**
 * TopBar — Thin glassmorphic navigation bar.
 *
 * Milestone 0: Displays project name, connection status,
 * and current milestone indicator.
 */
export default function TopBar({ connected }) {
  return (
    <header className="flex items-center justify-between h-10 px-4 bg-zinc-panel/60 border-b border-charcoal backdrop-blur-md select-none">
      {/* Left: Logo & Title */}
      <div className="flex items-center gap-2.5">
        {/* Seed icon */}
        <div className="flex items-center justify-center w-6 h-6 rounded-md bg-emerald/10 border border-emerald/20">
          <svg
            className="w-3.5 h-3.5 text-emerald"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M4.75 2A2.75 2.75 0 002 4.75v10.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25V4.75A2.75 2.75 0 0015.25 2H4.75zM10 6a1 1 0 011 1v2h2a1 1 0 110 2h-2v2a1 1 0 11-2 0v-2H7a1 1 0 110-2h2V7a1 1 0 011-1z" />
          </svg>
        </div>
        <h1 className="text-sm font-semibold tracking-tight text-zinc-white">
          WorldSeed
        </h1>
        <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-charcoal text-cool-gray">
          M1
        </span>
      </div>

      {/* Right: Connection status */}
      <div className="flex items-center gap-2">
        <div
          className={`w-2 h-2 rounded-full transition-colors duration-500 ${
            connected
              ? 'bg-emerald shadow-[0_0_8px_rgba(16,185,129,0.6)]'
              : 'bg-ruby shadow-[0_0_8px_rgba(239,68,68,0.6)] animate-pulse'
          }`}
        />
        <span className="text-xs text-cool-gray">
          {connected ? 'Connected' : 'Reconnecting…'}
        </span>
      </div>
    </header>
  );
}
