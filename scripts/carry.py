#!/usr/bin/env python3
"""Carry reviewed pages from the active Development Engine into this site.

One manifest drives everything. For each entry the script:

1. copies the source file from a path or reviewed Git branch of the Development
   Engine;
2. applies any named transform (for example cutting the emotion tables out of
   the old Gradient page);
3. rewrites every relative link: the link is resolved against the file's old
   location, looked up in MOVES, and rewritten relative to its new location.
   Targets that have not moved yet fall back to the Development Engine and are
   reported;
4. inserts a "carried" banner after <body>.

Re-running the script regenerates every carried file from source, so edits
belong in the manifest or the transforms, never in the carried files.

Usage:  python3 scripts/carry.py            (all entries)
        python3 scripts/carry.py 03-        (entries whose new path starts with 03-)
"""

from __future__ import annotations

import posixpath
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT.parent / "inner-compass-nervous-system-organization-gradient"
ENGINE_REL = "../inner-compass-nervous-system-organization-gradient"
ESM_S1 = "codex/esm-s1-emotional-signal-map"   # newer signal-map text

# ---------------------------------------------------------------- manifest
# new path (relative to ROOT), old path (relative to the old repo root),
# git ref to read from (None = working tree), transform name, banner.
MANIFEST = [
    # Foundations · what TEG-Blue is and the rules it works under
    ("foundations/notes/00-working-definition.md", "foundation/00-working-definition.md", None, None, None),
    ("foundations/notes/02-established-research.md", "foundation/02-established-research.md", None, None, None),
    ("foundations/notes/04-ethics-and-responsibility.md", "foundation/04-ethics-and-responsibility.md", None, None, None),
    ("foundations/notes/06-state-shaped-perception.md", "foundation/06-state-shaped-perception.md", None, None, None),
    ("foundations/notes/12-emotions-as-information.md", "foundation/12-emotions-as-information.md", None, None, None),
    ("foundations/notes/13-emotional-access-and-reality-contact.md", "foundation/13-emotional-access-and-reality-contact.md", None, None, None),
    ("foundations/notes/16-where-teg-blue-sits.md", "foundation/16-where-teg-blue-sits.md", None, None, None),
    ("foundations/notes/20-working-architectural-language.md", "foundation/20-working-architectural-language.md", None, None, None),
    ("foundations/notes/sources/08-acute-chronic-formations.md", "foundation/08-acute-chronic-formations.md", None, None, None),
    ("foundations/notes/sources/origin-00-timeline.md", "foundation/origin-00-timeline.md", None, None, None),
    ("foundations/notes/sources/origin-01-map-register.md", "foundation/origin-01-map-register.md", None, None, None),
    ("foundations/notes/sources/foundation-library-README.md", "foundation/README.md", None, None, None),
    ("foundations/notes/three-model-architecture.md", "development/decisions/three-model-architecture.md", None, None, None),
    ("foundations/notes/working-architectural-language-and-evidence-levels.md", "development/decisions/working-architectural-language-and-evidence-levels.md", None, None, None),

    # 04 · Model 3 · The Emotional–Somatic Cycle
    ("04-model-3-esc/cycle.html", "models/03-emotional-systems-cycle/index.html", None, None,
     ("Carried page · status approved architecture", "The canonical two-cycle page: the shared event spine, the whole operating sequence, the Fluid and Chronic Cognitive-Override comparison, the seven override distinctions, the Chronic cascade and the bridge to Model 2. Canonical since 23 August 2026; carried on 2 September 2026. The canon page summarises it; this is the full statement.", "index.html", "Model 3")),
    ("04-model-3-esc/shared-event-record.html", "models/shared-event-record.html", None, None,
     ("Carried coupling interface · status working", "How the three models describe one changing event: the coupling rule, the moments, the six record fields and what feedback changed. Carried on 2 September 2026. Cross-model, held by Model 3 as the temporal owner.", "index.html", "Model 3")),
    ("04-model-3-esc/grounding/ESC-component-decomposition.md", "evidence/claims/ESC-component-decomposition.md", None, None, None),
    ("04-model-3-esc/grounding/ESC-cognitive-override-grounding.md", "evidence/reviews/ESC-cognitive-override-grounding.md", None, None, None),
    ("04-model-3-esc/notes/M1-M2-M3-extraction.md", "development/decisions/M1-M2-M3-extraction.md", None, None, None),
    ("04-model-3-esc/notes/sources/esc-and-escalation-pathways-archive.html", "models/03-emotional-systems-cycle/esc-and-escalation-pathways-archive.html", None, None,
     ("Carried archive · status archived", "The earlier ESC and escalation-pathways page and the paused coupling draft, preserved as a labelled comparison. Superseded by the canonical two-cycle page on 23 August 2026. Provenance only.", "../../index.html", "Model 3")),
    ("04-model-3-esc/notes/sources/ESC-scientific-grounding-core-source-pack.md", "evidence/reviews/ESC-scientific-grounding-core-source-pack.md", None, None, None),

    # 01 · Signal Map
    ("01-signal-map/emotion/fluid.html", "signal-map/fluid.html", ESM_S1, None,
     ("Carried page · status working", "The full Fluid roster of Body and Situation Signals. Carried on 2 September 2026 from the working repository (signal-map/fluid.html, ESM-S1 branch text). It is the only home of the emotion tables.", "../index.html", "Signal Map")),
    ("01-signal-map/emotion/chronic.html", "signal-map/chronic.html", ESM_S1, None,
     ("Carried page · status working", "The Chronic companion reading of the same signals. Carried on 2 September 2026 from the working repository (signal-map/chronic.html, ESM-S1 branch text).", "../index.html", "Signal Map")),
    ("01-signal-map/grounding/neurochemistry.html", "signal-map/neurochemistry.html", ESM_S1, None,
     ("Carried grounding page · status working", "Signal-by-signal neurochemistry hooks. Carried on 2 September 2026 from the working repository (ESM-S1 branch text). Evidence, not canon.", "../index.html", "Signal Map")),
    ("01-signal-map/grounding/recruitment-persistence-and-recovery.html", "signal-map/signal-recruitment-persistence-and-recovery.html", ESM_S1, None,
     ("Carried grounding page · status working", "Scientific bridge from recruitment to persistence and recovery. Carried on 2 September 2026 from the working repository. Evidence, not canon.", "../index.html", "Signal Map")),
    ("01-signal-map/notes/sources/chronic-emotional-signals-collection.html", "development/model-notes/chronic-emotional-signals-collection.html", None, None,
     ("Carried source collection · status archived", "Raw collection of chronic emotional-signal descriptions gathered on 20 August 2026 from the older TEG-Blue corpus. Provenance for the Chronic roster, not current authority.", "../../index.html", "Signal Map")),
    ("01-signal-map/notes/body-and-situation-signals-what-they-need.md", "development/model-notes/body-and-situation-signals-what-they-need.md", None, None, None),
    ("01-signal-map/notes/nine-layer-emotional-signal-participation-filter.md", "development/model-notes/nine-layer-emotional-signal-participation-filter.md", None, None, None),
    ("01-signal-map/notes/fluid-chronic-emotion-analysis-reference-schema.md", "development/model-notes/fluid-chronic-emotion-analysis-reference-schema.md", None, None, None),
    ("01-signal-map/notes/fluid-love-nine-layer-signal-structure.md", "development/model-notes/fluid-love-nine-layer-signal-structure.md", None, None, None),
    ("01-signal-map/notes/chronic-love-nine-layer-signal-structure.md", "development/model-notes/chronic-love-nine-layer-signal-structure.md", None, None, None),
    ("01-signal-map/notes/fluid-chronic-love-nine-layer-comparison-and-owner-handoff.md", "development/decisions/fluid-chronic-love-nine-layer-comparison-and-owner-handoff.md", None, None, None),
    ("01-signal-map/notes/love-reference-case-completion-and-public-boundary.md", "development/decisions/love-reference-case-completion-and-public-boundary.md", None, None, None),

    # 02 · Model 1 · ESS · CLS · ME
    ("02-model-1-ess-cls-me/access.html", "models/01-information-systems/coordinated-conscious-access.html", None, None,
     ("Carried page · status approved", "Coordinated conscious access: the eleven-stage functional sequence, the hunger worked example and three Situation Signal paths. Approved on 26 August 2026 as Model 1's canonical access page; carried on 2 September 2026. The canon page holds the definitions; this page shows the sequence.", "index.html", "Model 1")),
    ("02-model-1-ess-cls-me/notes/sources/relational-capacities.html", "models/01-information-systems/relational-capacities.html", None, "capacities_sync",
     ("Carried source · status archived", "The eight configurations and the five quality dimensions as carried from the working repository on 2 September 2026. Superseded on 3 September 2026 by the <a href=\"../../me-access.html\">ME access add-on</a>, which absorbed this page and the capacity controller. Kept as provenance; the switches still read and write the shared setting.", "../../index.html", "Model 1")),
    ("02-model-1-ess-cls-me/processing.html", "models/01-information-systems/sensory-processing.html", None, None,
     ("Carried grounding page · status working", "How the body reads conditions before conscious access: the processing field, detection versus emotion, and the research foundations. Carried on 2 September 2026. Grounding, not canon.", "index.html", "Model 1")),
    ("02-model-1-ess-cls-me/grounding/ESS-CLS-component-decomposition.md", "evidence/claims/ESS-CLS-component-decomposition.md", None, None, None),
    ("02-model-1-ess-cls-me/grounding/relational-configuration-clinical-pattern-bridge.md", "evidence/reviews/relational-configuration-clinical-pattern-bridge.md", None, None, None),
    ("02-model-1-ess-cls-me/grounding/six-cluster-synthesis-and-F03-construct-families.md", "evidence/reviews/six-cluster-synthesis-and-F03-construct-families.md", None, None, None),
    ("02-model-1-ess-cls-me/notes/ESS-CLS-terminology-and-architecture.md", "development/decisions/ESS-CLS-terminology-and-architecture.md", None, None, None),
    ("02-model-1-ess-cls-me/notes/model-sketch.md", "development/model-notes/two-biological-information-systems-model-sketch.md", None, None, None),
    ("02-model-1-ess-cls-me/notes/sources/ESS-CLS-legacy-deep-dive.md", "development/model-notes/ESS-CLS-legacy-deep-dive.md", None, None, None),
    ("02-model-1-ess-cls-me/notes/sources/description-collection.md", "development/model-notes/two-biological-information-systems-description-collection.md", None, None, None),

    # 05 · Frameworks · F1, F2, F3
    ("05-frameworks/F01/review.md", "frameworks/reviews/F01-evolution.md", None, None, None),
    ("05-frameworks/F01/crosswalk.html", "frameworks/crosswalks/F01-evolution-to-fluid-gradient.html", None, None,
     ("Carried bridge · status working", "The many-to-many handoff from evolutionary capacity to present Fluid organisation. Carried on 2 September 2026. A bridge beside F1, not a second source of truth for the positions.", "index.html", "F1")),
    ("05-frameworks/F01/timeline.html", "frameworks/diagrams/F1/F1-Timeline.html", None, None,
     ("Carried visual account · status working", "The provisional eight-expansion evolutionary capacity timeline. Carried on 2 September 2026 as F1's current visual account. An orientation and research map, not a dated ladder. The other F1 diagram files stay in the Development Engine.", "index.html", "F1")),
    ("05-frameworks/F01/notes/F01-F02-connections-to-four-support-pages.md", "frameworks/crosswalks/F01-F02-connections-to-four-support-pages.md", None, None, None),
    ("05-frameworks/F02/review.md", "frameworks/reviews/F02-development.md", None, None, None),
    ("05-frameworks/F02/diagram.html", "frameworks/diagrams/F2-Emotion-Override/F2-emotion-overriding.html", None, None,
     ("Carried active account · status working", "What develops when emotion must be overridden: the seven layers where learning can intervene, the practice loop, the three forms of ME participation, and what the current sources carry. Carried on 2 September 2026 as F2's current active account.", "index.html", "F2")),
    ("05-frameworks/F02/notes/developmental-entries.md", "development/registers/F02-developmental-entries.md", None, None, None),
    ("05-frameworks/F02/grounding/trauma-stress-and-adversity-crosswalk.md", "evidence/crosswalks/F02-trauma-stress-and-adversity.md", None, None, None),
    ("05-frameworks/F02/grounding/trauma-stress-and-adversity-research-map.md", "evidence/reviews/trauma-stress-and-adversity-research-map.md", None, None, None),
    ("05-frameworks/F03/review.md", "frameworks/reviews/F03-adult-maintenance-and-revision.md", None, None, None),
    ("05-frameworks/F04/review.md", "frameworks/reviews/F04-shared-rules.md", None, None, None),
    ("05-frameworks/F05/review.md", "frameworks/reviews/F05-social-valuation.md", None, None, None),
    ("05-frameworks/F06/review.md", "frameworks/reviews/F06-bias-and-judgement.md", None, None, None),
    ("05-frameworks/F07/review.md", "frameworks/reviews/F07-power-and-enforcement.md", None, None, None),
    ("05-frameworks/F08/review.md", "frameworks/reviews/F08-recovery-and-repair.md", None, None, None),
    ("05-frameworks/F09/review.md", "frameworks/reviews/F09-neurodivergence-and-fit.md", None, None, None),
    ("05-frameworks/F10/review.md", "frameworks/reviews/F10-intergenerational-pathways.md", None, None, None),
    ("05-frameworks/F11/review.md", "frameworks/reviews/F11-responsible-integration.md", None, None, None),
    ("05-frameworks/F12/review.md", "frameworks/reviews/F12-emotional-authority.md", None, None, None),

    # 07 · Reference · behaviour and responsibility, human sociality
    ("07-reference/behaviour.html", "reference/behaviour-and-responsibility.html", None, None,
     ("Carried page · status approved reference", "Behaviour across the Gradient: the seven Positions on both planes written as what another person could observe, with the inferred and from-inside rows marked as such. Canonical cross-model reference since 23 August 2026; carried on 3 September 2026.", "index.html", "Reference")),
    ("07-reference/sociality.html", "reference/human-sociality-and-two-survival-functions.html", None, None,
     ("Carried page · status approved reference", "Human sociality and the two survival functions: the central proposition, the evidence stack, the cross-model ownership map, the claim-status ledger and the core source routes. Canonical since 23 August 2026; carried on 3 September 2026.", "index.html", "Reference")),
    ("07-reference/grounding/harm-power-and-repair.md", "evidence/reviews/harm-power-and-repair.md", None, None, None),

    # Evidence · protocol, source record, claims, pilots, reviews, registers
    ("evidence/protocol.html", "evidence/protocol/index.html", None, None,
     ("Carried page · status approved protocol", "The Science Grounding Protocol: the governing rule, question zero, the two searches, the evidence families, the selection boundaries, the protected research programme, the two labels and the minimum record. Governing since 22 August 2026; carried on 3 September 2026.", "index.html", "Evidence")),
    ("evidence/sources/shared-source-record-index.md", "development/registers/shared-source-record-index.md", None, None, None),
    ("evidence/claims/current-construct-decomposition.md", "evidence/claims/current-construct-decomposition.md", None, None, None),
    ("evidence/claims/current-construct-grounding-registry.md", "evidence/claims/current-construct-grounding-registry.md", None, None, None),
    ("evidence/pilots/PILOT-01-allostasis-resource-allocation-and-return.md", "evidence/pilots/PILOT-01-allostasis-resource-allocation-and-return.md", None, None, None),
    ("evidence/pilots/PILOT-02-interoception-bodily-representation-and-access.md", "evidence/pilots/PILOT-02-interoception-bodily-representation-and-access.md", None, None, None),
    ("evidence/pilots/PILOT-03-learning-controllability-generalisation-and-updating.md", "evidence/pilots/PILOT-03-learning-controllability-generalisation-and-updating.md", None, None, None),
    ("evidence/pilots/PILOT-04-ess-condition-reading-and-emotional-significance.md", "evidence/pilots/PILOT-04-ess-condition-reading-and-emotional-significance.md", None, None, None),
    ("evidence/pilots/PILOT-05-mentalizing-affective-sharing-and-instrumental-use.md", "evidence/pilots/PILOT-05-mentalizing-affective-sharing-and-instrumental-use.md", None, None, None),
    ("evidence/pilots/PILOT-06-entitlement-self-threat-power-and-retaliation.md", "evidence/pilots/PILOT-06-entitlement-self-threat-power-and-retaliation.md", None, None, None),
    ("evidence/pilots/PILOT-07-people-pleasing-dependency-appeasement-and-refusal.md", "evidence/pilots/PILOT-07-people-pleasing-dependency-appeasement-and-refusal.md", None, None, None),
    ("evidence/pilots/PILOT-08-avoidance-detachment-and-chosen-distance.md", "evidence/pilots/PILOT-08-avoidance-detachment-and-chosen-distance.md", None, None, None),
    ("evidence/pilots/PILOT-09-control-overcontrol-and-coercive-control.md", "evidence/pilots/PILOT-09-control-overcontrol-and-coercive-control.md", None, None, None),
    ("evidence/pilots/PILOT-10-self-other-distinction-identity-and-attachment-stress.md", "evidence/pilots/PILOT-10-self-other-distinction-identity-and-attachment-stress.md", None, None, None),
    ("evidence/reviews/scientific-lineage-and-integrative-grounding.md", "evidence/reviews/scientific-lineage-and-integrative-grounding.md", None, None, None),
    ("evidence/reviews/original-frameworks-claim-reassessment.md", "evidence/reviews/original-frameworks-claim-reassessment.md", None, None, None),
    ("evidence/reviews/scientific-architecture-inventory.md", "evidence/reviews/scientific-architecture-inventory.md", None, None, None),
    ("evidence/reviews/integrated-grounding-2026-08-19.md", "evidence/reviews/integrated-grounding-2026-08-19.md", None, None, None),
    ("evidence/notes/sources/scientific-grounding-working-set.md", "evidence/reviews/scientific-grounding-working-set.md", None, None, None),
    ("evidence/notes/project-terminology-ledger.md", "development/registers/project-terminology-ledger.md", None, None, None),
    ("evidence/notes/terminology-and-concept-improvement.md", "development/registers/terminology-and-concept-improvement.md", None, None, None),
    ("evidence/notes/three-corrections-terminology.md", "development/decisions/three-corrections-terminology.md", None, None, None),
    ("01-signal-map/grounding/chemical-mediators-and-prolonged-stress.md", "development/model-notes/chemical-mediators-and-prolonged-stress.md", None, None, None),

    # 06 · Inner Compass and the 4-Mode Gradient
    ("06-inner-compass-four-modes/notes/four-mode-gradient-architecture.md", "development/decisions/four-mode-gradient-architecture.md", None, None, None),

    # 03 · Model 2 · Gradient
    ("03-model-2-gradient/positions.html", "models/02-nervous-system-gradient/index.html", None, "gradient_tables",
     ("Carried page · status working", "The row-by-row Fluid and Chronic tables for the seven Positions. Carried on 2 September 2026 from the working repository's main Gradient page. The emotion tables it used to duplicate were removed; the Signal Map is their only home. The ME access controls are set on the <a href=\"../02-model-1-ess-cls-me/me-access.html\">Model 1 add-on</a>; the reading that changes with them is the <a href=\"../06-inner-compass-four-modes/compass.html\">Inner Compass</a>, drawn from these rows.", "index.html", "Model 2")),
    ("03-model-2-gradient/premise.html", "models/02-nervous-system-gradient/governing-premise.html", None, None,
     ("Carried governing page · status approved", "The interpretive rules for reading the Gradient: regulation is not calm, organisation is not behaviour or emotion, graded language, fit versus mismatch, and the sixteen lenses. Carried on 2 September 2026. The canon page summarises it; this is the full statement.", "index.html", "Model 2")),
    ("03-model-2-gradient/depth.html", "models/02-nervous-system-gradient/fluid-chronic-depth.html", None, None,
     ("Carried page · status working", "The three-coordinate view (organisation, processing layer, depth) and the six depth variables. Carried on 2 September 2026. Depth is the visual orientation; the persistence and flexibility profile is the construct. To be merged with the intermediate-layers page.", "fluid-chronic.html", "Fluid and Chronic")),
    ("03-model-2-gradient/intermediate-layers.html", "models/02-nervous-system-gradient/intermediate-layers.html", None, None,
     ("Carried page · status working", "The intermediate field between the Fluid and far Chronic reference planes, with the six-variable matrix. Carried on 2 September 2026. To be merged with the depth page.", "fluid-chronic.html", "Fluid and Chronic")),
    ("03-model-2-gradient/return.html", "models/02-nervous-system-gradient/return-and-recovery.html", None, None,
     ("Carried workbench · status working", "Completion, Return and recovery across the Fluid Gradient: nine words that are not interchangeable, the Fluid route matrix, and the research-term crosswalk. Chronic routes not yet written. Carried on 2 September 2026.", "index.html", "Model 2")),
    ("03-model-2-gradient/autonomic.html", "models/02-nervous-system-gradient/autonomic-organisation.html", None, None,
     ("Carried grounding page · status working", "Autonomic participation for the fourteen organisations, without one-pathway state claims. Every entry is a functional synthesis awaiting paper-grounded review. Carried on 2 September 2026.", "index.html", "Model 2")),
    ("03-model-2-gradient/grounding/fluid-gradient-organisation-science-matrix.md", "evidence/reviews/fluid-gradient-organisation-science-matrix.md", None, None, None),
    ("03-model-2-gradient/grounding/chronic-scientific-spine.md", "evidence/reviews/chronic-scientific-spine.md", None, None, None),
    ("03-model-2-gradient/notes/fluid-chronic-profile-and-visual-axis.md", "development/decisions/fluid-chronic-profile-and-visual-axis.md", None, None, None),
    ("03-model-2-gradient/notes/regulation-pass.md", "development/decisions/regulation-definition-and-F01-F12-pass.md", None, None, None),
    ("03-model-2-gradient/notes/regulation-current-use.md", "development/registers/regulation-current-use.md", None, None, None),
    ("03-model-2-gradient/notes/regulation-and-return-concepts.md", "development/model-notes/regulation-and-return-concepts.md", None, None, None),
    ("03-model-2-gradient/notes/sources/regulation-and-return-workbench.html", "development/model-notes/regulation-and-return-workbench.html", None, None,
     ("Carried workbench · status archived", "The 12 August 2026 regulation and Return workbench. Its settled concepts were absorbed into the Return page and the concepts note. Provenance only.", "../../index.html", "Model 2")),
]

ENGINE_HOME = {new: old for new, old, *_ in MANIFEST}

# old path -> new path for everything that has a home here.
MOVES = {old: new for new, old in ENGINE_HOME.items()}
MOVES.update({
    # The carried capacities page is provenance now; links to it mean the add-on.
    "models/01-information-systems/relational-capacities.html": "02-model-1-ess-cls-me/me-access.html",
    "assets/page-responsibility.css": "assets/page-responsibility.css",
    "assets/model-coupling.css": "assets/model-coupling.css",
    "assets/capacities.js": "assets/capacities.js",
    "index.html": "index.html",
    "project-map.html": "index.html",
    "README.md": "README.md",
    "development/session-control-board.md": "STATUS.md",
    "development/roadmap.md": "STATUS.md",
    "development/registers/project-terminology-ledger.md": "GLOSSARY.md",
    "foundation/22-nervous-system-gradient.md": "03-model-2-gradient/index.html",
    "foundation/23-fluid-and-chronic-organisation.md": "03-model-2-gradient/fluid-chronic.html",
    "foundation/21-information-systems-inner-compass-and-me.md": "02-model-1-ess-cls-me/index.html",
    "models/01-information-systems/inner-compass-sequence.html": "02-model-1-ess-cls-me/access.html",
    "foundation/24-emotional-somatic-cycle.md": "04-model-3-esc/index.html",
    "models/03-emotional-systems-cycle/esc-two-cycle-rebuild.html": "04-model-3-esc/cycle.html",
    "evidence/crosswalks/F01-fluid-chronic-grounding.md": "05-frameworks/F01/index.html",
    "frameworks/index.html": "05-frameworks/index.html",
    "frameworks/README.md": "05-frameworks/index.html",
    "reference/README.md": "07-reference/index.html",
    "evidence/README.md": "evidence/index.html",
    "evidence/reviews/six-cluster-synthesis-and-F03-construct-families.md": "02-model-1-ess-cls-me/grounding/six-cluster-synthesis-and-F03-construct-families.md",
})
# Folder prefixes for concepts that are still placeholders.
PREFIXES = [
    ("models/01-information-systems/", "02-model-1-ess-cls-me/index.html"),
    ("models/02-nervous-system-gradient/", "03-model-2-gradient/index.html"),
    ("models/03-emotional-systems-cycle/", "04-model-3-esc/index.html"),
    ("models/shared-event-record.html", "04-model-3-esc/index.html"),
    ("frameworks/", "05-frameworks/index.html"),
    ("reference/", "07-reference/index.html"),
    ("evidence/", "evidence/index.html"),
    ("development/registers/", "evidence/index.html"),
]
# Anchors that moved from the old Gradient page to the Fluid roster.
ROSTER_ANCHORS = {"body-signals", "situation-signals", "belonging-emotions",
                  "belonging-at-risk", "threat-protection", "survival-rage", "completion"}
ROSTER = "01-signal-map/emotion/fluid.html"

HREF = re.compile(r'(href|src)="([^"]+)"')
MDLINK = re.compile(r'\]\(([^)\s]+)\)')
unmapped: set[str] = set()


# ------------------------------------------------------------- transforms
def gradient_tables(text: str) -> str:
    """Drop the duplicated emotion tables; keep the three-process block."""
    start = text.index('<section class="notes">\n      <h2 id="emotions">')
    keep_from = text.index('<h3 id="signal-access">', start)
    keep_to = text.index('<h3 id="body-signals">', keep_from)
    end = text.index('<section class="return-section"', keep_to)
    kept = text[keep_from:keep_to].rstrip()
    # Links are written as Development Engine paths; the rewrite step maps them.
    replacement = (
        '<section class="notes">\n'
        '      <h2 id="processes">Three processes</h2>\n'
        '      <p class="caption">The emotion tables that used to sit here now live only on the '
        '<a href="../../signal-map/README.md">Emotional Signal Map</a>: the <a href="../../signal-map/fluid.html">Fluid roster</a> '
        'and the <a href="../../signal-map/chronic.html">Chronic roster</a>. The three-process block below stays because the table rows point to it.</p>\n'
        '      ' + kept + '\n    </section>\n\n    '
    )
    text = text[:start] + replacement + text[end:]
    # Internal anchors that now live on the roster or the Signal Map.
    for anchor in ROSTER_ANCHORS:
        text = text.replace(f'href="#{anchor}"', f'href="../../signal-map/fluid.html#{anchor}"')
    text = text.replace('href="#emotions"', 'href="../../signal-map/README.md#emotion-families"')
    # The situation-signals toggle refers to an element that no longer exists.
    text = text.replace("    document.getElementById('fluid-situation-signals').hidden = mode !== 'fluid'\n", "")
    return capacity_echo(text)


CAPACITY_ROWS = {
    "bodily": ["fluid-interoceptive-processing", "chronic-interoceptive-processing", "chronic-me-felt-access"],
    "affective": ["fluid-affective-sharing", "chronic-affective-sharing"],
    "mentalizing": ["fluid-mentalizing", "chronic-mentalizing"],
}
SLIDER_IDS = {"bodily": "access-interoceptive", "affective": "access-affective", "mentalizing": "access-mentalizing"}


def capacity_echo(text: str) -> str:
    """Model 2 stays the territory. Its ME sliders only echo the Model 1 setting;
    the changing reading lives on the Inner Compass view."""
    import json
    style = """
<style>
  /* Capacity controls are set on Model 1; the reading that changes is the Inner Compass. */
  .me-access-slider[disabled] { opacity: .85; cursor: not-allowed; }
  .capacity-echo { margin: 14px 0 0; padding: 12px 16px; background: #edfafd; border: 1px solid #bfeaf0; border-left: 6px solid #10b8cc; border-radius: 10px; font-size: 13px; line-height: 1.5; }
  .capacity-echo strong { color: #0b1f42; }
  .capacity-echo a { color: #076170; font-weight: 700; }
</style>
"""
    script = """
<script src="../../assets/capacities.js"></script>
<script>
  (function () {
    var C = window.TEG && window.TEG.capacities; if (!C) return;
    var SLIDERS = %s, VALUES = [10, 35, 60, 85];
    var CONTROLLER = "../02-model-1-ess-cls-me/me-access.html";
    var COMPASS = "../06-inner-compass-four-modes/compass.html";
    function apply(state) {
      Object.keys(SLIDERS).forEach(function (k) {
        var s = document.getElementById(SLIDERS[k]); if (!s) return;
        s.value = VALUES[state[k]]; s.disabled = true; s.setAttribute("aria-readonly", "true");
      });
      if (typeof updateAccessModel === "function") updateAccessModel();
      var echo = document.getElementById("capacity-echo");
      if (echo) {
        var code = C.code(state);
        echo.innerHTML = "<strong>Set on Model 1.</strong> Current configuration " + code + " · " + C.CONFIGS[code] +
          ". These tables do not change with the setting: they describe the organism's organisation, which is the same whatever ME can read of it. " +
          "The reading that changes is the Inner Compass. " +
          '<a href="' + C.link(COMPASS, state) + '">Open the Compass view →</a> · ' +
          '<a href="' + C.link(CONTROLLER, state) + '">Adjust the capacities on Model 1 →</a>';
      }
    }
    var reveal = document.getElementById("me-access-reveal");
    if (reveal) {
      var echo = document.createElement("div"); echo.id = "capacity-echo"; echo.className = "capacity-echo"; echo.setAttribute("role", "note");
      reveal.parentNode.insertBefore(echo, reveal);
    }
    apply(C.get());
    window.addEventListener("storage", function (e) { if (e.key === "teg.capacities.v1") apply(C.get()); });
  })();
</script>
""" % json.dumps(SLIDER_IDS)
    text = text.replace("</head>", style + "</head>", 1)
    return text.replace("</body>", script + "</body>", 1)


def capacities_sync(text: str) -> str:
    """The carried capacities page reads and writes the shared capacity state."""
    script = """
<script src="../../assets/capacities.js"></script>
<script>
  (function () {
    var C = window.TEG && window.TEG.capacities; if (!C) return;
    var MAP = { interoceptive: "bodily", affective: "affective", mentalizing: "mentalizing" };
    var buttons = Array.prototype.slice.call(document.querySelectorAll(".switch"));
    function fromState(state) {
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", String(state[MAP[b.dataset.capacity]] >= 2)); });
      if (typeof updateField === "function") updateField();
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var partial = {}, on = b.getAttribute("aria-pressed") === "true", current = C.get()[MAP[b.dataset.capacity]];
        partial[MAP[b.dataset.capacity]] = on ? (current >= 2 ? current : 3) : (current < 2 ? current : 0);
        C.set(partial);
      });
    });
    fromState(C.get());
  })();
</script>
"""
    return text.replace("</body>", script + "</body>", 1)


TRANSFORMS = {"gradient_tables": gradient_tables, "capacities_sync": capacities_sync}


# ------------------------------------------------------------ link rewrite
def new_target(old_path: str, anchor: str) -> tuple[str, str]:
    if old_path == "signal-map/README.md":          # the old folder guide → the canon page
        return "01-signal-map/index.html", anchor
    if old_path == "models/01-information-systems/ess-cls-me.html":
        # The canon page keeps the ids #ess, #cls and #me; other anchors are dropped.
        return "02-model-1-ess-cls-me/index.html", (anchor if anchor in {"ess", "cls", "me"} else "")
    if old_path == "models/02-nervous-system-gradient/index.html":
        # The old Gradient page split: emotion anchors went to the roster,
        # everything else to positions.html; a plain link means the canon page.
        if anchor in ROSTER_ANCHORS:
            return ROSTER, anchor
        if anchor == "emotions":                     # the removed emotion tables
            return "01-signal-map/index.html", "emotion-families"
        if anchor:
            return "03-model-2-gradient/positions.html", anchor
        return "03-model-2-gradient/index.html", ""
    if old_path in MOVES:
        target = MOVES[old_path]
        moved_intact = old_path in ENGINE_HOME.values()
        return target, (anchor if moved_intact else "")
    for prefix, target in PREFIXES:
        if old_path.startswith(prefix):
            return target, ""
    unmapped.add(old_path)
    return f"{ENGINE_REL}/{old_path}", anchor


def rewrite(link: str, old_dir: str, new_dir: str) -> str:
    if re.match(r"^[a-z]+:", link) or link.startswith("#") or not link:
        return link
    path, _, anchor = link.partition("#")
    old_path = posixpath.normpath(posixpath.join(old_dir, path))
    if old_path.startswith("../"):
        return link
    target, keep = new_target(old_path, anchor)
    if target.startswith("../"):
        rel = posixpath.join(posixpath.relpath(".", new_dir), target) if new_dir else target
    else:
        rel = posixpath.relpath(target, new_dir) if new_dir else target
    return rel + (f"#{keep}" if keep else "")


def rewrite_links(text: str, suffix: str, old_rel: str, new_rel: str) -> tuple[str, int]:
    old_dir, new_dir = posixpath.dirname(old_rel), posixpath.dirname(new_rel)
    count = 0

    def sub_html(m: re.Match) -> str:
        nonlocal count
        new = rewrite(m.group(2), old_dir, new_dir)
        count += new != m.group(2)
        return f'{m.group(1)}="{new}"'

    def sub_md(m: re.Match) -> str:
        nonlocal count
        new = rewrite(m.group(1), old_dir, new_dir)
        count += new != m.group(1)
        return f"]({new})"

    text = HREF.sub(sub_html, text) if suffix == ".html" else MDLINK.sub(sub_md, text)
    return text, count


# ----------------------------------------------------------------- banner
def add_banner(text: str, banner: tuple[str, str, str, str]) -> str:
    label, body, back, back_name = banner
    html = (f'<div class="carried-banner" role="note"><strong>{label}.</strong> {body} '
            f'<a href="{back}">Back to the {back_name} canon page →</a></div>\n')
    m = re.search(r'<body[^>]*>\s*(<div class="wrap">|<main class="shell">)?\s*', text)
    return text[:m.end()] + html + text[m.end():]


# ------------------------------------------------------------------- main
def source_text(old_rel: str, ref: str | None) -> str:
    if ref is None:
        return (ENGINE / old_rel).read_text(encoding="utf-8")
    return subprocess.run(["git", "-C", str(ENGINE), "show", f"{ref}:{old_rel}"],
                          check=True, capture_output=True, text=True).stdout


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    for new_rel, old_rel, ref, transform, banner in MANIFEST:
        if not new_rel.startswith(only):
            continue
        text = source_text(old_rel, ref)
        if transform:
            text = TRANSFORMS[transform](text)
        text, n = rewrite_links(text, Path(new_rel).suffix, old_rel, new_rel)
        if banner:
            text = add_banner(text, banner)
        out = ROOT / new_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"{n:4d} links  {new_rel}")
    if unmapped:
        print("\nStill pointing into the active Development Engine:")
        for item in sorted(unmapped):
            print(f"  {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
