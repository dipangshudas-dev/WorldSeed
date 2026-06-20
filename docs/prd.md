# Product Requirements Document (PRD): AI Civilization Simulator
**Author:** Startup CTO / AI Systems Architect  
**Status:** Draft / Ready for Review  
**Date:** June 20, 2026  

---

## 1. Vision & Executive Summary
The **AI Civilization Simulator** is a high-fidelity, zero-player sandbox simulation that models the organic development, stagnation, division, and collapse of an autonomous civilization. 

By placing self-interested agents with distinct personality profiles and physical needs into a procedurally generated, resource-constrained environment, the simulation allows complex macro-behaviors (economy, leadership, conflict, family structures, and settlements) to emerge entirely from micro-decisions. The user is strictly an observer, monitoring the rise or fall of these digital societies in real-time through an interactive web-based dashboard.

---

## 2. Goals & Non-Goals

### Goals
*   **True Emergence:** Provide a simulation engine where macro outcomes (e.g., a civil war or an economic market) are never hardcoded, but result naturally from individual agent interactions.
*   **Believable Chaos & Failure:** Validate failure states (mass starvation, tribal fragmentation, total extinction) as equally valuable and exciting outcomes as successful kingdoms.
*   **High-Fidelity Agent Individuality:** Enable users to click on any agent and read a cohesive, unique profile featuring their needs, personality, memory logs, and relationship networks.
*   **Clear Visual Storytelling:** Provide a responsive, premium top-down visualization reminiscent of classic colony simulations, showing agents moving, gathering, building, and fighting.

### Non-Goals
*   **Optimization/Perfect Pathfinding:** Agents should not seek the mathematically optimal way to live. They must make flawed, personality-biased decisions.
*   **Player Intervention/Control:** The user cannot issue commands, build structures, or control agents directly (except for optional, low-impact "Acts of God" triggers in later iterations).
*   **Massive Multiplayer Scale:** We are not building a simulator for 100,000 agents. The system will target 30–100 agents to maintain computational focus on high-fidelity individual behavior in the web browser.
*   **Strategy Game Loops:** There are no win conditions, points, or high scores.

---

## 3. Core Systems Architecture

```
                                  +-----------------------+
                                  |   Web Dashboard UI    |
                                  +-----------+-----------+
                                              | (Real-time State)
                                              v
                                  +-----------------------+
                                  |   Simulation Engine   |
                                  +-----+-----------+-----+
                                        |           |
               +------------------------+           +-------------------------+
               v                                                              v
+-----------------------------+                                 +-----------------------------+
|    Agent Cognitive Loop     |                                 |     World & Environment     |
|  - Needs & Utility Heuristic|                                 |  - Procedural Terrain       |
|  - Episodic Memory DB       |                                 |  - Resource Nodes & Regrowth|
|  - Relationship Graph       |                                 |  - Dynamic Boundaries       |
+-----------------------------+                                 +-----------------------------+
               |                                                              |
               +------------------------+           +-------------------------+
                                        v           v
                                  +-----------------------+
                                  |  Emergent Systems     |
                                  |  - Double-Auction     |
                                  |  - DBScan Clustering  |
                                  |  - Dynamic Paths      |
                                  +-----------------------+
```

### A. Environment System
*   **Procedural Map Generator:** Uses multi-octave Perlin/Simplex noise to create natural-looking landmasses, rivers, forests, mountains, and resource nodes (Food, Wood, Stone, Metal, Gold).
*   **Resource Depletion & Regrowth:** Resources are physical objects. Once harvested, they disappear and regenerate slowly based on local biome variables.

### B. Agent Cognitive Engine
*   **Utility Heuristics:** Agents evaluate actions using a weighted utility score driven by personality coefficients and immediate physiological needs.
*   **Flawed Pathfinding:** Pathfinding incorporates terrain traversal costs and a "laziness" factor based on personality.

### C. Social & Memory Ledger
*   **Episodic Memory Database:** A local store of events containing: `[Timestamp, Location, EventType, Partner, EmotionalCharge]`.
*   **Relationship Matrix:** Tracks bi-directional values of `Trust` [-100 to 100] and `Respect` [-100 to 100] between met agents.

### D. Economic Engine
*   **Double-Auction Marketplace:** A central registry where agents submit buy and sell orders. Trade fails if prices don't align, leading to bartering or theft under extreme need.
*   **Gold Standard:** The emergence of a currency node when trade frequencies exceed a transaction threshold.

### E. Settlement & Infrastructure Engine
*   **Spatial DBScan Clustering:** Runs periodically to identify spatial density clusters of agent-built structures, automatically designating them as camps, villages, or towns.
*   **Influence Map Projection:** Tracks territories owned or claimed by groups based on leadership and group size.

---

## 4. Agent Architecture & Decision Loop

Each agent is defined by a data structure that governs their daily tick-by-tick loop:

```
[Agent Tick Input] 
       |
       v
[Update Needs (Hunger, Energy)] 
       |
       v
[Evaluate Personality & Memory Modifiers]
       |
       v
[Calculate Utility Scores for Goals] 
       |
       v
[Select Highest Utility Action] 
       |
       v
[Execute Action (Gather, Socialize, Rest, Build, Fight)]
```

### Attributes
1.  **Needs:** Hunger (0-100), Energy (0-100), Health (0-100), Comfort (0-100).
2.  **Personality Vector:** Normalized weights summing to 1.0 across traits: `Friendly`, `Aggressive`, `Greedy`, `Curious`, `Loyal`, `Lazy`.
3.  **Skills (0-100):** Farming, Mining, Woodcutting, Construction, Combat, Leadership.
4.  **Family Lineage:** Tracks parents, spouse, and children.

---

## 5. Simulation Rules & Failure Mechanics

To ensure failure states emerge naturally, the simulation enforces these unforgiving rules:

*   **Starvation:** If Hunger reaches 100, Health decays by 5 units per tick. At 0 Health, the agent dies.
*   **Resource Scarcity & Hoarding:** During winter or droughts, resource spawn rates drop by 80%. Greedy agents prioritize building storage chests and lock food away. If their trust in neighbors is low, they refuse to trade, driving others to steal or starve.
*   **Combat Resolution:** If an agent chooses the "Theft" or "Attack" action (high aggressive and greedy weights), combat occurs. The outcome is determined by Combat skill, health, and a slight randomness factor.
*   **Faction Splitting (Civil War / Tribalism):** If a settlement's average relationship score between two sub-groups falls below -50, they form rival factions. One faction will either migrate to form a new camp, or launch attacks to claim the current settlement's resources.

---

## 6. Emergent Behavior Design

The simulator utilizes simple rules to provoke complex societal developments:

| Emergent State | Micro-Condition Trigger | Macro-Phenomenon Observed |
| :--- | :--- | :--- |
| **Tribal Fragmentation** | Low trust between agents in different geographical clusters. | Formation of isolated camps; refusal to trade across settlement boundaries. |
| **Civil War** | High greed and combat skills in secondary leaders coupled with low respect for the primary leader. | Internal combat ticks, destruction of structures, and split of a village into two factions. |
| **Market Crash/Famine** | Inefficient farming skills + high hoarding behavior among resource owners. | Skyrocketing gold prices for food, followed by mass starvation and theft. |
| **Kingdom Emergence** | High leadership/respect scores for a single agent, combined with structural density. | The leader directs group resource pools to build defensive walls, roads, and town halls. |

---

## 7. Dashboard Requirements (User Experience)

The observer interacts with the simulator through a unified web interface:

### A. The Real-time Canvas (Viewport)
*   **Top-down 2D Isometric/Orthographic View:** Stylized representation of terrain, trees, water, and structures.
*   **Agent Visuals:** Moving sprites with small visual state indicators (e.g., carrying wood, sleeping, fighting).
*   **Clash of Clans/Colony Sim Aesthetic:** Soft colors, organic animations, and clear path indicators.

### B. Inspector Panel (Agent & Settlement Profiles)
*   **Agent Profile:** Click an agent to view their radar chart of personalities, need bars, skill levels, lineage, and recent memories (e.g., "Felt betrayed by Arthur when he overcharged for bread").
*   **Settlement Profile:** Shows population, stockpiled resources, average happiness, current leader, and faction breakdowns.

### C. The Chronicle (Historical Ledger)
*   **Narrative Feed:** A scrolling timeline showing automatically constructed historical events.
*   **World Stats Graph:** Real-time line graphs showing population, total gold, and food reserves over time.

---

## 8. Success Metrics

To validate the simulation engine's quality before shipping, it must meet these milestones:

1.  **Zero-Crash Stability:** The simulation must run continuously for 1,000 ticks (approx. 3 hours of real-time simulation) without freezing, crashing, or running out of memory.
2.  **Outcome Diversity Index:** Out of 50 runs with randomized seeds, the engine should yield at least:
    *   15% complete extinctions/mass starvations.
    *   20% stable, cooperative kingdoms.
    *   30% split/rival tribe fragmentations.
    *   35% stagnant, baseline villages.
3.  **Frame Rate Stability:** Maintain a consistent 60 FPS on the dashboard UI by utilizing multi-threading/Web Workers for the cognitive engine.

---

## 9. Future Roadmap

```
Phase 1: Foundations (Engine & Needs)
    ├── Procedural Map Generation
    ├── Basic Needs Loop & Pathfinding
    └── Visual Canvas rendering
Phase 2: Social Systems (Memories & Trust)
    ├── Episodic Memory implementation
    ├── Dynamic Relationship Matrix
    └── Bartering & Double-Auction Market
Phase 3: Macro Evolution (Settlements & Leadership)
    ├── DBSCAN Settlement Clustering
    ├── Factions & Civil War Mechanics
    └── Historical Narrative Chronicler
Phase 4: Expansion (Future Beliefs & Technology)
    ├── Technology Tree discovery (e.g., farming tools)
    └── Emergent Religion & Belief Systems
```
