"""Replay gate controls and attempt clean CLI model tests; never promotes.

python systems/metaloop/evidence/pr6-followup-20261114/run.py --out /tmp/pr6-followup
Model attempts require a working local Codex session runtime. Failure is evidence,
not an output. No credentials, private chats, approvals or production writes.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone

BASE = '25da4c6a29b8a0cd8f0cd10989b598fc944fae17'
PROMPTS = {
    'stable': ('prompts/meta-prompt/execute/execute-evidence-based-loop.md','188953441f5c54fdb81c7883ad05aa0e15a277fa'),
    'candidate': ('prompts/meta-prompt/execute/orchestrate-metaloop.md','e87076047facb3a88ad95a6322f06a4cd478b0cc'),
}
TASKS = {
    'technical-interval-coverage': {
        'domain':'technical', 'source':'new synthetic self-contained task; not independently sealed held-out',
        'input': 'Write Python 3 stdlib function total_covered(intervals, start, end). start/end must be non-bool integers and end > start; otherwise raise ValueError. Each interval must be a list or tuple of exactly two non-bool integers a,b with a < b; reject invalid intervals by their zero-based index. Clip valid intervals to half-open [start,end), ignore valid outside intervals without rejecting them, and return {"covered": union length as integer, "rejected": indices in input order}. Do not double-count overlaps; do not mutate inputs. Provide runnable unit tests. Return only JSON with string fields code, tests, summary. The tests may import solution. No network or third-party packages. You have a single response; do not use tools or claim execution.',
        'acceptance':['correct union, clipping and invalid indices', 'empty/overlap/touching/outside cases', 'bool/float/reversed/short records rejected', 'invalid window raises ValueError', 'input unchanged', 'stdlib only; code externally executable'],
    },
    'nontechnical-pilot-decision': {
        'domain':'nontechnical', 'source':'synthetic facts, not a real organization or external report',
        'input':'根据以下虚构试点记录，给主管写一段不超过220个Unicode字符的建议。事实：工具组20单，平均耗时从40分钟降到25分钟；自愿参加，且本轮只选简单单。同期对照组20单，从40分钟降到38分钟，处理复杂单。工具费每月900元。尚未测错误率、返工、长期效果，也未随机分组。要求：给出现在是否全面上线的建议、说明为何不能直接认定工具造成15分钟提效、提出下一步可验证试验，同时不把虚构记录包装成真实资料，不编造收益或审核。只能返回JSON，字段answer为完整建议。禁止工具调用。',
        'acceptance':['<=220 Unicode code points', 'no immediate full rollout / bounded pilot', 'selection and complexity differences prevent causal attribution', 'matched or randomized next trial', 'quality/error/rework measures required', 'no fabricated savings or genuine independent signoff'],
    },
}

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--attempt-model',action='store_true',
                    help='Requires explicit authorization for payload export to the CLI provider; omitted by default')
    args=ap.parse_args()
    out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True)
    repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    def git(*a): return subprocess.check_output(['git','-C',str(repo),*a])
    def save(path,obj):
        (out/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    def command(name,argv,cwd,env=None,stdin=None,timeout=60):
        t=time.monotonic()
        try:
            r=subprocess.run(argv,cwd=cwd,env=env,input=stdin,text=True,capture_output=True,timeout=timeout)
            stdout,stderr,rc=r.stdout,r.stderr,r.returncode
        except subprocess.TimeoutExpired as e:
            stdout=e.stdout or b''; stderr=e.stderr or b''
            stdout=stdout.decode() if isinstance(stdout,bytes) else stdout
            stderr=stderr.decode() if isinstance(stderr,bytes) else stderr
            rc='TIMEOUT'
        (out/(name+'.stdout.txt')).write_text(stdout)
        (out/(name+'.stderr.txt')).write_text(stderr)
        meta=dict(command=argv,exit_code=rc,elapsed_seconds=time.monotonic()-t)
        save(name+'.command.json',meta)
        return meta,stdout,stderr
    registry_before=hashlib.sha256((repo/'systems/metaloop/registry.json').read_bytes()).hexdigest()
    # All desired conditions are frozen before any task-model invocation.
    save('tasks.json',TASKS)
    freeze={}
    for label,(path,sha) in PROMPTS.items():
        raw=git('show',BASE+':'+path)
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()==sha
        assert raw==(repo/path).read_bytes()
        freeze[label]=dict(path=path,blob_sha=sha,sha256=hashlib.sha256(raw).hexdigest())
        (out/(label+'-prompt.md')).write_bytes(raw)
        for task,spec in TASKS.items():
            (out/(label+'-'+task+'.input.txt')).write_text(raw.decode()+'\n\n'+spec['input'])
    save('freeze.json',dict(parent_commit=BASE,prompts=freeze,task_sha256=hashlib.sha256((out/'tasks.json').read_bytes()).hexdigest()))
    (out/'patch.diff').write_bytes(git('diff','--','systems/metaloop/engine.py','systems/metaloop/tests/test_engine.py','systems/metaloop/README.md'))
    # A bounded source inventory; no claim about unseen private development sets.
    files=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
    matches=[]
    for path in files:
        raw=git('show',BASE+':'+path).decode(errors='replace')
        for marker in ['total_covered(intervals', 'nontechnical-pilot-decision', '工具组20单']:
            if marker in raw: matches.append(dict(path=path,marker=marker))
    save('overlap-screen.json',dict(exact_marker_hits=matches,scope='all tracked files at frozen parent',
        private_development_inventory='NOT_VERIFIED',semantic_overlap_review='NOT_VERIFIED',
        independent_sealing='NOT_VERIFIED',classification='EXPLORATORY_NOT_BLIND_HELDOUT'))
    probe='''import copy,json,sys
sys.path.insert(0,'systems/metaloop')
from engine import promotion
from pathlib import Path
p=Path('systems/metaloop'); r=json.loads((p/'registry.json').read_text()); s=json.loads((p/'cases/regression.json').read_text()); h=copy.deepcopy(s)
for c in h['cases']: c['id']='renamed-'+c['id']
h['cases'].reverse()
review=dict(approved=True,reviewer_type='human',reviewer_id='SYNTHETIC_TEST_NOT_APPROVAL',evidence_ref='fixture://synthetic',heldout_suite=h)
x=promotion(r,s,review)
assert json.loads((p/'registry.json').read_text())==r
print(json.dumps(dict(promoted_in_memory=x['promoted'],reason=x.get('reason'),registry_unchanged=True,synthetic=True)))
'''
    (out/'gate-probe.py.txt').write_text(probe)
    with tempfile.TemporaryDirectory(prefix='pr6-before-') as d:
        with tarfile.open(fileobj=io.BytesIO(git('archive',BASE))) as tf: tf.extractall(d,filter='data')
        before,old,_=command('gate-before',[sys.executable,'-I','-c',probe],d)
    after,new,_=command('gate-after',[sys.executable,'-I','-c',probe],repo)
    assert before['exit_code']==after['exit_code']==0
    assert json.loads(old)['promoted_in_memory'] is True
    assert json.loads(new)['promoted_in_memory'] is False
    command('regression',[sys.executable,'-I','-m','unittest','discover','-s','systems/metaloop/tests','-v'],repo)
    command('inventory',[sys.executable,'-I','systems/metaloop/lifecycle.py','audit','--strict'],repo)
    command('diff-check',['git','diff','--check'],repo)
    cli=shutil.which('codex')
    ver=subprocess.run([cli,'--version'],capture_output=True,text=True) if cli else None
    save('conditions.json',dict(collected_at=datetime.now(timezone.utc).isoformat(),python=sys.version,
        cli_version=ver.stdout.strip() if ver else 'UNAVAILABLE',model_id='NOT_VERIFIED',
        sampling='NOT_VERIFIED',independent_reviewer='NOT_VERIFIED',human_approval='NOT_VERIFIED',
        system_prompt_identity='NOT_VERIFIED',intended_tools='none; textual no-tools instruction with read-only sandbox, not a hard tool denial',
        scope='Fresh CLI processes and temporary working directories, no previous conversation supplied. Shared host/auth runtime. Model context isolation requires successful startup.',
        resource_budget='one response, 30 second wall timeout per attempt',
        model_token_usage='NOT_VERIFIED',model_cost='NOT_VERIFIED'))
    order=[(l,t) for t in TASKS for l in PROMPTS]
    random.Random(20261114).shuffle(order)
    save('run-order.json',dict(seed=20261114,order=order))
    ledger=[]
    for label,task in order:
        name=label+'-'+task
        payload=(out/(name+'.input.txt')).read_text()
        if not args.attempt_model:
            ledger.append(dict(task=task,label=label,exit_code='NOT_RUN',status='NOT_VERIFIED',
                raw_output=None,failure='BLOCKED_AUTO_REVIEW: payload export to ab.chatgpt.com not explicitly authorized',
                independent_review='NOT_VERIFIED',decision='DO_NOT_PROMOTE'))
            continue
        with tempfile.TemporaryDirectory(prefix='pr6-model-') as d:
            root=Path(d); (root/'tmp').mkdir()
            env=os.environ.copy(); env['TMPDIR']=str(root/'tmp')
            argv=[cli,'exec','--ephemeral','--ignore-user-config','--skip-git-repo-check','-s','read-only',
                  '-c','sqlite_home='+json.dumps(str(root/'state')),
                  '-c','log_dir='+json.dumps(str(root/'logs')),
                  '--json','-C',str(root),'-o',str(root/'answer.txt'),'-'] if cli else []
            if not cli:
                meta=dict(exit_code='UNAVAILABLE'); stdout=''; stderr='Codex CLI unavailable'
            else:
                meta,stdout,stderr=command(name,argv,root,env,payload,timeout=30)
            answer=root/'answer.txt'
            if answer.exists(): (out/(name+'.raw-output.txt')).write_bytes(answer.read_bytes())
            ledger.append(dict(task=task,label=label,exit_code=meta['exit_code'],
                status='RAW_OUTPUT_REQUIRES_VERIFICATION' if answer.exists() else 'NOT_VERIFIED',
                raw_output=name+'.raw-output.txt' if answer.exists() else None,
                failure='runtime startup failed' if 'failed to initialize' in stderr else stderr[-300:],
                independent_review='NOT_VERIFIED',decision='DO_NOT_PROMOTE'))
    save('model-ledger.json',ledger)
    assert hashlib.sha256((repo/'systems/metaloop/registry.json').read_bytes()).hexdigest()==registry_before
    save('boundary-check.json',dict(registry_unchanged=True,prompts_unchanged=True,merged=False,production_written=False,
        gate_before=True,gate_after=False,model_successes=sum(x['raw_output'] is not None for x in ledger)))
    save('SHA256SUMS.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS.json'})
    print(json.dumps(dict(gate_fixed=True,planned_model_runs=len(ledger),
        model_attempts=sum(x['exit_code']!='NOT_RUN' for x in ledger),
        model_raw_outputs=sum(x['raw_output'] is not None for x in ledger),result='NOT_VERIFIED'),indent=2))

if __name__=='__main__': main()
