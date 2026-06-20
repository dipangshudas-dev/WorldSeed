# UI/UX Design Document: AI Civilization Simulator

This document establishes the user interface guidelines, user experience goals, and visual design systems for the **AI Civilization Simulator**. It combines the immersive aesthetic of premium indie simulation games with the minimal usability of modern SaaS dashboards (like Vercel and Linear).

---

## 1. Design Vision

The user experience should feel like looking through an advanced scientific lens at a pocket universe. When a user opens the dashboard, they should feel like an observer in a digital observatory: quiet, intrigued, and deeply curious. The visual style is dark-mode first, prioritizing soft glowing indicators, crisp typography, and fluid, slow-paced motion to draw the observer into the tiny lives of the agents.

---

## 2. Design Principles

*   **Observe, Don't Control:** The UI has zero input triggers for steering the agents. Interaction is purely informational.
*   **Story First:** Technical state variables (like integers) should be translated into descriptive text and contextual iconography.
*   **Data without Overwhelm:** Clean dashboard layouts with progressive disclosure. Details are hidden unless the user inspects an entity.
*   **Every Agent Matters:** Agents are drawn with subtle visual distinctions, and their profiles read like micro-biographies rather than raw data matrices.

---

## 3. Information Architecture

The application is structured as a single-page app containing three primary viewport perspectives, accessible via a global top navigation bar:

```
[Top Navigation Bar]
       ├── Observation Dashboard (Default View)
       │     ├── Left: Live Chronicle Event Feed
       │     ├── Center: HTML5 World View Canvas
       │     └── Right: Inspector Context Panel (Agent/Settlement details)
       │
       ├── History & Chronicle (Full-Screen Ledger)
       │     └── Filterable & searchable event database
       │
       └── Population Analytics (Graph Hub)
             └── Real-time statistical line graphs
```

---

## 4. Dashboard Layout

The workspace is organized in a three-column desktop-first configuration to maximize spatial efficiency on standard monitors:

*   **Top Navigation:** A thin, translucent glassmorphic bar containing the simulation control hub (Play, Pause, Speed multiplier indicators), current Year/Tick display, and view toggles.
*   **Left Column (Event Feed Panel - 20% Width):** A scrolling list of real-time micro-events (e.g., *"Arthur gathered wood"*, *"John built a shelter"*). Clicking an event snaps the camera to the target.
*   **Center Column (World View Canvas - 55% Width):** The main gameplay viewport. It is borderless and houses the HTML5 simulation canvas.
*   **Right Column (Inspector Panel - 25% Width):** A context-sensitive sidebar. When nothing is selected, it displays overall world parameters. When an agent or settlement is clicked, it transitions to show detailed profile pages.

---

## 5. World View Design

The world is rendered in a clean, flat 2D tile style utilizing a modern, muted color palette.

*   **Camera Interactions:** Standard mouse-drag to pan; scroll wheel to zoom (from 0.5x macroscopic map overview to 4x pixel-level detail).
*   **Terrain Visualization:** Muted background blocks. Grasslands are dark gray-green, forests are accented with small green triangles, and water is a deep navy blue block.
*   **Resource Node Indicators:** Circular nodes that shrink in size as resources deplete, displaying a small radial reload circle when regenerating.
*   **Agent Representation:** Tiny circular avatars containing the agent's initials or a minimal icon reflecting their current activity (e.g., a pickaxe symbol when mining).
*   **Structure Representation:** Simple wireframe outlines indicating homes, farms, and storage, which color-fill as their physical completion increases.

---

## 6. Agent Profile Experience

Clicking an agent opens the Agent Inspector, designed to build empathy with the digital subject:

*   **Header Section:** Displays the agent's name, age, current state (e.g., *"Searching for food"*), and a dynamic status badge (e.g., *Healthy*, *Hungry*, *Starving*).
*   **Needs Grid:** Progress bars using a red-to-green gradient mapping Hunger, Energy, and Health metrics.
*   **Personality Radar Chart:** A minimal pentagon chart showing the agent's personality traits (e.g., Greedy, Aggressive, Loyal).
*   **Memory Timeline:** A vertical feed listing the agent's episodic memories:
    > *"Felt threatened by John when he was seen holding a weapon nearby." (20 Ticks Ago)*
*   **Relationship List:** Circular cards representing met agents, displaying a bi-directional scale bar for Trust and Respect.

---

## 7. Settlement Profile Experience

Clicking on a settlement boundary opens the Settlement Inspector:

*   **Demographic Profile:** Displays the settlement name, designated tier (e.g., *Camp*, *Village*), active population count, and average community happiness.
*   **Resource Stockpile Bar:** A horizontal breakdown showing total collective wood, stone, and food stored within the settlement.
*   **Leadership Indicator:** Shows the avatar of the agent currently recognized as the leader based on community trust scores, alongside a list of active community goals.

---

## 8. History & Chronicle Experience

The **History View** functions as a searchable world ledger:

*   **Chronicle Timeline:** An auto-scrolling log of events written like an ancient diary.
*   **Filter Matrix:** Toggle buttons to filter events by categories: *Diplomatic*, *Conflict*, *Domestic*, *Disaster*.
*   **Search Bar:** Users can type keywords (e.g., "Oakvale") to view the entire history of a specific place or agent.

---

## 9. Analytics Experience

A data-dense analytics panel for macro-observers:

*   **Demographic Charts:** Real-time line graphs showing active population decay over ticks.
*   **Resource Supply Lines:** Area charts indicating stockpiled resources vs. consumer demand.
*   **Gini Coefficient (Inequality Index):** A line graph monitoring wealth/resource concentration among agents.

---

## 10. Visual Design System

The system follows a strict, dark-mode first design framework:

### A. Color Palette
*   **Background (Primary):** `#09090b` (Deep Obsidian)
*   **Panels (Secondary):** `#18181b` (Muted Zinc)
*   **Borders & Accents:** `#27272a` (Charcoal)
*   **Text (Primary):** `#f4f4f5` (Zinc White)
*   **Text (Secondary):** `#a1a1aa` (Cool Gray)
*   **Indicator - Success:** `#10b981` (Emerald Green)
*   **Indicator - Danger:** `#ef4444` (Ruby Red)

### B. Typography
*   **Interface Typeface:** *Inter* or *Geist Sans* (Clean, high-readability sans-serif).
*   **History/Chronicle Typeface:** *Merriweather* (Elegant serif to give narrative logs a literary feel).

---

## 11. Motion & Animation System

Animations are micro-interactions designed to add weight without slowing down the UI:

*   **Agent Movement:** Smooth linear interpolations between grid tiles instead of sudden grid snaps.
*   **Panel Slide-In:** Panels slide from the right edge with an easing curve (`cubic-bezier(0.16, 1, 0.3, 1)`) over 200ms.
*   **Event Notifications:** Toast notifications slide up from the bottom-left corner and fade out after 3 seconds.

---

## 12. Responsive Design Strategy

*   **Desktop View (Target System):** 3-column layout. High canvas visibility, constant sidebar inspector state.
*   **Laptop View:** Inspector sidebar slides out as an overlay rather than pushing canvas width.
*   **Tablet View:** Landscape-only support. Sidebar collapse is default; event panel becomes a drawer button.

---

## 13. Empty States & Edge Cases

*   **First Simulation Launch:** Dashboard displays a central setup card: *"Seed generated. Awaiting simulation initialization."* Clicking "Spawn" triggers a slow fade-in of the canvas grid.
*   **Total Extinction:** The viewport dims by 40%. A centralized banner is displayed: *"The civilization has collapsed. 0 agents remain active."* A final chronicle summary is generated.
*   **Paused State:** A thin, glowing yellow line borders the main viewport, with a clear "Paused" badge floating in the center-top section of the canvas.

---

## 14. MVP UI Scope

The Version 1 UI includes only the essential elements:

1.  **Main Screen:** Flat 2D Canvas grid, Left-side scrolling chronicle log, and Right-side Agent Inspector showing Needs and personality stats.
2.  **Basic Controls:** Play/Pause button, Tick Speed selector (1x, 2x, 4x).
3.  **Basic Modals:** Sim Setup panel (Grid Size, Agent Count sliders) and Simulation Extinction overlay.

---

## 15. Future UI Roadmap

*   **Family Trees:** An interactive node tree in the agent profile visualising generations of lineages.
*   **Technology Hub:** An overlay graph illustrating unlocked tech modifiers.
*   **Factions Map Mode:** A canvas map filter displaying glowing border lines around rival territories.
