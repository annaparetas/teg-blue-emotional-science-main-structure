#!/usr/bin/env python3
"""Build and validate the non-destructive Development Engine connection map."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT.parent / "inner-compass-nervous-system-organization-gradient"
OUTPUT = ROOT / "ENGINE-CONNECTIONS.md"
CARRY_PATH = ROOT / "scripts" / "carry.py"


def load_carry_module():
    spec = importlib.util.spec_from_file_location("site_carry", CARRY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {CARRY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Files that do not already appear in carry.py's relationship data. Keeping
# this list explicit means that a new Engine file makes --check fail until its
# site relationship has been considered.
#
# Each value is: (site targets, relationship statement).
# An empty target tuple means repository inventory rather than a content home.
EXTRA_RELATIONSHIPS: dict[str, tuple[tuple[str, ...], str]] = {
    'development/decisions/me-access-dials-consolidation.md': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Approved cross-repository access consolidation; records current ownership and the bounded implementation.'),
    'development/audits/me-access-dials/README.md': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Historical pre-implementation audit approved for consolidation; current ownership is in the dated decision.'),
    'development/audits/me-access-dials/file-inventory.csv': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Historical full-file disposition inventory supporting the approved consolidation.'),
    'development/audits/me-access-dials/link-rewiring.csv': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Historical link review plan; current links and compatibility routes implement the decision.'),
    'development/audits/me-access-dials/path-references.csv': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Historical raw path reference audit including ownership prose and migration code.'),
    'development/audits/me-access-dials/audit-metrics.json': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Counts for the historical pre-implementation access audit.'),
    'models/01-information-systems/coordinated-conscious-access.html': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Retired page body; compatibility route to the dials or Model 3 according to the requested section.'),
    'models/01-information-systems/relational-capacities.html': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Retired configuration controller; compatibility route to the current ME Access Dials. Historical source is fixed in the carry manifest.'),
    'models/01-information-systems/inner-compass-sequence.html': (("02-model-1-ess-cls-me/notes/access-consolidation.md", "02-model-1-ess-cls-me/me-access.html"), 'Compatibility route to the complete Model 3 event sequence.'),

    ".gitignore": (("README.md",), "Repository-support connection; each repository keeps its own ignore rules."),
    "AGENTS.md": (("README.md", "STATUS.md"), "Repository-governance connection; the Engine keeps its own working rules."),
    "CONTENT-MANIFEST.md": (("README.md", "STATUS.md"), "Repository-navigation connection; the Engine manifest continues to govern Engine ownership and reading routes."),
    "archive/outdated-references/EMOTIONS-TABLES-AND-EXPLANATIONS.md": (("01-signal-map/index.html",), "Existing Engine archive connection to the Emotional Signal Map; its Engine location and status do not change."),
    "archive/session-handovers/UPDATE-NOTE-RETURN-AND-SURVIVAL-PROBLEM.md": (("03-model-2-gradient/return.html", "07-reference/index.html"), "Existing Engine archive connection to Return and survival interpretation; its Engine location and status do not change."),
    "assets/emotions-across-the-gradient@4x.png": (("01-signal-map/index.html", "03-model-2-gradient/fluid-chronic.html"), "Engine visual-asset connection to emotional signals across Fluid and Chronic organisation."),
    "development/README.md": (("README.md", "STATUS.md"), "Repository-governance connection between the Engine development workspace and the site's ownership boundary."),
    "development/architecture-naming-propagation-ledger.md": (("GLOSSARY.md", "README.md"), "Architecture and naming connection; the Engine ledger remains the detailed propagation record."),
    "development/interim-session-git-protocol.md": (("STATUS.md",), "Repository-governance connection; the protocol governs Engine work, not site Git practice."),
    "development/model-notes/interaction-ideas.md": (("02-model-1-ess-cls-me/me-access.html", "03-model-2-gradient/index.html", "06-inner-compass-four-modes/compass.html"), "Historical interaction-design proposal, implemented in ME Access Dials; retained for provenance rather than as a request for another controller."),
    "development/model-notes/what-a-behaviour-costs.md": (("03-model-2-gradient/index.html", "07-reference/behaviour.html"), "Working conceptual connection between Gradient organisation and observable behaviour, impact and responsibility."),
    "emotions-as-information.html": (("00-emotions-as-information/index.html",), "Concept connection to the site's Emotions as Information page; the Engine file remains intact."),
    "frameworks/diagrams/.gitignore": (("05-frameworks/index.html",), "Engine diagram-workspace support connected to the Frameworks area; the ignore rule remains Engine-local."),
    "frameworks/diagrams/F1-Evolution/F1-evolution.html": (("05-frameworks/F01/index.html",), "Working F01 diagram connection; the full visual development file remains in the Engine."),
    "frameworks/diagrams/F1-Evolution/F1-evolution.md": (("05-frameworks/F01/index.html",), "Working F01 diagram-source connection; the source remains in the Engine."),
    "frameworks/diagrams/F1-Evolution/working-panels/panel-01-evolutionary-gradient.md": (("05-frameworks/F01/index.html",), "Working-panel connection to F01's evolutionary gradient."),
    "frameworks/diagrams/F1-Evolution/working-panels/panel-02-restorative-foundation.md": (("05-frameworks/F01/index.html",), "Working-panel connection to F01's restorative foundation."),
    "frameworks/diagrams/F1-Evolution/working-panels/panel-03-defensive-repertoire.md": (("05-frameworks/F01/index.html",), "Working-panel connection to F01's defensive repertoire."),
    "frameworks/diagrams/F1-Evolution/working-panels/panel-04-regulation-through-relationship.md": (("05-frameworks/F01/index.html",), "Working-panel connection to F01's regulation-through-relationship account."),
    "frameworks/diagrams/F1-Evolution/working-panels/panel-b-working.md": (("05-frameworks/F01/index.html",), "Working-panel connection to F01 visual development."),
    "frameworks/diagrams/F1/F1-diagram.html": (("05-frameworks/F01/index.html",), "Working F01 visual connection; the diagram remains in the Engine."),
    "frameworks/diagrams/F1/F1-origins-owed.md": (("05-frameworks/F01/index.html",), "F01 origins and attribution connection; the detailed record remains in the Engine."),
    "frameworks/diagrams/F1/F1-panel-D1-parked.html": (("05-frameworks/F01/index.html",), "Parked Engine panel connected to F01; this map does not change its Engine status."),
    "frameworks/diagrams/F1/F1-panel-E-parked.html": (("05-frameworks/F01/index.html",), "Parked Engine panel connected to F01; this map does not change its Engine status."),
    "frameworks/diagrams/F1/F1-panels.md": (("05-frameworks/F01/index.html",), "F01 panel-plan connection; the working plan remains in the Engine."),
    "frameworks/diagrams/F1/F1-scientific-grounding.html": (("05-frameworks/F01/index.html", "evidence/index.html"), "F01 grounding connection across the framework and evidence areas."),
    "frameworks/diagrams/F1/F1-state-profiles.html": (("05-frameworks/F01/index.html", "03-model-2-gradient/index.html"), "Working connection between F01 state profiles and Gradient organisation."),
    "frameworks/diagrams/F1/F1.html": (("05-frameworks/F01/index.html",), "Working F01 diagram connection; the full Engine version remains intact."),
    "frameworks/diagrams/README.md": (("05-frameworks/index.html",), "Framework visual-library connection; the Engine remains the home of diagram development and history."),
    "frameworks/diagrams/originals/00 - The Emotional MetaMap of TEG-Blue.png": (("index.html", "05-frameworks/index.html"), "Original whole-architecture artwork connected to the site spine and Frameworks map."),
    "frameworks/diagrams/originals/01-F1 - Map 1 — The Emotional Gradient — Public in general Diagram Edition.png": (("05-frameworks/F01/index.html",), "Original Map 1 artwork connected to F01."),
    "frameworks/diagrams/originals/02-F2 - Map 2 — The Ego Persona Construct.png": (("05-frameworks/F02/index.html",), "Original Map 2 artwork connected to F02."),
    "frameworks/diagrams/originals/02-Map 2 part 2.png": (("05-frameworks/F02/index.html",), "Original Map 2 continuation connected to F02."),
    "frameworks/diagrams/originals/03-F3 - Map 3 — The Three Inner Layers.png": (("05-frameworks/F03/index.html",), "Original Map 3 artwork connected to F03."),
    "frameworks/diagrams/originals/04-F7 - Map 7 — From Defense to Oppression.png": (("05-frameworks/F07/index.html", "07-reference/index.html"), "Original Map 7 artwork connected to F07 and the shared responsibility reference."),
    "frameworks/diagrams/originals/05-The 4-Mode Gradient of TEG-Blue.png": (("06-inner-compass-four-modes/index.html",), "Original 4-Mode Gradient artwork connected to the Inner Compass area."),
    "frameworks/diagrams/originals/06-full-break-down.png": (("06-inner-compass-four-modes/index.html",), "Original Four Modes full-breakdown artwork connected to the Inner Compass area."),
    "frameworks/diagrams/originals/07-emotions.png": (("00-emotions-as-information/index.html", "01-signal-map/index.html"), "Original emotion glyph library connected to Emotions as Information and the Emotional Signal Map."),
    "frameworks/diagrams/originals/08 - The Emotional Circuit Board R.png": (("index.html", "05-frameworks/index.html"), "Original architecture-wiring artwork connected to the site spine and Frameworks map."),
    "frameworks/diagrams/originals/README.md": (("05-frameworks/index.html",), "Original-artwork register connected to the Frameworks map; provenance remains in the Engine."),
    "inner-compass-project-map.html": (("README.md", "STATUS.md"), "Compatibility redirect within the Engine, connected to the site's repository relationship controls."),
    "models/01-information-systems/ess-cls-me.html": (("02-model-1-ess-cls-me/index.html",), "Model 1 concept connection; the Engine owner page remains intact."),
    "models/01-information-systems/source-documents/sensory-processing.docx": (("02-model-1-ess-cls-me/processing.html",), "Model 1 source-document connection to sensory processing; the source document remains in the Engine."),
    "models/README.md": (("02-model-1-ess-cls-me/index.html", "03-model-2-gradient/index.html", "04-model-3-esc/index.html"), "Model-boundary connection to the site's three separate model areas."),
    "scripts/check-local-links.py": (("scripts/check-local-links.py",), "Parallel repository-support connection; each repository checks its own local links."),
    "scripts/migrations/2026-08-22-reorganise-repository.py": (("README.md", "STATUS.md"), "Engine repository-history connection; the migration script remains in the Engine and is not a site operation."),
    "signal-map/README.md": (("01-signal-map/index.html",), "Signal Map navigation connection; the Engine README remains the research-layer route."),
}


def engine_files() -> list[str]:
    if not ENGINE.is_dir():
        raise RuntimeError(f"Development Engine not found: {ENGINE}")
    # Git's content inventory is stable across worktrees and ignores OS metadata.
    result = subprocess.run(
        ["git", "-C", str(ENGINE), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True, capture_output=True, text=True,
    )
    return sorted({path for path in result.stdout.split("\0") if path})



def site_link(target: str) -> str:
    label = f"`{target}`"
    href = quote(target, safe="/-._~")
    return f"[{label}]({href})"


def area_for(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else "Repository root"


def relationships(files: list[str]):
    carry = load_carry_module()
    manifest_targets = {old: new for new, old, *_ in carry.MANIFEST}
    rows = {}

    for source, target in carry.MOVES.items():
        if source not in files:
            continue
        if source in manifest_targets:
            if target in carry.GRADUATED_SITE_FILES:
                kind = "Site-owned presentation with Engine provenance"
                statement = (
                    "The site presentation has its own reviewed ownership; the Engine file "
                    "continues as the research and provenance source. Later Engine work crosses only by review."
                )
            else:
                kind = "Reviewed carry relationship"
                statement = (
                    "The Engine file remains the source; the site file is the reviewed, navigable snapshot "
                    "named in the carry manifest."
                )
        else:
            kind = "Documented concept connection"
            statement = (
                "The Engine file remains in place; the site target is the related curated concept or control."
            )
        rows[source] = ((target,), statement, kind)

    for source, (targets, statement) in EXTRA_RELATIONSHIPS.items():
        rows[source] = (targets, statement, "Additional explicit connection")

    return rows


def validate_inventory(files: list[str], rows) -> list[str]:
    problems = []
    file_set = set(files)
    row_set = set(rows)
    for path in sorted(file_set - row_set):
        problems.append(f"Engine file has no reviewed connection: {path}")
    for path in sorted(row_set - file_set):
        problems.append(f"Connection points to an Engine file that is not present: {path}")

    for source in sorted(file_set & row_set):
        targets, _, _ = rows[source]
        for target in targets:
            if not (ROOT / target).exists():
                problems.append(f"Site target does not exist for {source}: {target}")
    return problems


def render(files: list[str], rows) -> str:
    counts = Counter(rows[path][2] for path in files)
    lines = [
        "# Development Engine connection map",
        "",
        "This is a relationship map, not a migration plan. It records how every current file in the sibling `inner-compass-nervous-system-organization-gradient/` Development Engine relates to this navigable site.",
        "",
        "## Preservation rule",
        "",
        "- Each row records a current Engine file and its declared relationship. The approved access consolidation is recorded explicitly for retired interfaces; this map does not itself change content or status.",
        "- A site connection identifies the related concept or repository control. It does not authorise moving, deleting, renaming, replacing, hiding, archiving or reclassifying the Engine file.",
        "- The Engine's `CONTENT-MANIFEST.md` and `project-map.html` continue to govern Engine ownership and reading routes. This document assigns no new content status.",
        "- A reviewed carry is a specific existing transfer relationship. Other rows are conceptual or repository-support connections only; no file transfer is implied.",
        "",
        "## Coverage",
        "",
        f"- **{len(files)} Engine files listed: {len(files)} of {len(files)}.**",
        f"- {counts['Reviewed carry relationship']} reviewed carry relationships.",
        f"- {counts['Site-owned presentation with Engine provenance']} site-owned presentations with continuing Engine provenance.",
        f"- {counts['Documented concept connection']} documented concept connections already present in the site transfer logic.",
        f"- {counts['Additional explicit connection']} additional explicit concept, visual, archive or repository-support connections.",
        "",
        "The count includes tracked content and untracked non-ignored content, including repository guidance such as `.gitignore`. Ignored macOS metadata and Git internals are excluded, making the inventory stable across worktrees.",
        "",
        "Run `python3 scripts/build-engine-connections.py --check` after either repository changes. A new, removed or renamed Engine file, a missing site target, or an out-of-date generated map makes the check fail.",
        "",
    ]

    grouped: dict[str, list[str]] = {}
    for source in files:
        grouped.setdefault(area_for(source), []).append(source)

    areas = sorted(grouped, key=lambda area: (area != "Repository root", area))
    for area in areas:
        heading = "Repository root" if area == "Repository root" else f"`{area}/`"
        lines.extend([
            f"## {heading}",
            "",
            "| Engine file | Site connection | Relationship |",
            "| --- | --- | --- |",
        ])
        for source in grouped[area]:
            targets, statement, kind = rows[source]
            site = "Repository inventory only" if not targets else "<br>".join(site_link(target) for target in targets)
            lines.append(f"| `{source}` | {site} | **{kind}.** {statement} |")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the generated Markdown map")
    parser.add_argument("--check", action="store_true", help="validate inventory, targets and generated output")
    args = parser.parse_args()
    if args.write == args.check:
        parser.error("choose exactly one of --write or --check")

    files = engine_files()
    rows = relationships(files)
    problems = validate_inventory(files, rows)
    if problems:
        print("Development Engine connection map cannot be built:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    expected = render(files, rows)
    if args.write:
        OUTPUT.write_text(expected, encoding="utf-8")
        print(f"Wrote {OUTPUT.name}: {len(files)} of {len(files)} Engine files connected.")
        return 0

    if not OUTPUT.exists():
        print(f"Missing generated map: {OUTPUT.name}")
        return 1
    if OUTPUT.read_text(encoding="utf-8") != expected:
        print(f"{OUTPUT.name} is out of date. Run: python3 scripts/build-engine-connections.py --write")
        return 1
    print(f"Checked {OUTPUT.name}: {len(files)} of {len(files)} Engine files connected; all site targets exist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
