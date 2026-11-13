# Persistence, interchange, and tools

## Purpose

Define how ontology definitions, game content, world snapshots, event history,
and derived graph data are authored, exchanged, persisted, and migrated.

## Separate data categories

At minimum, distinguish:

- ontology and rule definitions;
- static game content and initial world setup;
- mutable current world state;
- event history and causal provenance;
- caches or rebuildable derived inferences.

This separation determines what must be versioned, backed up, migrated, or
recomputed.

## Storage and interchange

Evaluate relational databases, document or graph-oriented stores, and
file-based serialization according to query patterns, consistency needs, world
size, offline use, and engine packaging constraints. Do not select SQL or
NoSQL solely by category; prototype representative queries and workloads.

Serialization should include schema and ontology versions, stable identifiers,
and validation. It should define how unknown optional fields and unsupported
module versions are handled. Event history can support explanations and replay,
but may grow substantially and need retention or compaction policies.

## Authoring

Protégé and OWL/RDF may support ontology design, inspection, and validation.
Evaluate how authored data maps to runtime concepts and how rules, temporal
facts, and game-specific constraints are represented. A custom authoring format
may be appropriate, but should have a documented schema and validation tools.

## Build and developer tooling

Makefile targets or a portable build system can automate generation,
validation, tests, and packaging. Tooling should make it easy to validate an
ontology composition before launching an engine and to inspect why a fact or
consequence was produced.

## Migrations and reproducibility

Version data formats and rule sets. Migrations should be explicit, testable,
and preferably preserve original saves. For reproducibility, record the
framework version, ontology composition, rule versions, and random seed used
for a simulation or saved snapshot.

## Open questions

- Is an event log authoritative, or is a snapshot authoritative with a
  best-effort history?
- Which data needs to be editable by non-programmers?
- Are network synchronization or user-authored mods in scope?
