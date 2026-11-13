# Core world ontology

## Purpose

Specify the smallest stable vocabulary that other modules and game settings can
reuse. The core should be broad enough to model different RPG genres without
requiring every game to implement every domain.

## Core concepts

- **Entity:** an identifiable thing in the modeled world. It can be an agent,
  object, place, organization, or another domain-specific type.
- **Agent:** an entity capable of actions or decisions. It may be a player
  character, non-player character, creature, collective, or automated actor.
- **Place:** a location or spatial region, optionally nested in other places.
- **Event:** an occurrence at a time or interval that may change state.
- **State:** a set of propositions about the world at a point or interval in
  time, with provenance and optional confidence.
- **Relationship:** a typed, possibly directed and time-bounded association
  between entities.
- **Resource:** a thing or measurable quantity that can be held, consumed,
  produced, transformed, or transferred.
- **Rule:** a condition and one or more proposed inferences, effects, or
  opportunities.
- **Objective:** a desired or forbidden condition that may be used by a quest,
  faction, or agent.

These concepts need not all be concrete entity types. Some are abstract
categories, while others are capabilities or relations that multiple types can
support. For example, an entity may be ownable and tradeable without those
capabilities defining its identity or forcing it into a single subtype chain.
See [ontology architecture](02-ontology-architecture.md) for the type graph and
composition rules.

## Identity and lifecycle

Instances need stable identifiers separate from mutable names and descriptions.
The model should distinguish creation, discovery, activation, destruction,
depletion, retirement, and disappearance; these transitions are not equivalent.
Aliases and localization should map to an identifier rather than become its
identity.

An event that creates or discovers an entity is not the entity itself. For
example, a `MineDiscovered` event can establish that a mine entity exists, set
its location and known resource deposits, and record who discovered it.

## Properties and relationships

Properties should declare their value type, multiplicity, valid subject types,
and temporal behavior. Relationships should declare direction, cardinality,
valid endpoint types, and whether they can be reciprocal or overlapping.
Avoid representing every domain relation as an untyped string pair.

For facts that can change, record validity time (when true in the world) and
recorded time (when learned or stored), where the use case needs both. This
supports delayed discovery, rumors, and historical queries.

## Knowledge and provenance

Distinguish at least:

- objectively modeled world state;
- an agent's beliefs or goals;
- information known by a group;
- an unverified claim or rumor;
- an inference produced by a rule.

Each derived fact should be traceable to its source facts, event, and rule.
Games may choose simpler subsets, but should not be forced to treat a
character's knowledge as omniscient world truth.

## Extension policy

Domain and setting ontologies may add capabilities, subtypes, properties, and
constraints. Keep type definitions separate from instance state: a type
describes what instances mean and permit, while an instance represents a
particular character, object, or place in a world. The core remains neutral
about genre-specific entities and mechanics. For example, the core may define
an `Agent` and `Resource`, while a fantasy module defines a spellcaster and a
sci-fi module defines a synthetic intelligence.
