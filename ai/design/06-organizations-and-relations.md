# Social, economic, and military organizations

## Purpose

Model both relationships between entities and collective entities that act in
the world. This includes personal ties, social groups, economic organizations,
political bodies, scientific/cultural/magical research groups, and military formations.

## Relationships

Candidate relationship types include friendship, enmity, affection or love,
kinship, mentorship, rivalry, allegiance, debt, trust, and betrayal. A
relationship should have typed semantics and may have direction, strength,
status, start/end time, evidence, and the agents who know about it.

Avoid reducing complex social states to a single value such as "approval."
Different relations can coexist: two nobles may be allies politically and
personal rivals, or be publicly allied while privately plotting against one
another.

## Organizations

An organization is an entity with members, roles, governance, goals, resources,
and optional subgroups. Candidate organization kinds include:

- political groups, kingdoms, councils, and noble houses;
- guilds, syndicates, businesses, and commercial coalitions;
- universities, research institutions, companies, employers, and adventuring
  companies;
- religions, cults, and other belief-based groups;
- armies, battalions, militias, and alliances;
- informal groups such as rebels, crews, or social circles.

Membership can be multiple, temporary, contested, secret, or involuntary.
Represent membership and rank as explicit relations rather than assuming a
strict tree.

## Contracts and agreements

Contracts, treaties, marriages, vows, and other agreements can be modeled as
entities or events with parties, terms, obligations, validity, and status.
Their breaking, fulfillment, or renegotiation should be explicit events. A
marriage may create personal and political links; whether it merges kingdoms
must be a game rule, not a universal assumption.

## Governance and collective decisions

Organizations may make decisions through a leader, council, vote, delegation,
consensus, or another game-defined process. Governance rules should declare who
can participate, how proposals are introduced, how votes are counted, what
quorum or threshold applies, how ties and abstentions are handled, and when a
decision becomes binding.

Collective governance can be enabled by an optional decision-making
sub-plugin. A DAO- or smart-contract-inspired model can provide proposal
lifecycle, voting rounds, eligibility, execution conditions, and auditable
outcomes without requiring a blockchain, cryptocurrency, distributed ledger,
or external network service. Agreements and automated policies are modeled as
game-world data and evaluated locally unless a game explicitly chooses
otherwise.

Governance is not identical for every organization. A kingdom may use a
monarch's decision or a council; a guild may vote; an army may delegate
authority by rank; a university or company may use committees or executives.
The organization's configured policy chooses among available governance
strategies.

## Conflict and change

Events such as assassination, betrayal, rebellion, alliance, merger, or
succession can affect multiple relationships and organizations. The event
record should retain the actor(s) (if known), target, evidence, affected facts,
and rules used to derive follow-on changes. Reactions may differ by agent and
group, including support, opposition, neutrality, or lack of knowledge.

## Open questions

- Which organization behaviors are generic, and which need game-specific
  governance rules?
- How should contradictory accounts of a relationship be represented?
- Which group decisions are simulated centrally versus derived from member
  goals?
- Which governance policy is appropriate to each organization, and can it
  change over time?
