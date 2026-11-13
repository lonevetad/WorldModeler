# Setting ontologies

## Purpose

Define genre-specific extensions that can be combined with shared world and
domain modules. A genre label is a useful starting point, not a fixed ontology:
individual games may mix genres or reject familiar conventions.

## Candidate settings and extensions

| Setting | Possible concepts extending the shared ontology |
| --- | --- |
| Fantasy | Magic systems, spells, enchanted items, species, curses, supernatural places |
| Social and romantic drama | Courtship, affection, commitments, social reputation, family expectations |
| Thriller and detective noir | Evidence, leads, cases, witnesses, suspects, investigations, corruption |
| Science fiction | Star systems, spacecraft, advanced technologies, artificial life, alien societies |
| Horror | Threats, fear, hauntings, occult practices, contamination, survival pressure |

These are illustrative modules. A game should be able to combine them, define
new ones, or use none of them.

## Extension contract

Each setting module should document:

- the shared concepts it specializes or depends on;
- new entity, event, relationship, and resource types;
- constraints and rules it introduces;
- which mechanics are descriptive versus executable;
- optional and required dependencies;
- compatibility and migration behavior.

Use the common identity, event, time, provenance, and rule interfaces wherever
possible. Genre modules should not introduce duplicate concepts for generic
ideas such as an agent, location, or inventory merely because they use
different display terms.

## Example boundaries

- A romantic relationship can reuse the core relationship model while adding
  setting-specific stages, customs, or commitments.
- An investigation can reuse events, agents, places, and evidence-like items;
  investigative rules may track which agents know which clues.
- A magical weapon remains an item or equipment entity. Magical properties and
  spell interactions come from the fantasy module.
- A sci-fi game can add travel and technology models without requiring magic or
  fantasy species.

## Open design questions

- Should setting definitions be represented as ontology modules, rule packs, or
  both?
- Can a world use multiple competing rule interpretations (for example,
  different cultures' beliefs about magic)?
- How should modules declare conflicts where two settings use the same term
  with different meanings?
