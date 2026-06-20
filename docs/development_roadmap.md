# Development Roadmap: AI Civilization Simulator

This document establishes the execution plan, sprint milestones, testing criteria, and release checklists for the **AI Civilization Simulator**. It is tailored for a solo developer working part-time, utilizing AI-assisted development to build a high-fidelity MVP while keeping code structures simple and performance footprint small.

---

## 1. Development Philosophy

*   **MVP-First (Minimal Viable Product):** Never build a complex feature if a simpler one can prove the core simulation loop. Verify that agents can move and survive before coding trade networks or buildings.
*   **Visible Progress Loops:** Every sprint must culminate in a visible, interactive state in the terminal or on the canvas. If you cannot see it, you cannot verify if the simulation is emerging naturally.
*   **Fail Early, Fail Safe:** Societal collapse, starvation, and extinction are valid simulation states. We do not code safety nets for the agents; we let the algorithms run their course.
*   **Clean Separation of Concerns:** Keep the Python backend simulation code completely independent of the React rendering interface. This allows fast headless runs and keeps code complexity manageable.

---

## 2. Project Milestones

```
M0: Project Setup ─────► M1: World Sim ─────► M2: Agent Survival
                                                    │
M5: Dashboard UI ◄───── M4: Building Sys ◄── M3: Gathering
      │
M6: Profiles ──────────► M7: Social Matrix ──► M8: Settlements ──► M9: Public Release
```

*   **Milestone 0: Project Setup:** Establish Git repositories, set up FastAPI skeleton, React-Vite project, and SQLite link.
*   **Milestone 1: World Simulation:** Procedural grid generation (Grass, Forest, Mountains) rendering statically on the canvas.
*   **Milestone 2: Agent Survival:** Spawn agents, run need decay (Hunger, Health), and resolve basic ticking loops.
*   **Milestone 3: Resource Gathering:** Place Food/Wood nodes on the grid; agents walk to nodes and harvest resources.
*   **Milestone 4: Building System:** Agents construct simple shelters on grid tiles when tired.
*   **Milestone 5: Dashboard UI:** Connect WebSockets to stream state changes to the HTML5 Canvas client.
*   **Milestone 6: Agent Profiles:** Clicking an agent opens a detailed inspector sidebar displaying needs and personality.
*   **Milestone 7: Relationships:** Introduce the memory log and trust scores between interacting agents.
*   **Milestone 8: Settlement Formation:** Run spatial density clustering to group shelters into dynamically named villages.
*   **Milestone 9: Public Demo Release:** Build package, clean GitHub repository, write README, and host demo.

---

## 3. Sprint Plan

| Week | Sprint Target | Core Deliverables |
| :--- | :--- | :--- |
| **Week 1** | Setup & Grid | Backend FastAPI config, 2D Grid structure, basic static Canvas rendering. |
| **Week 2** | Needs & Movement | Tick loop runner, Agent entity models, pathfinding, hunger decay logic. |
| **Week 3** | Resource Nodes | Wood/Food spawn locations, harvesting actions, inventory updates. |
| **Week 4** | Shelter Building | Tiredness state triggers, tile placement logic, building integrity decay. |
| **Week 5** | Live WebSockets | Stream coordinate updates from server to client canvas at 2 ticks/sec. |
| **Week 6** | Inspector Sidebar | UI panels showing agent statistics, needs graphs, and rolling memories. |
| **Week 7** | Social Matrix | Inter-agent collision encounters, relationship trust modifier logic. |
| **Week 8** | DBSCAN Villages | Automatic settlement boundary calculation, visual town marker icons. |
| **Week 9** | Testing & Polish | Run long-term simulation loop tests, fix performance lag, write documentation. |

---

## 4. Task Breakdown & Success Criteria

### Milestone 0: Project Setup
*   **Tasks:** Initialize git repo; install Python dependency packages; configure Vite+Tailwind boilerplate.
*   **Dependencies:** None.
*   **Success Criteria:** Running `npm run dev` and `uvicorn main:app` simultaneously starts both systems without errors.

### Milestone 1: World Grid
*   **Tasks:** Code the 2D grid matrix class; implement Perlin Noise terrain generator; write canvas grid-cell renderer.
*   **Dependencies:** Milestone 0.
*   **Success Criteria:** Browser displays a procedural terrain map containing mountains, rivers, and grasslands.

### Milestone 2: Agent Survival
*   **Tasks:** Code agent class structures; create the tick manager loop; execute hunger/health decay updates.
*   **Dependencies:** Milestone 1.
*   **Success Criteria:** Agents render as static dots on the map; console logs confirm they die when Hunger reaches 100.

### Milestone 3: Resource Gathering
*   **Tasks:** Spawn resource nodes; implement A* navigation heuristics; code the "Harvest" utility action.
*   **Dependencies:** Milestone 2.
*   **Success Criteria:** Starving agents calculate path to closest food, walk there, and decrement node resource counts.

### Milestone 4: Building System
*   **Tasks:** Create shelter entity; code wood-consumption requirements; design shelter building coordinates.
*   **Dependencies:** Milestone 3.
*   **Success Criteria:** Agents gather wood, find a vacant grass tile, consume wood, and spawn a shelter block.

---

## 5. MVP Scope Definition

### Included in V1 (MVP)
*   **Procedural 2D Grid Map** (Grass, Forest, Mountain, Water).
*   **Agent Needs Loop** (Hunger, Energy, Health).
*   **Basic Actions** (Harvest, Sleep, Move, Build Shelter).
*   **Dynamic Relationships** (Trust and Respect vectors).
*   **Episodic Memory Buffer** (Capped at 20 logs).
*   **Settlement Detector** (Basic DBSCAN clustering of houses).
*   **Dashboard** (Canvas viewport, agent inspector sidebar, narrative history scroll).

### Excluded from V1 (Post-MVP)
*   **Factions & Kingdoms** (Diplomatic lines, physical borders).
*   **Combat & Wars** (Weapon crafting, sieges, military leadership).
*   **Market Currency & Economics** (Gold tracking, structured shops).
*   **Religion & Technology Trees** (Temples, researched tools).
*   **Linage Trees** (Births, marriages, family nodes).

---

## 6. Testing Roadmap

1.  **Headless Execution Testing:** Run the Python simulation engine without launching the browser client. Run for 2,000 ticks to verify no data deadlocks occur.
2.  **Boundary Stress Testing:** Spawn 150 agents on a tiny 30x30 map grid to force high-density pathfinding requests, verifying server tick rates remain above 2 ticks/sec.
3.  **Extinction Verification:** Set food regeneration rates to zero. Verify that all agents starve to death, the engine catches the state, and writes the extinction chronicle event correctly.

---

## 7. GitHub & Repository Strategy

*   **Structure:** Monorepo architecture containing two root folders: `/backend` and `/frontend`.
*   **Branching Model:**
    *   `main`: Always represents stable, runnable releases.
    *   `development`: Target branch for merging weekly sprints.
    *   `feature/*`: Temporary branches for individual milestones (e.g., `feature/agent-needs`).
*   **Commit Pattern:** Use clean prefixes: `feat:`, `fix:`, `docs:`, `perf:` (e.g., `feat: implement A-star pathfinding`).

---

## 8. Demo Roadmap

*   **Internal Demo 1 (Week 3):** Verification of needs and paths. Green circles (agents) walk toward brown squares (food) on a flat colored map.
*   **Internal Demo 2 (Week 5):** WebSocket sync. Canvas updates smoothly over WebSockets when simulation speed scales up to 4x.
*   **Internal Demo 3 (Week 8):** Full interface check. Clicking an agent updates the inspector, displaying relationships and memories correctly.
*   **Public MVP Demo (Week 9):** Clean GitHub repository containing an animated README GIF demonstrating a 10-minute simulation evolution.

---

## 9. Risk Management

| Identified Risk | Impact | Mitigation Plan |
| :--- | :--- | :--- |
| **Performance Lag on WebSockets** | High | Reduce state payload sizes by only sending coordinate deltas instead of full grid arrays. |
| **Farming Deadlock (Extinction)** | Critical | Ensure baseline wild food sources regenerate constantly near forests, even if agents fail to build farms. |
| **Scope Creep (Adding Trade/Combat)** | Medium | Block all trade or conflict code development until Milestone 8 is fully completed and stable. |

---

## 10. Timeline Estimate

*   **Best Case:** 6 Weeks (Highly focused execution, zero pathfinding blockages).
*   **Expected Case:** 9 Weeks (Accommodating part-time learning, debugging, and dashboard adjustments).
*   **Worst Case:** 13 Weeks (Encountering performance issues, requiring major algorithm rewrites).

---

## 11. Launch Checklist

- [ ] Backend runs without error on `uvicorn main:app`.
- [ ] Frontend builds cleanly with `npm run build`.
- [ ] Readme file includes set-up commands, system schema diagram, and screenshots.
- [ ] SQLite database file initializes automatically on clean start.
- [ ] WebSocket reconnect logic is stable when server restarts.
- [ ] Demo GIF added to GitHub header showing civilization progress.

---

## 12. Post-MVP Roadmap (Phases 2-9)

```
Phase 2: Lineage (Births, Marriages)
    ├── Phase 3: Trade (Double-Auction Market)
    │     ├── Phase 4: Factions (Rival Clans, Flags)
    │     │     ├── Phase 5: Leadership (Laws, Taxes)
    │     │     │     ├── Phase 6: Conflict (Combat, Walls)
    │     │     │     │     ├── Phase 7: Kingdoms (Empires, Alliances)
    │     │     │     │     │     ├── Phase 8: Religion (Altars, Beliefs)
    │     │     │     │     │     └── Phase 9: Technology Evolution (Agriculture)
```
