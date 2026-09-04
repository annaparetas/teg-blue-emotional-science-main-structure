# Scientific Grounding Working-Set Review

Status: completed milestone review · next-step guidance superseded 19 August 2026
Scope: the scientific-grounding files created in this working session, including the later F1/Fluid/Chronic crosswalk
Purpose: decide what each file should continue to do, identify overlap and establish the next responsible phase

Current handoff: the three recommended pilots were completed. Use the [Integrated Grounding Review](../../reviews/integrated-grounding-2026-08-19.md) and [Pending Tasks Register](../../../STATUS.md) for present authority and next work.

## Overall assessment

The files now form a coherent base layer, but they are not all the same kind of document. Their value depends on keeping four functions separate:

1. **claim architecture** — what TEG-Blue currently says;
2. **research-family routing** — which bodies of knowledge may be relevant;
3. **framework lineage** — how earlier models relate to current claims;
4. **source-level grounding** — what individual studies can actually support.

The first three functions now have a workable structure. The fourth has begun through selected anchors and boundaries, but has not yet been completed claim by claim.

The next phase should therefore deepen evidence rather than create another broad map.

## File-by-file review

| File | Present function | What it contributes | What it should not become | Decision |
| --- | --- | --- | --- | --- |
| [Scientific Lineage and Integrative Grounding](../../reviews/scientific-lineage-and-integrative-grounding.md) | System-level orientation | Six interacting levels, time, three scientific identities and lineage relationships | A catalogue of every researcher or a source ledger | **Keep as the conceptual introduction.** |
| [Current Construct Grounding Registry](../../claims/current-construct-grounding-registry.md) | Master index | One place to see constructs, roles, ownership and grounding state | The place where full evidence reviews are written | **Keep short; use it to route work.** |
| [Current Construct Claim Decomposition](../../claims/current-construct-decomposition.md) | Claim architecture | Separates definition, phenomenon, mechanism, development, application and boundary claims | A framework-family list | **Make this the primary unit of future grounding.** |
| [Original Frameworks → Current Claims](../../reviews/original-frameworks-claim-reassessment.md) | Historical lineage crosswalk | Recovers useful ancestry while distinguishing direct, partial, contextual and challenged contributions | Proof that TEG-Blue is validated because many frameworks resemble it | **Keep as lineage; revisit only when claim evidence changes.** |
| [Terminology and Concept Improvement Register](../terminology-and-concept-improvement.md) | Language and concept audit | Records terms that improve precision and exposes conflations | A second definitions file competing with the claim decomposition | **Convert accepted decisions into the construct definitions over time.** |
| [Harm, Power and Repair Grounding](../../../07-reference/grounding/harm-power-and-repair.md) | Behavioural and ethical claim family | Keeps internal protection separate from power, coercion, impact, responsibility and repair | A nervous-system explanation of harmful behaviour | **Preserve as a parallel assessment plane.** |
| [Trauma, Stress and Adversity Research Map](../../../05-frameworks/F02/grounding/trauma-stress-and-adversity-research-map.md) | Typed research-family intake | Separates exposure, response, development, mechanism, diagnosis, outcome and recovery | One umbrella trauma theory or a list of famous names | **Keep as the trauma research index.** |
| [F2 · Trauma, Stress and Adversity Crosswalk](../../../05-frameworks/F02/grounding/trauma-stress-and-adversity-crosswalk.md) | Claim-to-family routing for F2 | Connects evidence to signal generation, representation, access, identification, expression, action and emotion belief | Evidence that adult behaviour reveals childhood history | **Use as the source-search plan for F2.** |
| [F1, Fluid and Chronic Scientific Grounding Crosswalk](../../../05-frameworks/F01/index.html) | Framework-layer routing | Separates evolutionary availability, present organisation and learned persistence across 31 research families | A claim that one theory grounds the whole Gradient | **Use to build three smaller scientific spines.** |

## What is working well

### The unit of analysis has changed

The work no longer asks whether a whole framework “supports TEG-Blue”. It asks which kind of claim a source can support and where the inference must stop. This is the most important structural improvement.

### Several repeated conflations are now visible

The working set consistently separates:

- exposure from mechanism and diagnosis;
- signal from interpretation;
- emotion from behaviour;
- activation from danger;
- immobility from consent;
- adaptation from inevitability;
- internal restriction from harm to others;
- explanation from responsibility;
- evolutionary capacity from developmental learning;
- present organisation from chronic persistence.

### The framework layers now have clearer ownership

- F1 owns evolutionary availability.
- F2 owns developmental shaping of access and participation.
- Fluid owns present-condition correspondence, flexible action, updating and Return.
- Chronic owns recurrent recruitment, narrowing, generalisation, persistence and difficult updating.
- Harm, Power and Repair owns relational action, coercion, impact, accountability and repair.

This division is not complete, but it is coherent enough to guide the next research pass.

## Where overlap needs management

### Research families recur across several files

Attachment, interoception, allostasis, conditioning, controllability, mentalization and adversity dimensions appear in more than one map. That is appropriate because they answer different questions. It will become confusing if each file develops its own independent summary of the same evidence.

**Decision:** create one source record for a study or review, then link its relevant findings to several claims. Do not rewrite the source from scratch in every crosswalk.

### Terminology decisions and construct definitions can diverge

The terminology register contains better language that has not yet been accepted into every construct definition or active page.

**Decision:** give each terminology proposal one of four states: proposed, accepted, implemented or rejected. Only accepted terms should move into claim definitions.

### Research maps are broader than the active model needs

The trauma register contains 37 families plus missing candidates; the new crosswalk contains 31 families. Only a smaller subset will carry the central architecture.

**Decision:** keep broad maps for coverage, but build narrow evidence spines for each active framework.

### F1 lives in a separate repository

The F1 active file belongs to the Foundational Diagrams repository, while the present crosswalk lives with the Inner Compass grounding system.

**Decision:** keep the evidence architecture here until it stabilises. When claims are ready, implement F1 changes in its own repository through a separate, traceable commit.

## The architecture to use from now on

```text
Scientific grounding protocol
        ↓
Current construct registry
        ↓
Claim decomposition and claim IDs
        ↓
Research-family maps and framework crosswalks
        ↓
Source records linked to exact claims
        ↓
Claim decisions and terminology decisions
        ↓
Careful changes to active framework pages
```

The maps help us find the evidence. They are not themselves the evidence.

## Recommended next phase

### 1 · Create one shared source-record format

Each source record should contain:

- stable source ID and full citation;
- source type and evidence level;
- population or species;
- design and measures;
- phenomenon actually studied;
- result relevant to TEG-Blue;
- claim IDs it may support;
- what it cannot establish;
- conflicts, limitations and replication status;
- decision: supports, partially supports, challenges, contextualises or remains uncertain.

### 2 · Pilot the method on three architectural bridges

Begin with three areas that affect several files:

1. **allostasis, resource allocation and Return** — IC-03, IC-10, IC-11, NG-01, NG-02 and NG-04;
2. **interoception, bodily representation and conscious access** — IC-02, IC-04, IC-06, IC-08, IC-09 and RC-01;
3. **learning, controllability, generalisation and updating** — IC-07, IC-10, NG-02, NG-04 and the F2 action/belief layers.

These pilots will show whether the registry and claim structure work before hundreds of sources are added.

### 3 · Build a narrow spine for each framework

- F1: viability, sensing, affect/action, defence, relationship and reflective-symbolic capacity.
- F2: relational learning, access, identification, expression, action and learned expectation.
- Fluid: correspondence, action availability, contextual discrimination, regulation and Return.
- Chronic: recruitment threshold, weighting, generalisation, restricted action, persistence and updating.
- Harm/Power/Repair: agency, coercion, impact, feedback, responsibility and recurrence.

### 4 · Delay broad active-page revision

The active files should change only after a claim has:

1. an agreed definition;
2. a specified claim type;
3. at least one appropriate source record;
4. a recorded boundary;
5. language proportionate to the evidence.

This prevents an attractive research theory from being inserted into several pages before its precise contribution is understood.

## Concepts likely to improve significantly

The present work suggests that the following areas may change materially once source-level grounding begins:

- Fluid and Chronic as correspondence and learned availability rather than state intensity;
- Return as updating, action completion, recovery and renewed capacity rather than simple calm;
- Body Signals as bodily information rather than a fixed emotion–chemical code;
- Situation Signals as relevance-bearing information whose interpretation remains testable;
- emotion override as several separable changes in access, identification, expression and action;
- safety as contextual, relational and learned information rather than absence of arousal;
- connection as a regulatory resource without assuming synchrony, closeness or compliance is beneficial;
- shutdown as a family of distinct phenomena rather than one parasympathetic endpoint;
- Chronic protection as persistence that may once have fitted conditions without excusing present harm;
- harmful behaviour as an action-and-power question that cannot be read directly from internal organisation.

## Decision

The working set is ready to move from **mapping** to **claim-level evidence records**.

The best next action is not another comprehensive framework list. It is a small, demanding pilot that tests the method on allostasis/Return, interoception/access and learning/updating. Once those three bridges are grounded, we can see which parts of the Inner Compass, F1, F2 and the Fluid–Chronic depth model require revision and which already hold.
