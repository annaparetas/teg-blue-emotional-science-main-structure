#!/usr/bin/env python3
"""Extract the signal records the map view shows from the Signal Map's own pages.

Reads the canon page (family definitions), the Fluid roster (Body Signal table,
four Emotion family tables, the illustrative foregrounding row), the Chronic
roster (four family matrices, the proposed additional experiences) and the
neurochemistry grounding page (entry ids and evidence status), and writes them
as one data file, 01-signal-map/data/signals.js. The map view reads that file,
so every card is the rosters' own words. Re-run after editing any roster.

Nothing here decides membership. The five Body-condition families and their
members are read from the canon page's family table; the four Emotion families
and their members come from the roster tables themselves.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "01-signal-map"
CANON = FOLDER / "index.html"
FLUID = FOLDER / "emotion" / "fluid.html"
CHRONIC = FOLDER / "emotion" / "chronic.html"
NEURO = FOLDER / "grounding" / "neurochemistry.html"
TARGET = FOLDER / "data" / "signals.js"

POSITIONS = ["X", "A", "A↔B", "B", "C", "D", "Z"]
STRIP_SPANS = ("cell-hooks", "column-scope", "swatch", "review-status")


# ------------------------------------------------------------ html helpers
def clean(fragment: str) -> str:
    for cls in STRIP_SPANS:
        fragment = re.sub(rf'<span class="{cls}"[^>]*>.*?</span>', "", fragment, flags=re.S)
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def table_after(text: str, anchor: str) -> str:
    """The first <table> that follows the element carrying id="anchor"."""
    start = text.index(f'id="{anchor}"')
    open_ = text.index("<table", start)
    close = text.index("</table>", open_)
    return text[open_:close]


def rows(table: str) -> list[list[str]]:
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table, flags=re.S):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.S)
        out.append([clean(c) for c in cells])
    return out


def body_rows(table: str) -> list[list[str]]:
    tbody = table[table.index("<tbody"):]
    return [r for r in rows(tbody) if r]


# --------------------------------------------------------------- readers
def read_families() -> tuple[list[dict], list[dict]]:
    text = CANON.read_text(encoding="utf-8")
    body = []
    for tr in re.findall(r'<tr id="([a-z-]+)-family">(.*?)</tr>', text, flags=re.S):
        cells = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr[1], flags=re.S)]
        body.append({"id": tr[0], "name": cells[0], "problem": cells[1], "access": cells[2], "status": cells[3],
                     "canon": f"index.html#{tr[0]}"})
    emotion = []
    tbl = table_after(text, "emotion-families") if 'id="emotion-families"' in text else text
    for tr in re.findall(r'<tr id="(belonging|belonging-at-risk|threat-protection|survival-rage)">(.*?)</tr>', tbl, flags=re.S):
        cells = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr[1], flags=re.S)]
        emotion.append({"id": tr[0], "name": cells[0], "relationship": cells[1], "members_text": cells[2], "status": cells[3],
                        "canon": f"index.html#{tr[0]}"})
    return body, emotion


def read_fluid() -> dict:
    text = FLUID.read_text(encoding="utf-8")
    out: dict = {"body": [], "emotion": {}, "association": {}}

    for r in body_rows(table_after(text, "body-signals")):
        name, function, body, condition, needs = r[:5]
        out["body"].append({"name": name, "function": function, "body": body, "condition": condition, "completing": needs})

    for fam, anchor in (("belonging", "belonging-emotions"), ("belonging-at-risk", "belonging-at-risk"),
                        ("threat-protection", "threat-protection"), ("survival-rage", "survival-rage")):
        recs = []
        for r in body_rows(table_after(text, anchor)):
            name, function, body, condition, example, needs, carry = r[:7]
            recs.append({"name": name, "function": function, "body": body, "condition": condition,
                         "example": example, "completing": needs, "carryover": carry})
        out["emotion"][fam] = recs

    # Characteristic Fluid association, from the family table in the Situation Signals section.
    for r in body_rows(table_after(text, "situation-signals")):
        if len(r) >= 4:
            out["association"][slug(r[0].replace(" Emotions", ""))] = {"association": r[2], "function": r[3]}

    return out


def read_chronic() -> dict:
    text = CHRONIC.read_text(encoding="utf-8")
    out: dict = {"profiles": {}, "emotion": {}, "additional": []}
    first = table_after(text, "belonging-emotions")
    for letter, sub in re.findall(r'<th scope="col" class="pos">(.*?)<span class="pos-sub">(.*?)</span>', first):
        out["profiles"][clean(letter)] = clean(sub)
    for fam, anchor in (("belonging", "belonging-emotions"), ("belonging-at-risk", "belonging-at-risk"),
                        ("threat-protection", "threat-protection"), ("survival-rage", "survival-rage")):
        cells = {}
        for r in body_rows(table_after(text, anchor)):
            if len(r) == 8:
                cells[slug(r[0])] = dict(zip(POSITIONS, r[1:]))
        out["emotion"][fam] = cells
    for r in body_rows(table_after(text, "distorted-signals")):
        if len(r) >= 4:
            out["additional"].append({"name": r[0], "related": r[1], "hypothesis": r[2], "earlier": r[3]})
    # The Body Signal note under the Survival-Rage table.
    m = re.search(r"</table>\s*</div>\s*<p class=\"aside\">(.*?)</p>", text[text.index('id="survival-rage"'):], flags=re.S)
    out["body_note"] = clean(m.group(1)) if m else ""
    return out


def read_neuro() -> dict:
    text = NEURO.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<article class="entry" id="([a-z-]+)">(.*?)</article>', text, flags=re.S):
        status = re.search(r'<p class="status">(.*?)</p>', m.group(2), flags=re.S)
        fields = {clean(k): clean(v) for k, v in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", m.group(2), flags=re.S)}
        out[m.group(1)] = {"status": clean(status.group(1)) if status else "", "fields": fields}
    return out


# ------------------------------------------------------------------ build
def main() -> int:
    body_fams, emo_fams = read_families()
    fluid, chronic, neuro = read_fluid(), read_chronic(), read_neuro()

    body_by_slug = {slug(r["name"]): r for r in fluid["body"]}
    # Members are read from the canon table's "Current mapped access" cell.
    ALIAS = {"need-to-urinate": "needing-to-urinate", "need-to-empty-the-bowels": "needing-to-empty-the-bowels"}
    groups = [{"id": "body", "name": "Body-condition signals", "question": "What internal condition is the organism regulating?",
               "families": []},
              {"id": "emotion", "name": "Emotion signals", "question": "What does this present or represented condition mean for the organism?",
               "families": []}]
    used = set()
    for fam in body_fams:
        members = []
        for part in re.split(r",\s*|\s+and\s+", fam["access"].lower()):
            s = ALIAS.get(slug(part), slug(part))
            if s in body_by_slug:
                members.append(s); used.add(s)
        groups[0]["families"].append({**fam, "members": members})
    missing = set(body_by_slug) - used
    if missing:
        raise SystemExit(f"Body signals not placed in a family: {sorted(missing)}")

    signals = {}
    for s, r in body_by_slug.items():
        signals[s] = {"id": s, "name": r["name"], "group": "body", "fluid": r, "chronic": None,
                      "grounding": f"grounding/neurochemistry.html#{s}", "grounding_status": neuro.get(s, {}).get("status", "")}
    for fam in emo_fams:
        members = []
        for r in fluid["emotion"][fam["id"]]:
            s = slug(r["name"]); members.append(s)
            signals[s] = {"id": s, "name": r["name"], "group": "emotion", "family": fam["id"], "fluid": r,
                          "chronic": chronic["emotion"][fam["id"]].get(s),
                          "grounding": f"grounding/neurochemistry.html#{s}", "grounding_status": neuro.get(s, {}).get("status", "")}
        assoc = fluid["association"].get(fam["id"], {})
        groups[1]["families"].append({**fam, "members": members, "association": assoc.get("association", ""),
                                      "survival_function": assoc.get("function", "")})
    for fam in groups[0]["families"]:
        for s in fam["members"]:
            signals[s]["family"] = fam["id"]

    for s, rec in signals.items():
        if rec["group"] == "emotion" and not rec["chronic"]:
            raise SystemExit(f"No Chronic reading found for {s}")
        if s not in neuro:
            raise SystemExit(f"No neurochemistry entry for {s}")

    for sid, rec in signals.items():
        f = rec["fluid"]
        biology = neuro[sid]["fields"]
        fluid_link = f"emotion/fluid.html#signal-{sid}"
        biology_link = rec["grounding"]
        rec["questions"] = [
            {"question": "What does it register?", "answer": f["condition"], "status": "Working functional reading", "source": fluid_link},
            {"question": "What is its function?", "answer": f["function"], "status": "Working functional reading", "source": fluid_link},
            {"question": "What does it change?", "answer": f["function"], "status": "Current functional description; separate accounts of attention, bodily activity and action-readiness still need review", "source": fluid_link},
            {"question": "How might it become felt?", "answer": f["body"], "status": "Possible experience, not a required sign", "source": fluid_link},
            {"question": "What regulates its participation?", "answer": biology.get("What may raise priority", "An emotion-specific account of recruitment, persistence, reduction and redirection has not yet been separated in this record. The linked biological material is working grounding, not a complete regulation mechanism."), "status": "Partial account" if "What may raise priority" in biology else "Separate account still needed", "source": biology_link},
            {"question": "What allows updating?", "answer": f["completing"], "status": "Possible completing condition; relief, recovery and repair remain separate", "source": fluid_link},
            {"question": "What differs under Fluid and Chronic organisation?", "answer": "Compare the same signal in the two readings below. The Chronic profiles describe possible differences in access, interpretation and participation; they do not change its identity." if rec["chronic"] else chronic["body_note"], "status": "Working comparison" if rec["chronic"] else "No individual Chronic record", "source": f"emotion/chronic.html#signal-{sid}" if rec["chronic"] else "emotion/chronic.html#top"},
            {"question": "What supports the explanation?", "answer": biology.get("Evidence status", biology.get("Evidence carried forward", "Evidence review remains open.")) + " " + biology.get("Context and limits", ""), "status": rec["grounding_status"], "source": biology_link},
        ]
        rec["biology_fields"] = biology

    data = {
        "positions": POSITIONS,
        "chronic_profiles": chronic["profiles"],
        "body_chronic_note": chronic["body_note"],
        "groups": groups,
        "signals": signals,
        "additional": chronic["additional"],
        "sources": {"canon": "index.html", "fluid": "emotion/fluid.html", "chronic": "emotion/chronic.html",
                    "neurochemistry": "grounding/neurochemistry.html"},
    }
    output = ("/* Generated by scripts/build-signal-map-data.py from the Signal Map's own pages. Do not edit. */\n"
              "window.TEG_SIGNALS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    record_lines = ["# Signal records", "", "Generated from the site’s Fluid, Chronic and biological records. Do not edit this file directly.", "", "Status: working synthesis and explicitly identified gaps. A complete set of questions is not a completed evidence review.", "", "Read [the session guide](SESSION-GUIDE.md) before using these records. [Open the interactive map](map.html).", ""]
    for sid, rec in signals.items():
        record_lines += [f'<a id="{sid}"></a>', f'## {rec["name"]}', "", f'Group: {rec["group"]}. Family: {rec["family"]}.', "", f'[Interactive record](map.html#{sid}) · [Fluid reading](emotion/fluid.html#signal-{sid}) · [Biology and Neurochemistry]({rec["grounding"]})', ""]
        if sid == "love":
            record_lines += ["### Deeper working analysis", "", "Love also has an emotion-specific nine-layer working package. Its evidence placeholders remain unresolved; do not transfer its answers to another emotion.", "", "[Fluid analysis](notes/fluid-love-nine-layer-signal-structure.md) · [Chronic analysis](notes/chronic-love-nine-layer-signal-structure.md) · [Comparison and owner handoff](notes/fluid-chronic-love-nine-layer-comparison-and-owner-handoff.md) · [Completion and public boundary](notes/love-reference-case-completion-and-public-boundary.md)", ""]
        for q in rec["questions"]:
            record_lines += [f'### {q["question"]}', "", q["answer"], "", f'Status: {q["status"]}. [Source]({q["source"]}).', ""]
        record_lines += ["### Biological participation in the current grounding", ""]
        for label, value in rec["biology_fields"].items():
            record_lines += [f'**{label}:** {value}', ""]
        if rec["chronic"]:
            record_lines += ["### Chronic reference profiles", "", "These are working possibilities, not person types or a scale of severity.", ""]
            for position in POSITIONS:
                record_lines += [f'**{position}:** {rec["chronic"][position]}', ""]
        if rec["fluid"].get("example"):
            record_lines += ["### Fluid example", "", rec["fluid"]["example"], ""]
        if rec["fluid"].get("carryover"):
            record_lines += ["### Possible carryover", "", rec["fluid"]["carryover"], ""]
    record_output = "\n".join(record_lines)
    record_target = FOLDER / "signal-records.md"
    n_body = len(body_by_slug); n_emo = len(signals) - n_body
    if "--check" in sys.argv[1:]:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != output or not record_target.exists() or record_target.read_text(encoding="utf-8") != record_output:
            print(f"Generated data is stale: run scripts/build-signal-map-data.py to update {TARGET.relative_to(ROOT)}")
            return 1
        print(f"Generated data is current: {n_body} Body-condition signals, {n_emo} Emotion signals, {len(data['additional'])} additional experiences")
        return 0
    unknown = [arg for arg in sys.argv[1:] if arg != "--check"]
    if unknown:
        print("Usage: python3 scripts/build-signal-map-data.py [--check]", file=sys.stderr)
        return 2
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(output, encoding="utf-8")
    record_target.write_text(record_output, encoding="utf-8")
    print(f"{n_body} Body-condition signals, {n_emo} Emotion signals, {len(data['additional'])} additional experiences → {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
