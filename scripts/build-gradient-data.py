#!/usr/bin/env python3
"""Build Model 2's connected position records from current site sources.

Sixteen questions come from premise.html; answers remain attributed excerpts
from positions.html and autonomic.html. No mechanism is inferred by the build.
Usage: python3 scripts/build-gradient-data.py [--check]
"""
from __future__ import annotations
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / '03-model-2-gradient'
SPEC = importlib.util.spec_from_file_location('compass_source', ROOT / 'scripts/build-compass-data.py')
COMPASS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPASS)
KEYS = ['x', 'a', 'ab', 'b', 'c', 'd', 'z']

def clean(value):
    value = re.sub(r'<[^>]+>', '', value)
    return re.sub(r'\s+', ' ', html.unescape(value)).strip()

def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')

def build():
    source = (FOLDER / 'positions.html').read_text()
    walker = COMPASS.TableWalker(); walker.feed(source)
    tables = {plane: {h.split('ME slider')[0].strip(): cells for h, cells in rows} for plane, rows in walker.rows.items()}
    premise = (FOLDER / 'premise.html').read_text()
    lenses = [dict(title=clean(t), question=clean(q)) for t, q in re.findall(r'<article class="lens">.*?<h3>(.*?)</h3><p>(.*?)</p>.*?</article>', premise, re.S)]
    assert len(lenses) == 16, 'The governing premise must supply sixteen lenses'
    autonomic = {}
    for ident, article in re.findall(r'<article[^>]*id="((?:fluid|chronic)-[a-z]+)"[^>]*>(.*?)</article>', (FOLDER / 'autonomic.html').read_text(), re.S):
        fields = {clean(k): clean(v) for k, v in re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', article, re.S)}
        status = re.search(r'<p class="status">(.*?)</p>', article, re.S)
        autonomic[ident] = {'fields': fields, 'status': clean(status[1]) if status else 'Working synthesis; evidence review open'}
    assert len(autonomic) == 14
    records = {}
    for i, key in enumerate(KEYS):
        record = {'key': key, 'position': COMPASS.POSITIONS[i], 'readings': {}}
        for plane in ['fluid', 'chronic']:
            rows = tables[plane]
            bio = autonomic[f'{plane}-{key}']
            def row(label):
                if label not in rows: return None
                target = f'{plane}-{slug(label)}-{key}'
                assert f'id="{target}"' in source, target
                return {'label': label, 'text': rows[label][i], 'source': f'positions.html#{target}'}
            def biology(label):
                if label not in bio['fields']: return None
                return {'label': label, 'text': bio['fields'][label], 'source': f'autonomic.html#{plane}-{key}'}
            # Each mapping makes a source relevant to a question; it does not
            # assert that the source fully answers the question.
            mapping = [
                [row('Organisational problem-space' if plane == 'fluid' else 'Protective recruitment'), biology('Functional autonomic task')],
                [biology('Likely pathway participation'), biology('Measurement and evidence limits')],
                [row('Resource allocation emphasis')],
                [biology('Organ-level pattern')],
                [biology('Organ-level pattern')],
                [biology('Organ-level pattern'), row('Action-readiness, available repertoire and controllability')],
                [row('Perception' if plane == 'fluid' else 'Information weighting')],
                [row('Perception' if plane == 'fluid' else 'Information weighting')],
                [row('Interoceptive processing'), biology('What may become conscious')],
                [row('Emotions' if plane == 'fluid' else 'ESS emotional signal formation')],
                [row('Mentalizing'), row('CLS contribution to interpretation')],
                [row('Affective sharing'), row('Empathic concern')],
                [biology('Organ-level pattern')],
                [row('Summary' if plane == 'fluid' else 'Action-readiness, available repertoire and controllability')],
                [biology('What allows updating')],
                [row('Current availability for transition and Return' if plane == 'fluid' else 'Current organisation persistence, transition and Return availability'), biology('What allows updating')]
            ]
            entries=[]
            for n, (lens, fragments) in enumerate(zip(lenses, mapping)):
                fragments=[f for f in fragments if f]
                note='Working source excerpts; a mapped answer does not establish a validated mechanism.'
                if not fragments: note='No separate position-specific answer in the current mapped sources. Keep this question open.'
                elif n in [3,4,5,12]: note='Shared organ-level account. This lens still needs a separate position-specific explanation; the excerpt is not a complete account of this system.'
                elif n in [6,7]: note='Current information-priority description. Sensory processing and attention still need separate accounts.'
                elif n in [8,10,11]: note='Model 2 describes process conditions. Conscious access and use belong to Model 1; these excerpts do not assign an access level or behaviour.'
                elif n==2: note='Allocation emphasis only. Detailed energy mechanisms remain open.'
                entries.append({**lens, 'fragments': fragments, 'note': note})
            record['readings'][plane]={'name': rows['Nervous system organisation'][i], 'summary': row('Organisational problem-space' if plane == 'fluid' else 'Protective recruitment'), 'lenses': entries, 'rows': [row(label) for label in rows], 'biology': bio, 'grounding': row('Grounding'), 'source': f'positions.html#{plane}-position-{key}'}
        records[key]=record
    return {'positions': KEYS, 'records': records, 'premise': 'premise.html#lenses'}

def readable(data):
    lines=['# Nervous System Gradient position records', '', 'Generated from the current site Gradient table, autonomic companion and governing premise. Edit the source pages, then regenerate; this file is a reading view, not a second definition.', '', 'Status: working position explanations. Naming, position architecture and interpretive rules retain their existing approval status. A complete set of questions does not mean completed scientific review.', '', '[Session guide](SESSION-GUIDE.md) · [Source comparison](notes/source-comparison.md) · [Full Gradient table](positions.html)', '']
    for key, record in data['records'].items():
        lines += [f'## {record["position"]} · {record["readings"]["fluid"]["name"]}', '', f'[Open the connected position record](position.html?position={key})', '']
        for plane, reading in record['readings'].items():
            lines += [f'<a id="{plane}-{key}"></a>', f'### {plane.title()} · {reading["name"]}', '', f'[Original table position]({reading["source"]}) · [Autonomic participation](autonomic.html?position={key}&reading={plane}#{plane}-{key}) · [Depth](depth.html?position={key}&reading={plane}) · [Return and recovery](return.html?position={key}&reading={plane})', '']
            for lens in reading['lenses']:
                lines += [f'#### {lens["title"]}', '', lens['question'], '', lens['note'], '']
                for fragment in lens['fragments']: lines += [f'**{fragment["label"]}:** {fragment["text"]}', '', f'[Source]({fragment["source"]})', '']
            lines += ['#### Evidence and limits', '', reading['biology']['status'], '', reading['grounding']['text'], '', f'[Grounding source]({reading["grounding"]["source"]})', '', '#### All original table rows for this position', '']
            for row in reading['rows']: lines += [f'**{row["label"]}:** {row["text"]}', '', f'[Exact table cell]({row["source"]})', '']
    return '\n'.join(lines)

def main():
    if any(a != '--check' for a in sys.argv[1:]): raise SystemExit('Usage: build-gradient-data.py [--check]')
    data=build()
    outputs={FOLDER/'data/positions.js': '/* Generated by scripts/build-gradient-data.py. Do not edit. */\nwindow.TEG_GRADIENT = '+json.dumps(data,ensure_ascii=False,indent=1)+';\n', FOLDER/'position-records.md': readable(data)}
    if '--check' in sys.argv:
        stale=[str(p.relative_to(ROOT)) for p,t in outputs.items() if not p.exists() or p.read_text()!=t]
        if stale: print('Regenerate Model 2 records: '+', '.join(stale));return 1
    else:
        for p,t in outputs.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
    print('Model 2 records current: seven positions, two readings, sixteen sourced questions per reading.')
    return 0
if __name__=='__main__': raise SystemExit(main())
