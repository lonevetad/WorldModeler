# Events and consequence graphs

## Purpose

Represent world changes as explicit events and connect them to their causes,
effects, and derived consequences. A single event may start multiple chains of
consequences, and separate chains may converge on the same later event.

## Event model

An event should identify its type, occurrence time or interval, participants,
location, triggering source, preconditions, state changes, and provenance.
Useful source categories include authored story, player action, autonomous
agent or group action, scheduled simulation, and random or procedural
generation.

The event is distinct from any entity it creates, changes, or discovers. For
example, discovering a mine is an event; the mine and its deposit are entities
in the resulting world state.

Events can be proposed, validated, committed, canceled, or superseded. The
simulation should define which of these stages are needed and which are
observable to players.

## Graph structure

Use typed edges rather than one generic "leads to" relation. Candidate edges
include:

- **causes:** an event or condition contributes to another event;
- **enables:** a condition makes an event possible but does not guarantee it;
- **prevents:** a condition blocks an event;
- **requires:** an event depends on a precondition;
- **derives:** a rule inferred a fact or opportunity from its inputs;
- **responds-to:** an agent or organization reacts to an event.

Store the rule, supporting facts, confidence, and time for derived edges.
Consequences can be conditional or uncertain; the graph must not imply that
every plausible consequence is inevitable.

## Example chains

### Magical weapon in a royal vault

The appearance or discovery of a magical weapon can change what kingdoms know
and believe. Rules may propose alliances, theft attempts, or campaigns to
control it. These events may in turn create openings for a guard, assassin,
mercenary, knight, diplomat, or other player role. Which actions occur depends
on the world state and agent decisions.

### Crystal mine discovered

A discovery can reveal a resource deposit and trigger competing claims. If
mining or trade rules apply, they may propose a commercial route, contracts,
caravans, guards, or smuggling activity. The discovery itself does not
automatically create all these outcomes.

### Noble assassinated

An assassination may end or alter relationships, invalidate obligations under
game-specific rules, create uncertainty about responsibility, and provoke
reactions. Allies and beneficiaries may respond differently; facts about the
assassin should remain unknown unless established by evidence.

### Forest harvesting

A kingdom's decision to harvest a forest may result in extraction events and
contracts, and may incentivize a woodcutters' guild. Nature-aligned groups may
protest or rebel. Player opportunities can include supporting a faction,
protecting or exploiting the forest, disrupting supply, or taking another
action. Harmful in-world choices are modeled as fictional outcomes, not
prescribed player actions.

### Marriage and political union

A marriage can create personal and political relations. A game-specific rule
may merge claims or kingdoms, affect treaties, and prompt competition among
nobles or organizations. A fair, intrigue, or attempted murder is a possible
follow-on only when supported by the setting's rules and agents' goals.

### New villain appears

The emergence of a demon, lich, tyrant, monster, or alien can become known at
different times by different agents. Some may ally with it; others may offer
quests to oppose it. These reactions should emerge from goals, knowledge, and
rules rather than a fixed universal response.

## Lifecycle and graph maintenance

The system needs policies for duplicate event detection, cycles, stale
consequences, and changed assumptions. If a premise is retracted or an event is
rewound, derived facts should be identifiable for invalidation or recomputation.
The graph may be cyclic when agents react to one another; evaluation therefore
needs cycle detection and a bounded work policy.
