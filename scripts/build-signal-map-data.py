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
    out: dict = {"body": [], "emotion": {}, "association": {}, "foregrounding": {}}

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

    # Illustrative foregrounding by Position: the Emotions row of the Fluid Gradient table.
    grad = table_after(text, "fluid-emotions")
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", grad, flags=re.S):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.S)
        if cells and clean(cells[0]).startswith("Emotion"):
            vals = [clean(c) for c in cells[1:]]
            if len(vals) == 7:
                out["foregrounding"] = dict(zip(POSITIONS, vals))
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
        out[m.group(1)] = clean(status.group(1)) if status else ""
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
                      "grounding": f"grounding/neurochemistry.html#{s}", "grounding_status": neuro.get(s, "")}
    for fam in emo_fams:
        members = []
        for r in fluid["emotion"][fam["id"]]:
            s = slug(r["name"]); members.append(s)
            signals[s] = {"id": s, "name": r["name"], "group": "emotion", "family": fam["id"], "fluid": r,
                          "chronic": chronic["emotion"][fam["id"]].get(s),
                          "grounding": f"grounding/neurochemistry.html#{s}", "grounding_status": neuro.get(s, "")}
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

    data = {
        "positions": POSITIONS,
        "chronic_profiles": chronic["profiles"],
        "foregrounding": fluid["foregrounding"],
        "body_chronic_note": chronic["body_note"],
        "groups": groups,
        "signals": signals,
        "additional": chronic["additional"],
        "sources": {"canon": "index.html", "fluid": "emotion/fluid.html", "chronic": "emotion/chronic.html",
                    "neurochemistry": "grounding/neurochemistry.html"},
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text("/* Generated by scripts/build-signal-map-data.py from the Signal Map's own pages. Do not edit. */\n"
                      "window.TEG_SIGNALS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    n_body = len(body_by_slug); n_emo = len(signals) - n_body
    print(f"{n_body} Body-condition signals, {n_emo} Emotion signals, {len(data['additional'])} additional experiences → {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
