# Understanding the Nervous System Gradient in a new session

The model describes present organism-level resource and capacity organisation
across Fluid and Chronic reference positions. Read a position as an organisation
in a context, not a whole person, emotion, behaviour, diagnosis or moral category.

## Follow the explanation

1. [Model overview](index.html): what the Gradient describes and the ownership boundaries.
2. [Governing premise](premise.html): regulation, resource allocation, graded language and the same sixteen questions at every position.
3. [Original Gradient table in the site](positions.html): the current Fluid and Chronic rows across X, A, A↔B, B, C, D and Z. Each position heading opens its record.
4. [Connected position record](position.html): read one position through both organisations. [Readable records](position-records.md) contain the same sourced material for sessions without a browser.
5. [Fluid and Chronic](fluid-chronic.html): how organisation relates to present conditions. These are readings of the same positions, not additional positions or person types.
6. [Depth](depth.html): the overview of recruitment, information weighting, differentiation, flexibility and updating. [Intermediate patterns](intermediate-layers.html) expand the comparison. Both retain working status; they are not a score or a new access scale.
7. [Autonomic participation](autonomic.html): specific source entries for each position and reading, including tasks, pathway participation, organ-level patterns, timing and limits.
8. [Return and recovery](return.html): the nine terms and the partial workbench. Autonomic updating descriptions do not replace the missing route analysis.

The navigation carries the selected position and reading into companion pages
and offers an explicit return link. Exact source links can also open the relevant
cell in the original table. Model 2 uses Model → position → processes → updating;
it does not borrow the Signal Map's group and family taxonomy.

## Answer the same sixteen questions

The questions are read directly from [the governing premise](premise.html#lenses).
The generator maps existing source excerpts to them. A mapped excerpt does not
mean the question has been fully answered or empirically validated.

- Organisational problem and allocation: what demand is being organised for, and what capacities receive priority?
- Biological participation: autonomic, energy, cardiovascular, respiratory, motor and non-urgent processes. Several currently share one organ-level description; separate explanations remain open.
- Information and participation: sensory organisation, attention, interoception, emotional processing, cognition and social engagement.
- Action and change: available responses, updating and transition / Return.

Keep what processes are recruited separate from what becomes consciously
available and usable. Model 1 owns conscious access and ME participation.
Model 3 owns how response and feedback unfold through time. Behaviour and
repair require their own evidence. A position cannot assign an access band.

## Preserve the original and later revisions

The original Development Engine page is
`inner-compass-nervous-system-organization-gradient/models/02-nervous-system-gradient/index.html`.
Its six-file folder supplied the site's table, premise, depth, intermediate,
autonomic and Return companions. [The source comparison](notes/source-comparison.md)
records the relationship. [The decisions](notes/decisions.md) explain later site
revisions, including the 4 September Model 1 / Model 2 access boundary.

The current site table is the source for the new records. Do not copy the Engine
index over it: that would restore older wording and duplicate emotion material.
The six carried HTML pages are now protected by the site's carry manifest;
their source paths remain recorded there. Later Engine research requires review
and a dated site decision. Neither this guide nor generated records supersede
an owning source page.

## Distinguish architecture, working explanation and evidence

Position names, reference structure and governing rules retain their existing
approval. Many position definitions and biological descriptions remain working
syntheses. Preserve their source limits even when a row uses compressed wording.
No short table label establishes objective danger or a unique autonomic profile.

The full sixteen-lens structure is not a completed mechanism account. The Return
workbench has incomplete Fluid fields; a completed Chronic route matrix remains
open. The depth/profile visual still needs owner review. Keep current adverse
conditions, learned expectation and persistence after changed conditions distinct.

Consult [Model 2 grounding](grounding.md), the [Fluid science matrix](grounding/fluid-gradient-organisation-science-matrix.md)
and [Chronic scientific spine](grounding/chronic-scientific-spine.md) before adding
scientific explanations. Do not infer a mechanism from a familiar label.

## Maintain the connected records

Edit `positions.html`, `autonomic.html` or `premise.html` according to the
question's owner, then run these commands from the site root:

```sh
python3 scripts/build-gradient-data.py
python3 scripts/build-gradient-data.py --check
python3 scripts/check-local-links.py
python3 scripts/carry.py --ownership
```

If table wording changes, also regenerate the Inner Compass source data with
`python3 scripts/build-compass-data.py`. Keep the generated records aligned with
the sources; do not edit `data/positions.js` or `position-records.md` directly.
