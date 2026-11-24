# Resources, goods, and equipment

## Purpose

Model resources consistently across gathering, production, storage, trade,
consumption, crafting, and conflict. The model should support both discrete
objects and quantities.

## Resource categories

The abstract model should allow game-specific subtypes, including:

- food, drink, and brewing ingredients;
- raw and industrial materials, including timber and ore;
- catalysts, components, and crafting inputs;
- finished goods and trade goods;
- precious objects and valuables;
- currencies, tokens, and other kinds of money;
- renewable or finite deposits, such as forests and crystal mines;
- abstract capacities where useful, such as labor, influence, or energy.

Categories should be extensible and need not form a single exclusive
classification. An item might be both a valuable object and a trade good.

## Goods, trade, and type composition

`Goods` is a useful shared economic concept for things that can participate in
trade. Resources and equipment can both specialize or conform to `Goods`, so
market rules can work across both domains. This is a type relationship, not a
claim that every resource or piece of equipment is currently for sale.

Represent tradeability as a capability or a rule evaluated in context. A
specific instance may be unavailable because it is protected, reserved,
illegal, damaged, inaccessible, or not owned by a party able to sell it. The
trade transaction itself should record parties, items or quantities, price or
barter terms, time, and resulting transfers.

The concept graph should support multiple classifications without duplicating
instances. For example, a sword can be equipment and goods; a crystal can be a
resource and goods; a healing potion may be both a consumable resource and an
item. Use subtypes for true specialization and explicit capabilities for
cross-cutting behaviors.

## Quantity and lifecycle

Represent a resource as a discrete entity, a stackable quantity, a capacity, a
stock, a flow, or a spatial deposit as appropriate. Define units, precision,
and limits explicitly. Track important transitions such as extraction,
production, transformation, transfer, consumption, spoilage, and depletion.

For a resource-bearing place, separate the place from its deposit and from
inventory extracted from it. This makes ownership, depletion, and later
discovery expressible without conflating them.

## Ownership and economy

Ownership or custody should be modeled with explicit relations and time
intervals; possession does not necessarily mean legal ownership. A transfer
may reference a contract, payment, theft, gift, tax, or other event.

Economy modules may model prices, scarcity, supply, demand, routes, production
chains, contracts, and commercial organizations. The abstract core should not
assume one universal currency or price model.

## Weapons and equipment

Weapons are a specialized kind of item or equipment, not a separate identity
system. Equipment may have slots, requirements, condition, durability,
ownership, and effects. A setting module can add weapon classes or supernatural
properties. Rules that govern damage or combat belong to the relevant gameplay
module, not the general resource vocabulary.

Equipment may need a substantial ontology of its own. Keep the shared equipment
module composable, with optional extensions for slots and loadouts,
compatibility and prerequisites, condition and maintenance, use and
activation, effects and modifiers, and setting-specific equipment. Equipment
instances should remain interoperable with inventory, ownership, and market
modules through shared identifiers and declared capabilities.

## Example

A crystal deposit may be discovered by an event, claimed by a kingdom, and
worked by a guild. Extraction changes the deposit's remaining quantity and
creates inventory lots with provenance. Those lots may be sold under a
contract, moved along a route, guarded by a military group, stolen, or used in
crafting.

## Open questions

- Which quantities require exact accounting, and which can be abstracted?
- Are economic simulation and crafting required core modules or optional
  systems?
- How should simultaneous claims and disputed ownership be represented?
