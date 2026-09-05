# Dark cycle presentation review

Status: integrated locally after parent review on 5 September 2026. Scientific content and approval dates are unchanged.

## Review location

- Branch: `codex/dark-cycle-presentation`.
- Base: local site main `c7a6700` (ME Access Dials consolidation).
- Worktree: `/private/tmp/teg-blue-dark-review/teg-blue-emotional-science-main-structure`.
- Preview: http://127.0.0.1:8876/ . The parent preview on port 8765 is untouched.
- The app-assigned umbrella worktree did not exist. This is a worktree of the canonical **site** repository, not of the umbrella or the Engine.
- The sibling Engine path is a symlink to the canonical Engine. The site preview resolves that mount without writing to it. No Engine files have been edited.
- The design task completed without merging, pushing or publishing. Its worktree is under the temporary directory; the committed branch preserves the handoff. The parent integration is recorded below.

## Design decisions

The reference is `04-model-3-esc/cycle.html`, not its lighter `index.html` sibling.
The shared palette uses cycle navy `#080c13`, surface `#0f1520`, raised surface
`#151d2a`, heading ink `#eef3fb`, body text `#bcc7d8` and muted text `#a2afc3`.
Sans-serif headings use the cycle’s Inter/system stack, with the system font
fallback when Inter is unavailable. Borders separate reading regions; conceptual
colours retain their hues and remain distinct from the neutral surfaces.

Overviews retain a heading and reading hierarchy beside the article. Tables
retain their comparison structure and scroll in a focusable region. Records
retain the source questions and disclosures. Diagrams retain their own spatial
relationships. The dials and Compass retain their controls, four bands and state.
This is a presentation change, not a new public visual grammar for Compass modes.

## Maintenance and carry

`assets/presentation/theme.css` owns the shared tokens and deliberate component
exceptions. `layout.js` gives tables keyboard-accessible scroll regions and a
minimum width based on column count. It does not change their cells or anchors.

`python3 scripts/presentation.py` rebuilds generated overview, shared-component
and per-page CSS adapters and the page inventory. Generated adapters preserve
source layout rules while translating pale surfaces and dark labels. They are
loaded only by active pages. Do not edit generated adapters directly. Original
styles remain available for source comparison; they are not copied from the cycle
into every page. The shared theme loads last. Page-specific styles load only on
their own page, so generic selectors in carried layouts do not leak between pages.

`carry.py` reapplies this presentation after source transfer. The existing
manifest, graduated-file protection and ownership decisions are unchanged.
Importing a non-graduated diagram in the regression test retains its wording and
anchor, attaches the theme and does not graduate its source. Repeated application
is stable. New active HTML pages enter coverage on the next presentation build;
archives, notes/source snapshots and the access bookmark stub remain excluded.
The Gradient table remains active even though its old access anchors redirect.

## Validation

- All 60 HTML files compared with the base: visible source wording, IDs and link
  destinations unchanged. All 13 excluded files byte-identical.
- Generated Signal Map and Gradient data checks pass. Compass regeneration leaves
  its generated data unchanged. Family membership, seven positions and both
  readings are preserved.
- Local links: 164 HTML/Markdown files pass, including this review note.
- Ownership report passes. Engine connections: 173 of 173 connected; targets exist.
- Python regression suite: 11 tests pass (7 existing access tests and 4 presentation
  boundary tests). Both existing JavaScript access/state suites pass, including
  15 compatibility cases.
- Browser audit: every active page at 1440 × 1000 and 390 × 1000. No JavaScript
  exceptions, page-level horizontal overflow or detected text-contrast failures
  in the final default-state audit. Dense tables scroll inside their region.
- Browser interactions pass at both widths: Model 2 dropdown by keyboard, Tab,
  Escape, destination, forward/back; incoming dial state, keyboard range edits,
  four bands, eight configuration records, Compass round trip, mixed/unknown
  reading, reset; position/reading deep link and disclosure operation.
- Reduced-motion mode disables the Compass marker transition.
- Actual screenshots inspected for overview, table, record and interactive page
  types at desktop and mobile sizes. The mobile table inspection caught narrow
  columns missed by overflow detection; column-count-based minimum widths fix it.

`browser-audit.json` and `interactions.json` hold the per-page and interaction
results. `screenshots/` includes entry views and content views. The contrast check
composites solid/alpha ancestor backgrounds and uses 4.5:1 normal-text and 3:1
large-text thresholds. It does not certify every gradient pixel, hover state,
SVG label or assistive-technology combination. Screenshots supplement that check.
Verification used Chromium through bundled Playwright; the agent-browser CLI was
unavailable. Safari and Firefox were not tested.

Reproduce browser checks with a local preview running, Playwright available to
Node, and optionally `CHROMIUM_EXECUTABLE` and `PLAYWRIGHT_MODULE` set to installed
paths. Run `node scripts/audit-presentation.cjs` and
`node scripts/check-presentation-interactions.cjs`. `PREVIEW_URL` defaults to the
separate review port 8876. These commands open isolated temporary browser profiles.

## Page coverage

| Page | Treatment / reason |
| --- | --- |
| `00-emotions-as-information/index.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/emotion/chronic.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/emotion/fluid.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/grounding/neurochemistry.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/grounding/recruitment-persistence-and-recovery.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/index.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/map.html` | Shared dark presentation; desktop/mobile audited |
| `01-signal-map/notes/sources/chronic-emotional-signals-collection.html` | Historical archive / source snapshot; unchanged |
| `02-model-1-ess-cls-me/access.html` | Compatibility bookmark route; unchanged |
| `02-model-1-ess-cls-me/index.html` | Shared dark presentation; desktop/mobile audited |
| `02-model-1-ess-cls-me/me-access.html` | Shared dark presentation; desktop/mobile audited |
| `02-model-1-ess-cls-me/notes/sources/relational-capacities.html` | Historical archive / source snapshot; unchanged |
| `02-model-1-ess-cls-me/processing.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/autonomic.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/depth.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/fluid-chronic.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/index.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/intermediate-layers.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/notes/sources/regulation-and-return-workbench.html` | Historical archive / source snapshot; unchanged |
| `03-model-2-gradient/position.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/positions.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/premise.html` | Shared dark presentation; desktop/mobile audited |
| `03-model-2-gradient/return.html` | Shared dark presentation; desktop/mobile audited |
| `04-model-3-esc/cycle.html` | Shared dark presentation; desktop/mobile audited |
| `04-model-3-esc/index.html` | Shared dark presentation; desktop/mobile audited |
| `04-model-3-esc/notes/sources/esc-and-escalation-pathways-archive.html` | Historical archive / source snapshot; unchanged |
| `04-model-3-esc/shared-event-record.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F01/crosswalk.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F01/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F01/timeline.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F02/diagram.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F02/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F03/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F04/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F05/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F06/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F07/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F08/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F09/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F10/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F11/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/F12/index.html` | Shared dark presentation; desktop/mobile audited |
| `05-frameworks/index.html` | Shared dark presentation; desktop/mobile audited |
| `06-inner-compass-four-modes/compass.html` | Shared dark presentation; desktop/mobile audited |
| `06-inner-compass-four-modes/index.html` | Shared dark presentation; desktop/mobile audited |
| `07-reference/behaviour.html` | Shared dark presentation; desktop/mobile audited |
| `07-reference/index.html` | Shared dark presentation; desktop/mobile audited |
| `07-reference/sociality.html` | Shared dark presentation; desktop/mobile audited |
| `archive/pre-numbered-main-structure-2026-09-04/emotional-signal-map.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/emotions-as-information.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/index.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/inner-compass-four-mode-gradient.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/model-1-two-biological-information-systems-and-me.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/model-2-nervous-system-organisation-gradient.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/model-3-emotional-somatic-cycle.html` | Historical archive / source snapshot; unchanged |
| `archive/pre-numbered-main-structure-2026-09-04/twelve-frameworks-map.html` | Historical archive / source snapshot; unchanged |
| `evidence/index.html` | Shared dark presentation; desktop/mobile audited |
| `evidence/protocol.html` | Shared dark presentation; desktop/mobile audited |
| `foundations/index.html` | Shared dark presentation; desktop/mobile audited |
| `index.html` | Shared dark presentation; desktop/mobile audited |


## Parent review and local integration

On 5 September 2026, the parent task reviewed design commit `e6a5ac8` against
its base `c7a6700` and fast-forwarded the clean local site `main` to that commit.
There were no conflicts or unrelated working changes. The canonical preview
at `http://localhost:8765/` now serves the same presentation as the review preview.
The Development Engine was not changed. No push or publication occurred.

Independent checks passed: local links (164 HTML/Markdown files), generated
Signal Map and Gradient records, 173 Engine connections, all 16 ownership
entries, 11 Python regression tests, both JavaScript access/state suites and
Git whitespace checks. A separate HTML comparison found no changes in visible
source text, section IDs or link destinations across all 60 pre-existing pages.

The parent inspected the Model 1 overview on desktop and the Gradient table and
ME Access Dials at 390 pixels. The page width remained 390 pixels while the
Gradient table retained readable columns in its scroll region. Keyboard operation
opened the Model 2 menu and followed the table link. Independent dial edits from
incoming values 1/2/3 remained 0/0/3 and arrived correctly in the Inner Compass.
No browser console errors were recorded in these checks. The full design-task
browser audit and its stated limits above remain part of the review record.
