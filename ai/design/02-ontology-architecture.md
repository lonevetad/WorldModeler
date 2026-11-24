# Ontology architecture

## Purpose

Use multiple composable ontologies rather than one monolithic vocabulary. The
architecture should let a game reuse common world concepts and opt into only
the setting-specific extensions it needs.

## Proposed layers

### 1. Abstract world ontology

Defines concepts shared across games: entity, agent, place, event, state,
resource, item, relationship, organization, rule, objective, and time. It
describes the shape and semantics of concepts, not a particular story world.

### 2. Domain modules

Add reusable, cross-setting domains such as inventory and resources, social
relations, economy, conflict, quests, and knowledge. Modules depend on the
abstract ontology and declare their own dependencies.

### 3. Setting ontologies

Define concepts that are specific to a genre or world, such as magic, starships,
hauntings, courtly customs, or investigative evidence. They extend or specialize
shared concepts rather than redefining them incompatibly.

### 4. Game ontology and content

A game combines selected modules and setting ontologies, then supplies its own
classes, instances, rules, names, and constraints. A concrete world is data
conforming to that composition.

## Type hierarchy and ontology roles

The composition is a graph of ontology modules and concepts, not merely a
four-level taxonomy. It should provide type relationships analogous in purpose
to object-oriented interfaces, abstract classes, and concrete classes, while
remaining a domain model rather than inheriting programming-language runtime
semantics.

- **Capability/interface concepts** specify properties or relations an entity
  must support, such as being tradable, ownable, usable, or perishable. A
  concept can satisfy several capabilities without forcing them into one
  inheritance chain.
- **Abstract concepts** define shared meaning and constraints but are not
  instantiated directly, such as `Goods`, `Equipment`, or `LivingEntity`.
- **Concrete concepts** define instantiable domain kinds, such as a particular
  sword, potion, ration, or vehicle type. Their instances still have stable
  identities and mutable state distinct from the type definition.

Use subtype relations for genuine "is-a" specialization and capability
relations for cross-cutting behavior. Multiple inheritance or equivalent
composition may be necessary: an item can be both equipment and a trade good,
and a resource can also be a trade good. Model this as a directed acyclic
subtype graph where possible, with explicit capabilities for relationships
that should not imply subtype membership. Composition must detect cycles and
incompatible inherited constraints.

For example, `Goods` can be an abstract market-domain concept; `Resource` and
`Equipment` can specialize it where the game defines them as goods, while
specific resources and equipment types specialize those concepts further.
Tradeability should be a declared capability or market rule, not an assumption
that every instance is always available for sale. A kingdom's forest resource,
for example, may be protected, unclaimed, or otherwise unavailable to trade.

Equipment warrants a dedicated ontology module, potentially split into modules
for slots, compatibility, condition, use, effects, and domain-specific
equipment. The shared equipment ontology should define reusable semantics;
games select or extend only the complexity they need.

Keep **ontology module dependencies**, **concept subtype/capability relations**,
and **instance relationships** as separate graphs. A game module depends on
another module; a concept specializes another concept; and a world instance
participates in relations such as ownership or membership. Conflating these
graphs makes composition, validation, and runtime queries ambiguous.

## Composition requirements

- Every ontology/module has an identifier, version, declared dependencies, and
  compatibility information.
- Concepts have stable identifiers independent of display names and
  localization.
- Extensions declare whether they add a capability, subtype, property,
  constraint, or rule. They must not silently change the meaning of a shared
  concept.
- Composition detects missing dependencies, duplicate identifiers, incompatible
  property definitions, subtype cycles, incompatible inherited constraints,
  and unsatisfied constraints before simulation starts.
- Optional modules can be omitted without leaving invalid references in the
  core model.
- Migrations describe how persisted data changes when an ontology version
  changes.

## Representation questions

Evaluate whether ontology definitions should be authored in a standard
knowledge-representation format, a project-specific schema, or both. Protégé
and OWL/RDF may be useful for authoring and validation, but their suitability
for runtime performance, game-specific temporal state, and C++ integration must
be measured rather than assumed.

Keep the runtime model and authoring format decoupled enough that a future
format change does not require rewriting game content.

## Example composition

A game might combine the abstract world ontology with resource, organization,
and quest modules, then add a fantasy ontology for magic and nonhuman species.
A detective game could reuse the same abstract concepts and organization
module, while using evidence, investigation, and noir setting extensions
instead.
