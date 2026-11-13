# Collective decision-making

## Purpose and scope

Provide an optional sub-plugin for modeling decisions made collectively by
organizations and other groups of agents. It can support kingdoms, guilds,
universities, companies and employers, armies, adventuring companies, councils,
and other groups.

The feature is a local simulation capability, not a requirement to use
blockchain technology. DAO and smart-contract concepts are useful design
inspiration for proposals, voting rounds, eligibility rules, execution
conditions, and auditable outcomes. Blockchain, distributed consensus,
cryptocurrency, and networked ledgers are explicitly not assumed; performance
and predictable simulation are priorities.

## Sub-plugin boundary

The sub-plugin should consume and produce framework-level proposals, agent and
organization identifiers, rules, events, and decision records. It should not
own authoritative world state or depend on a particular engine, database, or
network service.

Its interface should allow the host game to:

- enable, disable, or replace collective decision-making;
- select strategies per organization, decision type, or game mode;
- configure parameters and validate them before simulation;
- submit a proposal and query the round's status;
- receive a committed decision, a no-decision result, or a diagnostic;
- use a fallback policy if the sub-plugin is disabled or cannot decide.

Individual agent reasoning and collective governance remain separate tools.
The collective sub-plugin can query relevant agent preferences or decision
recommendations, but it does not replace the general rule reasoner.

## Decision-round model

A decision round may contain:

1. **Proposal:** a proposed action, policy, or resolution with alternatives,
   proposer, supporting evidence, and expected effects.
2. **Constituency:** eligible members or representatives, determined from
   membership, roles, knowledge, location, status, and game rules.
3. **Deliberation:** optional information sharing, argument, negotiation, or
   agent-specific utility evaluation.
4. **Voting or selection:** ballots, delegation, consensus, a leader's choice,
   or another configured procedure.
5. **Tally and validation:** quorum, thresholds, tie handling, veto rights,
   eligibility, and current-state preconditions are checked.
6. **Execution:** a successful result creates a normal framework event or
   proposal for validation and commit; it does not mutate world state outside
   the event lifecycle.

Rounds can be synchronous or span simulation time. A time-spanning round must
not stall other simulation. Its state should be inspectable and serializable
when save/load or replay requires it.

## Configurable strategies

Provide replaceable strategy implementations rather than hard-coding DAO
behavior. Candidate strategies include:

- direct leader or executive decision;
- one-agent-one-vote, optionally weighted by a declared role or stake;
- representative or delegated voting;
- quorum-based council decisions;
- consensus or threshold approval;
- ranked or scored alternatives;
- utility aggregation from member goals or preferences;
- game-specific scripted or authored rules;
- a hybrid process, such as a council vote subject to a leader veto.

These are options to evaluate, not a mandate to implement all strategies.
Configuration should define eligible voters, weights, quorum, thresholds,
abstentions, ties, vetoes, delegation, deadlines, and failure handling. The
system should report which policy produced a result and make alternatives
configurable per organization or decision context.

## Automatic decisions and player intervention

An eligible Player may be offered a chance to participate or intervene when
game rules permit. If the Player declines, is unavailable, lacks prerequisites,
or a deadline expires, the round follows its configured policy. NPCs and groups
may vote or contribute preferences only according to their knowledge, roles,
and goals. Do not fabricate participation or grant agents information they do
not possess.

If a round cannot reach a valid result, its fallback may defer the decision,
escalate it to another authority, choose an eligible leader, invoke the general
automatic decision policy, or select a seeded random valid alternative. Make
this behavior explicit per organization or decision type.

## Smart-contract-inspired rules

Contract-like rules can encode preconditions, deadlines, authorization,
quorum, and consequences. They should be deterministic, inspectable, and
bounded. Treat these as ordinary versioned game rules executed by the
framework; avoid arbitrary untrusted code execution and ensure that contracts
cannot bypass validation or commit state directly.

## Performance and determinism

Performance is a primary requirement. The design should avoid network
round-trips, mining, distributed consensus, and heavyweight general-purpose
contract virtual machines in the simulation hot path. Prefer bounded,
incremental evaluation over repeatedly recomputing every organization's full
membership and preferences.

Benchmark proposal creation, eligibility calculation, tallying, persistence,
and simultaneous active rounds at representative world sizes. Consider
incremental membership indexes, cached eligibility, early tally bounds, and
per-tick work budgets where they preserve correctness. Cache invalidation must
account for membership, role, policy, and world-state changes.

Reproducibility requires stable input ordering, explicit tie-breaking,
versioned strategies, and seeded random choices. Record the proposal,
constituency or reproducible eligibility query, policy configuration, ballots
or aggregate inputs as appropriate, result, fallback, and provenance.

## Security and integrity within the simulation

Even without a blockchain, model relevant game rules: voter eligibility,
duplicate ballots, delegation cycles, expired membership, hidden ballots,
quorum changes, and proposal invalidation. Do not confuse in-world security
with real-world cryptographic guarantees. Games that need secret voting should
define what is hidden from which agents and how that affects saved state and
debug traces.

## Validation and tests

- Test each enabled strategy with valid, invalid, tied, and incomplete rounds.
- Test membership and role changes during a round according to the chosen
  snapshot or live-eligibility policy.
- Test quorum failure, abstention, delegation cycles, vetoes, and deadlines.
- Test Player participation, decline, ineligibility, and timeout without
  blocking unrelated simulation.
- Test that execution always goes through standard event validation and commit.
- Test deterministic results and replay for identical inputs and seeds.
- Benchmark multiple organizations and overlapping rounds; enforce documented
  per-update time and memory budgets.

## Open questions

- Which strategies are required for the initial plugin release?
- Are ballots cast by individual agents, representative seats, or either?
- Is voter eligibility snapshotted when a round opens or recalculated until it
  closes?
- Should deliberation modify agent beliefs, or only aggregate existing
  preferences?
- Which round data must be saved, replayed, or hidden from the Player?
