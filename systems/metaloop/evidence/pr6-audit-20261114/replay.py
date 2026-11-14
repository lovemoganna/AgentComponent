"""Reproduce deterministic controls, NOT a prompt/model A/B. Stdlib only.

Run from any checkout: python path/to/replay.py --out /tmp/pr6-replay
Uses git archive of the frozen PR; never writes Registry or production refs.
"""
import argparse
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone

BASE = '011694de28436fc11cc1aa68ff916aa7579dff06'
HEAD = '13768da0d7e9655b481b1a01cd03754c6d24cfc9'
ASSETS = {
    'stable': ('prompts/meta-prompt/execute/execute-evidence-based-loop.md', '188953441f5c54fdb81c7883ad05aa0e15a277fa'),
    'candidate': ('prompts/meta-prompt/execute/orchestrate-metaloop.md', 'e87076047facb3a88ad95a6322f06a4cd478b0cc'),
}

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
    def git(*argv):
        return subprocess.check_output(['git', '-C', str(repo), *argv])
    def save(name, value):
        (out/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    frozen = {}
    for label, (path, sha) in ASSETS.items():
        content = git('show', f'{HEAD}:{path}')
        actual = hashlib.sha1(f'blob {len(content)}\0'.encode()+content).hexdigest()
        assert sha == actual
        assert git('rev-parse', f'{BASE}:{path}').decode().strip() == sha
        (out/f'{label}-prompt.md').write_bytes(content)
        frozen[label] = dict(path=path, blob_sha=sha, sha256=hashlib.sha256(content).hexdigest())
    save('freeze.json', dict(base_commit=BASE, pr_head_commit=HEAD, assets=frozen))
    protocol = git('show', f'{HEAD}:systems/metaloop/evidence/paired-eval-preregistration-20261114.md').decode()
    tasks = {}
    for key, start, end in [('A', '## Task A', '## Task B'), ('B', '## Task B', '## Paired execution')]:
        tasks[key] = protocol[protocol.index(start):protocol.index(end)]
    save('tasks.json', tasks)
    for label in ASSETS:
        for key, task in tasks.items():
            payload = (out/f'{label}-prompt.md').read_text()+'\n\n'+task
            (out/f'{label}-task-{key}.input.txt').write_text(payload)
    save('conditions.json', dict(
        collected_at=datetime.now(timezone.utc).isoformat(),
        runtime=sys.version, executable=sys.executable, platform=platform.platform(),
        python311='NOT_VERIFIED' if sys.version_info[:2] != (3,11) else 'VERIFIED',
        controller='Current ChatGPT session; exact deployed model identifier NOT_VERIFIED',
        model_runs=0, model_id='NOT_VERIFIED', model_temperature='NOT_VERIFIED',
        tokens='NOT_VERIFIED', cost='NOT_VERIFIED', model_latency='NOT_VERIFIED',
        isolation='Separate temporary directories/processes; sanitized env; Python -I; shared OS/kernel; no OS network isolation',
        clean_model_context='NOT_VERIFIED', independent_reviewer='NOT_VERIFIED',
        tools=['git', 'Python stdlib', 'exec_command', 'GitHub connector', 'web retrieval'],
        external_model_api_used=False,
    ))
    # Scope: complete tracked tree and reachable history; private chats, deleted
    # branches, external development corpora and model training are not accessible.
    hits = []
    needles = ['DictReader', 'id,amount', 'building-evaluation-probes-agentic-ai', '自评']
    for path in git('ls-tree', '-r', '--name-only', HEAD).decode().splitlines():
        raw = git('show', f'{HEAD}:{path}').decode(errors='replace')
        for n, line in enumerate(raw.splitlines(), 1):
            if any(s in line for s in needles):
                hits.append(dict(path=path, line=n, text=line))
    history = git('log', '--all', '--format=%H %s', '-G', 'DictReader|building-evaluation-probes-agentic-ai', '--', 'systems/metaloop').decode()
    save('overlap.json', dict(status='OVERLAP_DETECTED_PUBLIC_PRIOR_EXPOSURE', hits=hits, history=history,
        development_suite='systems/metaloop/cases/regression.json',
        complete_development_inventory='NOT_VERIFIED', independent_sealing='NOT_VERIFIED',
        interpretation='A/B preregistration and prior reference probes already expose tasks/answers. Not blind held-out. No claim of exact match to every private development case.'))
    records = []
    archive = git('archive', HEAD)
    for label in ['stable', 'candidate']:
        with tempfile.TemporaryDirectory(prefix='pr6-'+label+'-') as tmp:
            root = Path(tmp)
            with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
                tf.extractall(root, filter='data')
            home = root/'clean-home'
            home.mkdir()
            env = {'PATH':os.environ.get('PATH',''), 'HOME':str(home), 'LANG':'C.UTF-8', 'TZ':'UTC', 'PYTHONDONTWRITEBYTECODE':'1'}
            cmds = [
                ('regression', [sys.executable,'-I','-m','unittest','discover','-s','systems/metaloop/tests','-v']),
                ('adapter-compare', [sys.executable,'-I','systems/metaloop/engine.py','compare']),
                ('inventory', [sys.executable,'-I','systems/metaloop/lifecycle.py','audit','--strict']),
            ]
            for name, cmd in cmds:
                start = time.monotonic()
                r = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=60)
                elapsed = time.monotonic()-start
                (out/f'{label}-{name}.stdout.txt').write_text(r.stdout)
                (out/f'{label}-{name}.stderr.txt').write_text(r.stderr)
                records.append(dict(label=label, control=name, command=cmd, exit_code=r.returncode, elapsed_seconds=elapsed,
                    attribution='Repository deterministic control; prompt was NOT supplied to a model'))
            # Adversarial evidence: rename the development IDs but retain all
            # inputs/answers. The synthetic fixture is never external approval.
            probe = '''import copy,json,sys
sys.path.insert(0,'systems/metaloop')
from engine import promotion
from pathlib import Path
p=Path('systems/metaloop')
r=json.loads((p/'registry.json').read_text())
s=json.loads((p/'cases/regression.json').read_text())
h=copy.deepcopy(s)
for c in h['cases']: c['id']='renamed-'+c['id']
review=dict(approved=True,reviewer_type='human',reviewer_id='SYNTHETIC_FIXTURE_NOT_APPROVAL',evidence_ref='fixture://not-real',heldout_suite=h)
result=promotion(r,s,review)
assert json.loads((p/'registry.json').read_text())==r
print(json.dumps(dict(probe='renamed development cases',synthetic=True,inputs_and_answers_identical=True,promoted_in_memory=result['promoted'],disk_registry_unchanged=True,reason=result.get('reason')),indent=2))
'''
            (out/'overlap-gate-probe.py.txt').write_text(probe)
            r = subprocess.run([sys.executable,'-I','-c',probe],cwd=root,env=env,capture_output=True,text=True,timeout=30)
            (out/f'{label}-overlap-gate.stdout.txt').write_text(r.stdout)
            (out/f'{label}-overlap-gate.stderr.txt').write_text(r.stderr)
            records.append(dict(label=label,control='overlap-gate',exit_code=r.returncode,synthetic=True))
    save('execution.json', records)
    ledger=[]
    for task in ['A-technical-CSV', 'B-nontechnical-source-explanation']:
        ledger.append(dict(task=task, stable_raw_output=None, candidate_raw_output=None,
            stable_status='NOT_VERIFIED', candidate_status='NOT_VERIFIED',
            reason='No isolated model invocations performed; reference probe is not attributable to either prompt',
            independent_verification='NOT_VERIFIED', paired_result='NOT_COMPARABLE', promotion='BLOCKED'))
    save('model-ab-ledger.json', ledger)
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS.json'}
    save('SHA256SUMS.json',hashes)
    print(json.dumps(dict(output=str(out), commands=len(records), model_runs=0, result='NOT_VERIFIED'),indent=2))

if __name__ == '__main__':
    main()
