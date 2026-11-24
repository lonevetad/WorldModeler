# Rules and reasoning

## Purpose

Define how facts and rules produce inferences, proposed events, and
opportunities. The reasoning system should explain its results and should not
confuse a plausible outcome with a guaranteed one.

## Rule categories

- **Inference rules** derive facts, such as an organization's members being
  affected by an event.
- **Trigger rules** identify conditions under which an event may be proposed.
- **Decision rules** help an agent or group select an action according to its
  goals, knowledge, and constraints.
- **Validation rules** reject invalid state changes or enforce game-specific
  invariants.

Keep these categories distinct. Deriving that a faction is threatened should
not itself force that faction to rebel; the latter is a decision or event rule.

## Contradictions and conundrums

Do not treat every conflict as the same kind of contradiction. The system
should distinguish at least:

- **Inconsistent claims:** facts that cannot all be true under a declared
  constraint, such as two exclusive owners or incompatible location claims.
- **Uncertain or disputed knowledge:** agents hold different beliefs, or the
  world model lacks enough evidence to resolve a proposition.
- **Competing valid actions:** multiple agents or rules propose incompatible
  actions, such as rival claims or mutually exclusive political decisions.
- **Value or policy conflicts:** alternatives are valid but advance different
  goals, which is a narrative decision rather than a logical inconsistency.

Preserve the propositions, sources, confidence, and affected entities involved
in a conflict. Do not silently discard one side or force a single global
truth-resolution policy. A game's constraints determine what must be resolved
before state can commit and what may remain contested.

## Decision arbitration

When a conflict requires a choice, the resolver should produce explicit
alternatives and their consequences. The game may offer the Player a chance to
intervene when the Player has the required access, knowledge, and prerequisites
in the relevant context. Player intervention may be declined or unavailable;
the system must not pause indefinitely waiting for input.

If no eligible Player decision arrives before resolution, the Game Engine
chooses an outcome. A configurable policy may:

1. identify relevant agents with decision-making capability based on context,
   proximity or influence, knowledge, role, and goals;
2. estimate supported outcomes using their preferences or decision rules;
3. invoke an organization's configured governance strategy when the decision
   belongs to a collective;
4. select the most likely supported outcome when confidence is adequate;
5. otherwise choose among valid outcomes using seeded randomness and declared
   weights.

This is a policy, not a universal algorithm. Games may override it. The chosen
outcome, eligible alternatives, participating agents, weights or rationale,
timeout, and random seed (if used) should be recorded for replay and debugging.
Avoid presenting a probability estimate as objective certainty.

Collective governance procedures, including voting rounds and
smart-contract-like execution rules, are provided by the optional
[collective decision-making sub-plugin](15-collective-decision-making.md).
They supplement rule-based inference and individual agent decisions; they
should not be required by the core reasoner.

## Reasoning approach

Evaluate a custom rule engine, a Prolog-alike engine, or a hybrid. A logic
programming tool can be useful for declarative relationships and queries, but
the integration must address data mapping, runtime cost, debugging, deployment,
and deterministic behavior. No particular engine is required by these notes.

A hybrid design could keep the authoritative world state and event lifecycle in
C++, with a well-defined interface to an optional declarative reasoner.
Reasoning results should return identifiers and explanations, not mutate
untracked engine state.

## Evaluation requirements

- Rules declare their inputs, outputs, scope, and version.
- Each inference or proposal records the supporting facts and rule identifier.
- Rules can represent negation or absence only with explicit semantics; missing
  information is not automatically false.
- Conflicting proposals use documented constraints and game-specific
  arbitration; the conflict itself remains inspectable.
- Cycles and repeated firing are detected.
- Cascades have configurable limits, cancellation, and diagnostic traces.
- Random choices use an explicit seed and are separated from deterministic
  inference.
- Evaluation can be replayed against a known state for debugging and tests.

## Consequence versus execution

Reasoning may identify that a kingdom could declare war, that a caravan is
vulnerable, or that a quest opportunity exists. It should not necessarily
commit these outcomes. A separate simulation or agent-decision phase decides
whether a proposal becomes an event, checks preconditions, and commits its state
changes.

## Open questions

- Which reasoning operations must run synchronously in a real-time update?
- Should rules be authored in C++, a declarative language, or both?
- How are rule conflicts resolved when a setting adds a rule that specializes
  a shared rule?
- Which conflict classes are eligible for Player intervention, and which must
  be resolved automatically to preserve simulation progress?
- How should a game author likelihoods, confidence thresholds, and fallback
  randomness without implying false precision?
