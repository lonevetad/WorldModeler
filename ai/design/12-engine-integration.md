# Engine integration

## Purpose

Make the framework usable from Unreal Engine 5 and Godot while keeping
engine-specific APIs outside the reusable world-model core.

## Adapter responsibilities

Each adapter should translate engine lifecycle and data into framework
operations:

- create and configure a world-model instance;
- load ontology modules and game data;
- submit player, scripted, and engine-originated events;
- advance or pause simulation according to an explicit time policy;
- expose relevant state changes, opportunities, and diagnostics to the game;
- release resources safely during shutdown, reload, or scene changes.

Adapters should not independently reimplement ontology semantics or consequence
rules.

## Unreal Engine 5

Investigate a plugin module that wraps the framework with Unreal-facing types
and lifecycle hooks. Keep engine reflection, object ownership, serialization,
and build rules in the adapter. Verify supported compiler and C++ standard
settings against the specific UE5 versions targeted by the project.

Reference: [Unreal Engine](https://www.unrealengine.com/unreal-engine-5).

## Godot

Investigate a GDExtension-based adapter, or another officially supported native
extension route appropriate to the target Godot versions. Keep Godot node and
resource APIs in the adapter and define how native framework objects are
created, referenced, and freed.

Reference: [Godot Engine](https://godotengine.org/).

## Shared integration requirements

- Publish a supported engine-version and platform matrix.
- Avoid passing engine-owned pointers into long-lived framework state unless
  lifetime rules are explicit.
- Define thread affinity and safe event delivery between engine and framework.
- Translate errors and diagnostics into each engine's logging and inspection
  conventions.
- Test clean startup/shutdown, reload, world teardown, and repeated
  initialization.
- Keep standalone use possible without either engine installed.

## Open questions

- Which engine versions and platforms are required first?
- Should adapters be separate repositories/packages or live alongside the
  core?
- Which engine-facing concepts should be reflected as native engine resources
  or types?
