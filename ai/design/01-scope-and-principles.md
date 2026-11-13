# Scope and design principles

## Purpose

WorldModeler is intended to be a reusable framework for modeling highly dynamic
role-playing game worlds. Its central design challenge is to represent a shared
world vocabulary while allowing individual games to define their own settings,
rules, and content.

The framework should support a world that changes in response to authored
story, player actions, autonomous characters and groups, and stochastic or
procedural events. A change can produce further consequences, but those
consequences must remain inspectable and bounded.

## Goals

- Define reusable abstract concepts for entities, places, resources,
  relationships, organizations, events, and world state.
- Permit multiple game-specific ontologies to extend the shared concepts
  without making genre-specific assumptions mandatory for every game.
- Represent event causes, effects, and derived opportunities in a graph.
- Evaluate rules and derive consequences through a custom reasoning layer, with
  Prolog-alike tooling as an option rather than a required runtime dependency.
- Expose a C++ framework usable from standalone applications and adapters for
  Unreal Engine 5 and Godot.
- Keep the public framework compatible with C++20, C++23, and C++26 builds.

## Design principles

1. **Separate vocabulary from world content.** An ontology defines concepts and
   valid relationships; a particular game world contains instances of them.
2. **Separate occurrences from things.** A character, weapon, or mine is an
   entity. Its creation, discovery, transfer, destruction, or arrival is an
   event that changes world state.
3. **Make causality explicit.** Derived changes should identify the event,
   rule, and inputs that produced them.
4. **Preserve player choice.** The system may expose plausible roles and
   opportunities; it should not silently choose the player's response.
5. **Support uncertainty.** A game may distinguish facts, beliefs, rumors,
   hypotheses, and unknowns rather than treating every stored proposition as
   objectively true.
6. **Keep the core engine-independent.** Engine objects, rendering, UI, and
   engine-specific lifecycle APIs belong in adapters.
7. **Make simulation bounded and observable.** Cascades need limits, diagnostics,
   and reproducible traces so pathological rule sets can be found and explained.

## Boundaries to establish

- Is the framework responsible for simulation mechanics, or does it only
  provide world modeling and consequence evaluation?
- Which systems are required in the core library, and which are optional
  modules (for example, a Prolog bridge, database backend, or ontology editor)?
- How much real-time behavior is needed: frame-by-frame updates, discrete
  simulation steps, or both?
- Are multiplayer synchronization and authoritative simulation in scope?
- What level of compatibility is required for saved worlds across framework
  versions?

These decisions should be settled before committing to a storage format,
reasoning engine, or engine-specific public API.
