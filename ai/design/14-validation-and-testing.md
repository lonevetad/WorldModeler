# Validation and testing

## Purpose

Validate that ontology compositions are coherent, consequence evaluation is
correct and bounded, and the framework behaves consistently across language
standards and engine adapters.

## Ontology and rule validation

- Check identifiers, references, dependencies, type compatibility, and
  constraints when modules are composed.
- Validate rule inputs and outputs before runtime.
- Detect duplicate or incompatible definitions and provide actionable errors.
- Detect subtype cycles and incompatible constraints inherited through
  multiple ontology paths.
- Test that inferred facts and proposed events include provenance.
- Test unknown, conflicting, stale, and retracted facts explicitly.

## Scenario tests

Create small, deterministic scenarios for representative chains:

- a unique weapon appears and competing groups respond differently;
- a resource deposit is discovered and leads to claims, contracts, transport,
  and possible theft;
- an assassination changes some relations while leaving responsibility
  unknown until evidence is found;
- resource extraction creates economic activity and environmental or political
  opposition;
- a political marriage changes treaties or claims only when the game rules say
  it does;
- a new threat produces different reactions based on agents' knowledge and
  goals.
- a resource and equipment instance can both participate in trade through the
  shared goods model without being forced into the same subtype;
- a decision conflict is offered to an eligible Player, while an ineligible,
  declined, or expired decision is resolved automatically;
- automatic resolution favors relevant NPC/group preferences when supported,
  and uses a reproducible seeded fallback otherwise.
- collective decision strategies handle quorum, ties, delegation, eligibility,
  timeouts, and fallback policies as configured;
- collective decisions produce standard framework events and cannot bypass
  world-state validation;
- disabling the collective-decision sub-plugin leaves the configured general
  decision fallback functional.

Assert both expected outcomes and non-outcomes. For example, discovery of a
deposit should not unconditionally create every possible trade route.
Also assert that no player response is fabricated when a timeout occurs and
that unresolved conflicting claims remain visible until a resolution event is
committed.

## Framework and compatibility tests

- Build and run core tests in C++20, C++23, and C++26 modes for each claimed
  compiler/toolchain.
- Test standalone builds without Unreal Engine or Godot dependencies.
- Test serialization round trips, schema migrations, and invalid input errors.
- Test deterministic replay using recorded inputs and random seeds.
- Test graph cycles, duplicate events, cancellation, and cascade limits.
- Test decision eligibility, hidden timeout expiry, fallback policy, and
  deterministic replay of automatic choices.
- Benchmark collective decision rounds across representative member counts and
  concurrent organizations; verify configured runtime and memory budgets.
- Add adapter tests for initialization, event submission, state notification,
  teardown, and repeated lifecycle transitions.

## Performance and diagnostics

Benchmark representative world sizes, rule counts, and cascade shapes. Measure
time and memory for ontology loading, event commits, queries, and persistence.
Record enough diagnostics to explain slow or unexpectedly large consequence
chains without requiring a debugger.

Performance thresholds should be selected from actual target-game constraints
and recorded with the tested hardware and build configuration.
