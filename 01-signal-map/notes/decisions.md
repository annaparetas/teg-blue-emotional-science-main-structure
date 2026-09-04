# Decisions · Emotional Signal Map

Dated entries, newest first. A decision recorded here changes the canon page
only when the page is edited and its "last approved" date moves.

## 2026-09-04 · Interactive Signal Map as a generated view

`map.html` shows the whole map as one navigable structure: two groups, nine
families, thirty-five signals, the five proposed additional experiences drawn
outside the families, and one record per signal. It is a view, not a second
home. Records are drawn from the canon page, rosters and neurochemistry page by
`scripts/build-signal-map-data.py` into `data/signals.js`, the same pattern
the Inner Compass uses for Model 2's rows. Re-run the script after any roster
edit.

The taxonomy is the primary map. Only Emotion records offer Fluid and Chronic
tabs; their Chronic tab contains the Position selector as a comparison tool.
Body-condition records show their Fluid record and a separate Chronic-access
boundary because they do not have Chronic tables. Every proposed additional
experience has a shareable URL. A signal's family never changes with the
reading or selected Position, and a selected profile is a far Chronic reference
pattern, never a person. Status: working view.

## 2026-09-04 · Wording pass and site ownership of the four carried pages

The Fluid roster no longer says "one condition, one direction", no longer
describes the families as built from "the evolved function of each
emotion-signal", and labels the two survival functions as an organising
synthesis rather than an exhaustive taxonomy. These are the three phrasings
the F1 and F2 connections note of 20 August flagged as sounding more settled
than the evidence allows. The family table and family intros had already been
decoupled from Positions on 2 September; the copies in the Development
Engine's working tree still carry the older coupled wording and are not
edited.

The neurochemistry grounding page now says each Emotion entry transfers "the
earlier synthesis written under Fluid reference A" (and A↔B, B, D) instead of
"the earlier Organisation A synthesis", and that a peripheral concentration
cannot identify "a Gradient Position" instead of "Organisation A". The family
headers say the Fluid reference is characteristic and illustrative.

The four carried Signal Map pages (Fluid roster, Chronic roster,
neurochemistry, recruitment bridge) graduated to site ownership on 4 September
2026. `scripts/carry.py` keeps their Engine source and reviewed ref in the
manifest, validates the boundary through `--ownership`, and skips them during
carry runs so an older snapshot cannot erase the current site synthesis. The
Development Engine continues to own later research and full provenance. A
later Engine finding crosses into these files only through review, an explicit
site edit and a dated decision entry.

Still open from the same note: an upstream F1 and F2 block on the Fluid page
before the four guiding questions, and a matching bridge on the
neurochemistry page after the research rule. Not added in this pass.

## 2026-09-04 · All five Body-condition families now have an initial synthesis

Thermal-balance, Visceral-capacity and Restorative-capacity now have the same
five-field records as the first two families: condition, possible conscious
access, what may raise priority, what may allow updating and interpretive
boundary. Their grounding received an initial paper-level orientation. This
closes the missing-family review; it does not turn the five TEG-Blue families
into established scientific natural kinds or complete a systematic evidence
review.

Fury and Frenzy now have distinct seven-position readings in the Chronic
roster, developed from their existing Fluid definitions. These are working
framework syntheses. They do not establish that a Gradient Position produces
an emotion or that an emotion identifies a Position.

## 2026-09-02 · Transferred into this folder; one home for the emotion list

The families and members now live only on [index.html](../index.html) and
the two rosters. The copy of the emotion tables on the old Gradient page
(working repository, `models/02-nervous-system-gradient/index.html`) is now
the duplicate. It is dropped when Model 2 is transferred, not before. Until
then no wording change is made there.

The rosters were taken from the ESM-S1 branch
(`codex/esm-s1-emotional-signal-map`, 26 August 2026), which is later than
the checked-out branch for these files. The neurochemistry page came from the
same branch.

## 2026-09-02 · Essential-supply and Bodily-integrity records approved

Respiratory-sufficiency, hydromineral-sufficiency and energy-and-nutrient
sufficiency records, and the pain record, approved as initial syntheses.
Pain deliberately bounded: no pain types, diagnoses, pathways, treatment or
chronic pain at this stage.

## 2026-09-02 · Five Body-condition families and the reading order

Five working families approved. Five-step reading order (condition, signal
and regulation, possible conscious access, updating condition, boundary)
approved as a reading order, not a biological sequence.

## 2026-08-27 · Love reference case accepted as working architecture

The Fluid and Chronic Love nine-layer records, the reusable schema and the
nine-layer filter are Anna-approved working architecture. Not public
authority. Evidence entries CL-E01 to CL-E16 are placeholders. Public release
is gated behind the five conditions in
[love-reference-case-completion-and-public-boundary.md](love-reference-case-completion-and-public-boundary.md).

## 2026-08-26 · Families decoupled from Positions

Emotion families are functional groupings. A family may be characteristically
readable under one Fluid reference position, but the association is
illustrative, not membership, and never runs in reverse. Row heading on the
Fluid roster changed from "Emotions" to "Emotional foregrounding ·
illustrative examples · not exclusive contents".

## 2026-08-23 · Completion and Return vocabulary

"What the signal needs" replaced by "possible completing condition". A Body
Signal's need is often direct; a Situation Signal's is relational and may
depend on another person's response. Recorded in
[body-and-situation-signals-what-they-need.md](body-and-situation-signals-what-they-need.md).

## 2026-08-20 · Fluid and Chronic rosters built

Fluid roster built as the companion to the Gradient page; emotion tables
duplicated on both by decision, pending a slim-down. Chronic roster built the
same day with four chronic reading questions (what holds, what the feeling
becomes, what can still be felt, what completion would require), Distorted
Signals as a separate section, and Fury and Frenzy as working cells.

## Open

- Individual emotion records: split out of the rosters as each is reviewed.
  Love first; its evidence review is deferred.
- Nine-layer filter and schema: cross-owner review with Models 1 to 3, F2 and
  Behaviour/HPR pending.
- ~~Gradient-page duplicate of the emotion tables: drop when Model 2 moves.~~
  Done 2 September 2026: Model 2 transferred and the duplicate dropped.
