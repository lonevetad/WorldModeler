# Design analysis index

These notes decompose the initial project brief into focused design topics. They
are proposals and questions for analysis, not a claim that the architecture has
already been implemented or finalized.

## Topics

1. [Scope and design principles](01-scope-and-principles.md) — goals, constraints,
   terminology, and boundaries.
2. [Ontology architecture](02-ontology-architecture.md) — the shared abstract
   ontology, layered type hierarchy, game-specific extensions, and composition.
3. [Core world ontology](03-core-world-ontology.md) — reusable concepts for
   places, living entities, events, states, and relationships.
4. [Setting ontologies](04-setting-ontologies.md) — genre-specific vocabularies
   and extension examples.
5. [Resources, goods, and equipment](05-resources-goods-equipment.md) — resource
   types, inventories, production, trade, weapons, and equipment.
6. [Social, economic, and military organizations](06-organizations-and-relations.md)
   — relationships, groups, memberships, contracts, guilds, and armed forces.
7. [Events and consequence graphs](07-events-and-consequence-graphs.md) — event
   modeling, causal dependencies, cascades, and graph lifecycle.
8. [Rules and reasoning](08-rules-and-reasoning.md) — rule evaluation,
   Prolog-alike reasoning, contradictory state, decision arbitration, and
   bounded execution.
9. [Collective decision-making](15-collective-decision-making.md) — optional
   governance sub-plugin with DAO- and smart-contract-inspired voting and
   configurable alternatives.
10. [Player agency and quests](09-player-agency-and-quests.md) — roles,
   opportunities, quest generation, and player intervention in world
   conundrums.
11. [World simulation and time](10-world-simulation-and-time.md) — simulation
    phases, temporal behavior, determinism, and runtime boundaries.
12. [C++ framework architecture](11-cpp-framework-architecture.md) — modular
    C++ design and C++20/23/26 compatibility.
13. [Engine integration](12-engine-integration.md) — Unreal Engine 5 and Godot
    plugin adapters.
14. [Persistence, interchange, and tools](13-persistence-interchange-tools.md)
    — storage, serialization, ontology authoring, and build tooling.
15. [Validation and testing](14-validation-and-testing.md) — correctness,
    compatibility, performance, and integration validation.

## Suggested reading order

Start with scope and ontology architecture, then read the core and setting
ontology notes. Events, reasoning, and player agency describe the dynamic
simulation. The framework, engine, persistence, and validation notes cover the
implementation-facing constraints.
