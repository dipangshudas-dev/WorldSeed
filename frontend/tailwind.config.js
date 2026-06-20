/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        obsidian: '#09090b',
        'zinc-panel': '#18181b',
        charcoal: '#27272a',
        'zinc-white': '#f4f4f5',
        'cool-gray': '#a1a1aa',
        emerald: '#10b981',
        ruby: '#ef4444',
        amber: '#f59e0b',
        sky: '#38bdf8',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Merriweather', 'ui-serif', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
};
