# World simulation and time

## Purpose

Define when rules run, how events become state changes, and how world state
remains coherent across real-time or discrete simulation.

## Suggested simulation phases

1. Accept authored, player-driven, scheduled, or generated event proposals.
2. Validate proposals against current state and game rules.
3. Commit accepted events and their direct state changes.
4. Evaluate relevant inference and trigger rules.
5. Queue follow-on proposals, respecting cascade limits and priorities.
6. Detect inconsistent claims, disputed knowledge, and incompatible event
   proposals; classify conflicts and determine which require a decision.
7. Offer eligible Player interventions with their prerequisites and resolution
   deadlines, without blocking unrelated simulation.
8. When intervention is unavailable, declined, or times out, select an outcome
   using the game's automatic decision policy. Relevant NPCs and groups may
   inform the choice through their knowledge, goals, and decision rules; an
   organization's configured collective-governance strategy may run a bounded
   proposal or voting round. Use seeded randomness among valid choices when no
   sufficiently supported preference or governance result exists.
9. Validate and commit the selected outcome, recording alternatives,
   provenance, timeout, and decision rationale.
10. Let autonomous agents or groups make other decisions from their own
    knowledge and goals, then publish state changes and explanations to
    adapters and game systems.

The exact ordering is a design choice. It must be documented because ordering
can affect outcomes.

## Time model

Support events at a point in time and over an interval. Decide whether the core
uses simulation ticks, a logical clock, real-time durations, or a combination.
Engine frame time should not become the sole source of world time; adapters
should translate engine updates into the framework's time model.

Scheduled events, deadlines, decay, travel, and production should define their
time semantics and behavior when simulation is paused or accelerated.

Decision deadlines may be hidden from the Player, but remain explicit in
simulation state. A timeout policy should define its clock source, pause and
acceleration behavior, and whether expiry is processed at a tick boundary or
immediately. A hidden deadline is a presentation choice; it must not make
resolution timing nondeterministic or untestable.

Governance rounds also need explicit opening, voting, closing, and execution
times. They must not block unrelated world simulation while awaiting votes.
Where a round reaches its deadline without satisfying quorum or another
configured condition, apply the organization's declared fallback policy.

## Consistency and determinism

Define whether state transitions are atomic, how simultaneous proposals are
ordered, and how conflicting writes are handled. For reproducible simulation,
make event ordering, random seeds, and rule versions visible in traces.

Keep unresolved contradictions and decision conflicts represented explicitly
until a resolution event commits a choice. Automatic resolution should never
rewrite history as though the Player or a particular NPC made the decision if
the recorded actor was the simulation policy.

The framework should be able to pause, step, inspect, and where feasible replay
simulation. Rollback or branching history may be useful but should be treated as
an explicit capability with storage and performance costs.

## Runtime budgets

Large worlds and consequence cascades need limits on work per update. Consider
prioritization, incremental evaluation, deferred work, and cancellation. A
budget should result in visible pending work or a diagnostic, not silently
dropped consequences.
