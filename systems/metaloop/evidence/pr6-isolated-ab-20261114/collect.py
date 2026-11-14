"""Fresh native CLI A/B, no model API client; authorization already granted.

python collect.py --out /tmp/pr6-model-runs
Uses existing native login through a read-only symlink, never serializes auth.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import tempfile
import time
import tomllib
from datetime import datetime,timezone

MODEL='gpt-6.1-sol'  # Observed native default in saved preflight banner.
ASSETS={
 'stable':('prompts/meta-prompt/execute/execute-evidence-based-loop.md','188953441f5c54fdb81c7883ad05aa0e15a277fa'),
 'candidate':('prompts/meta-prompt/execute/orchestrate-metaloop.md','e87076047facb3a88ad95a6322f06a4cd478b0cc'),
}
ROOT=Path(__file__).resolve().parents[4]
PREVIOUS=ROOT/'systems/metaloop/evidence/pr6-followup-20261114/run-01/tasks.json'

def digest(raw):return hashlib.sha256(raw).hexdigest()

def native_run(payload,out,name):
    """Same native config; new writable runtime directory and cwd each time."""
    base=tomllib.loads(Path('/home/agent/.codex/config.toml').read_text())
    with tempfile.TemporaryDirectory(prefix='pr6-native-') as td:
        tmp=Path(td); home=tmp/'runtime';home.mkdir();cwd=tmp/'work';cwd.mkdir()
        (home/'auth.json').symlink_to('/home/agent/.codex/auth.json')
        config='\n'.join(k+' = '+json.dumps(base[k]) for k in ['openai_base_url','chatgpt_base_url'] if k in base)
        config+='\nproject_doc_max_bytes = 0\n[features]\napps=false\nplugins=false\nremote_plugin=false\nshell_tool=false\nshell_snapshot=false\nunified_exec=false\nmulti_agent=false\n'
        (home/'config.toml').write_text(config)
        # CODEX_HOME is used for its documented native configuration purpose;
        # no global environment, original home, login or mount is changed.
        env=os.environ.copy();env['CODEX_HOME']=str(home)
        answer=tmp/'answer.txt'
        cmd=['/opt/codex/bin/codex','exec','--ephemeral','--skip-git-repo-check','-s','read-only','-m',MODEL,'--json','-C',str(cwd),'-o',str(answer),'-']
        (out/(name+'.input.txt')).write_text(payload)
        start=time.monotonic()
        try:
            r=subprocess.run(cmd,input=payload,env=env,cwd=cwd,capture_output=True,text=True,timeout=90)
            stdout,stderr,rc=r.stdout,r.stderr,r.returncode
        except subprocess.TimeoutExpired as e:
            stdout=e.stdout or '';stderr=e.stderr or '';rc='TIMEOUT'
            if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
            if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
        elapsed=time.monotonic()-start
        (out/(name+'.events.jsonl')).write_text(stdout)
        (out/(name+'.stderr.txt')).write_text(stderr)
        raw=answer.read_text() if answer.exists() else ''
        (out/(name+'.raw.txt')).write_text(raw)
        events=[]
        for line in stdout.splitlines():
            try:events.append(json.loads(line))
            except json.JSONDecodeError:pass
        completed=[e for e in events if e.get('type')=='turn.completed']
        tool_events=[e for e in events if isinstance(e.get('item'),dict) and e['item'].get('type') not in ['agent_message','reasoning']]
        meta=dict(model_alias=MODEL,exact_backend_snapshot='NOT_VERIFIED',requested_model=MODEL,
          native_cli='0.167.0-alpha.4',command=cmd,exit_code=rc,elapsed_seconds=elapsed,
          success=rc==0 and bool(raw.strip()) and bool(completed),
          usage=completed[-1].get('usage') if completed else None,
          non_message_events=tool_events,raw_sha256=digest(raw.encode()),input_sha256=digest(payload.encode()),
          temperature='NOT_CONTROLLABLE_NOT_VERIFIED',cost='NOT_VERIFIED',config_sha256=digest(config.encode()),
          clean_process=True,fresh_runtime_and_cwd=True,previous_conversation_supplied=False,
          project_instructions_disabled=True,shell_tools_disabled=True,multi_agent_disabled=True)
        (out/(name+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
        return meta

def main():
    ap=argparse.ArgumentParser(__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    tasks=json.loads(PREVIOUS.read_text());(out/'tasks.json').write_bytes(PREVIOUS.read_bytes())
    prompts={};frozen={}
    for label,(path,sha) in ASSETS.items():
        raw=(ROOT/path).read_bytes()
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()==sha
        prompts[label]=raw.decode();frozen[label]=dict(path=path,blob_sha=sha,sha256=digest(raw))
        (out/(label+'-prompt.md')).write_bytes(raw)
    order=[(label,task,rep) for label in ASSETS for task in tasks for rep in [1,2]]
    random.Random(20261114).shuffle(order)
    freeze=dict(parent_commit='6f2bb71fc06a61d5377f328b8df2df65e8ab5592',prompts=frozen,
       task_sha256=digest(PREVIOUS.read_bytes()),order=order,random_seed=20261114,
       sealed_at=datetime.now(timezone.utc).isoformat(),independent_task_sealing='NOT_VERIFIED',
       classification='EXPLORATORY_PAIRED_PILOT_NOT_BLIND_HELDOUT',replicates_per_condition=2,
       authorization='User approved frozen public prompts and synthetic task payload export to ab.chatgpt.com on 2026-11-14',
       native_endpoints='Existing chatgpt.com native login routes; ab.chatgpt.com export authorized',
       resource_budget='single final response; 90s wall timeout per invocation; no worker tools')
    (out/'freeze.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
    # Frozen evaluator is authored before first scored invocation.
    evaluator=Path(__file__).with_name('verify.py')
    if evaluator.exists(): (out/'frozen-verifier.py').write_bytes(evaluator.read_bytes())
    ledger=[]
    for label,task,rep in order:
        name=f'{label}-{task}-r{rep}'
        payload=prompts[label]+'\n\n'+tasks[task]['input']
        meta=native_run(payload,out,name)
        ledger.append(dict(name=name,label=label,task=task,replicate=rep,**meta))
        (out/'ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(dict(run=name,success=meta['success'],elapsed_seconds=meta['elapsed_seconds'])),flush=True)

if __name__=='__main__': main()
