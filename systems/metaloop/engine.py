#!/usr/bin/env python3
"""MetaLoop deterministic MVP; no model API, no arbitrary code execution."""
import argparse
import hashlib
import json
import re
import time
from copy import deepcopy
from pathlib import Path

def normalize_ascii(v):
    return re.sub(r'[ \t]+', ' ', v).strip(' \t')

def normalize_unicode(v):
    return re.sub(r'[\u00a0 \t]+', ' ', v).strip(' \t\u00a0')

def dedupe_lines(v):
    return '\n'.join(dict.fromkeys(x.strip() for x in v.splitlines() if x.strip()))

def percentage_drop(v):
    high, low = float(v['high']), float(v['low'])
    if high <= 0 or low < 0:
        raise ValueError('require high > 0 and low >= 0')
    return round((high - low) / high * 100, 4)

def json_lookup(v):
    obj = json.loads(v['document'])
    for k in v['path'].split('.'):
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    return obj

OPS = dict(normalize_ascii=normalize_ascii, normalize_unicode=normalize_unicode,
           dedupe_lines=dedupe_lines, percentage_drop=percentage_drop, json_lookup=json_lookup)

def same(actual, expected, tolerance=0):
    if type(actual) is not type(expected):
        return False
    if type(actual) in (float, int):
        return abs(actual - expected) <= tolerance
    return actual == expected

def execute(task, operation=None, operations=None):
    """Apply explicit task contract with bounded retries and observable traces."""
    ops = operations or OPS
    calls, trace, last, status = 0, [], None, 'FAIL'
    maximum = max(0, min(int(task.get('max_calls', 4)), 20))
    repair_limit = max(0, min(int(task.get('max_repairs', 2)), 2))
    mode = task.get('route', 'direct')
    steps = task['steps'] if 'steps' in task else [operation or task['operation']]
    if not isinstance(steps, list) or not steps or mode not in ('direct', 'sequence', 'parallel'):
        raise ValueError('invalid workflow')
    if mode == 'direct' and len(steps) != 1:
        raise ValueError('direct requires one step')
    if mode == 'parallel' and task.get('repair_candidates'):
        raise ValueError('parallel repair unsupported')
    attempts = [steps] + [[x] for x in task.get('repair_candidates', [])[:repair_limit]]
    started = time.perf_counter()
    for attempt_no, attempt in enumerate(attempts):
        if calls + len(attempt) > maximum:
            status = 'BUDGET_STOP'
            break
        try:
            value, results = task['input'], []
            for name in attempt:
                if name not in ops:
                    raise ValueError('unregistered operation: ' + name)
                arg = task['input'] if mode == 'parallel' else value
                value = ops[name](arg)
                calls += 1
                results.append(value)
                trace.append({'attempt': attempt_no, 'operation': name, 'status': 'executed'})
            last = results if mode == 'parallel' else value
            if 'expected' not in task:
                status = 'UNVERIFIED'
                break
            if same(last, task['expected'], task.get('tolerance', 0)):
                status = 'PASS'
                break
            trace.append({'attempt': attempt_no, 'status': 'acceptance_failed'})
        except (KeyError, ValueError, TypeError, IndexError) as exc:
            trace.append({'attempt': attempt_no, 'status': 'error', 'detail': str(exc)[:200]})
            calls += 1
            status = 'FAIL'
    return dict(id=task.get('id', 'unnamed'), status=status, route=mode, output=last,
                calls=calls, repairs=max((x['attempt'] for x in trace), default=0),
                elapsed_ms=round((time.perf_counter() - started) * 1000, 3), trace=trace)

def compare(suite, baseline, candidate):
    """Compare deterministic outcomes only; not an independent LLM evaluation."""
    cases = suite['cases']
    if len(cases) < 3 or len({x['domain'] for x in cases}) < 2 or len({x['id'] for x in cases}) != len(cases):
        raise ValueError('need >=3 unique cases from >=2 domains')
    rows = []
    for case in cases:
        task = {k: deepcopy(v) for k,v in case.items() if k != 'domain'}
        alias = task['operation'] == 'normalize_alias'
        b = execute(task, operation=baseline if alias else None)
        c = execute(task, operation=candidate if alias else None)
        rows.append(dict(id=case['id'], domain=case['domain'], baseline=b['status'],
                         candidate=c['status'], baseline_output=b['output'], candidate_output=c['output']))
    improved = any(r['baseline'] != 'PASS' and r['candidate'] == 'PASS' for r in rows)
    regressed = any(r['baseline'] == 'PASS' and r['candidate'] != 'PASS' for r in rows)
    return dict(promotable=improved and not regressed,
                baseline_pass=sum(r['baseline']=='PASS' for r in rows),
                candidate_pass=sum(r['candidate']=='PASS' for r in rows),
                cases=rows, independent_model_judge=False)

def promotion(registry, suite):
    state = deepcopy(registry)
    stable = state['text_normalization']['stable']
    candidate = state['text_normalization']['candidate']
    if stable == candidate:
        return dict(promoted=False, reason='no candidate change', registry=state)
    report = compare(suite, stable, candidate)
    if not report['promotable']:
        return dict(promoted=False, reason='no gain or regression', report=report, registry=state)
    state.setdefault('history', []).append(stable)
    state['text_normalization']['stable'] = candidate
    digest = hashlib.sha256(json.dumps(suite, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    state.setdefault('promotion_log', []).append(dict(source=stable, target=candidate,
        suite_sha256=digest, baseline_pass=report['baseline_pass'],
        candidate_pass=report['candidate_pass']))
    return dict(promoted=True, report=report, registry=state)

def rollback(registry):
    state = deepcopy(registry)
    if not state.get('history'):
        raise ValueError('no rollback target')
    state['text_normalization']['stable'] = state['history'].pop()
    return state

def main():
    p = argparse.ArgumentParser(description='MetaLoop MVP (stdlib only)')
    p.add_argument('command', choices=('run', 'compare', 'promote', 'rollback'))
    p.add_argument('--task', type=Path)
    p.add_argument('--suite', type=Path)
    p.add_argument('--registry', type=Path)
    p.add_argument('--journal', type=Path)
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    root = Path(__file__).resolve().parent
    registry_file = args.registry or root/'registry.json'
    suite_file = args.suite or root/'cases/regression.json'
    state = json.loads(registry_file.read_text(encoding='utf-8'))
    if args.command == 'run':
        if not args.task: p.error('run needs --task')
        task = json.loads(args.task.read_text(encoding='utf-8'))
        alias = state['text_normalization']['stable'] if task.get('operation')=='normalize_alias' else None
        result = execute(task, operation=alias)
    elif args.command == 'compare':
        result = compare(json.loads(suite_file.read_text(encoding='utf-8')),
                         state['text_normalization']['stable'], state['text_normalization']['candidate'])
    elif args.command == 'promote':
        result = promotion(state, json.loads(suite_file.read_text(encoding='utf-8')))
        if args.write and result['promoted']:
            registry_file.write_text(json.dumps(result['registry'], ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    else:
        result = rollback(state)
        if args.write:
            registry_file.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if args.journal:
        with args.journal.open('a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
