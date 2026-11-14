"""External deterministic verifier, frozen before worker model runs."""
import argparse
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

TECH_CHECKER=r'''
import importlib.util,sys,json,copy
s=importlib.util.spec_from_file_location('solution',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
f=m.total_covered
cases=[
 ('empty',[],0,10,{'covered':0,'rejected':[]}),
 ('overlap',[[1,5],[3,8]],0,10,{'covered':7,'rejected':[]}),
 ('touching',[[0,3],[3,6]],0,10,{'covered':6,'rejected':[]}),
 ('clip',[[-5,4],[8,15]],0,10,{'covered':6,'rejected':[]}),
 ('outside',[[-8,-2],[11,14]],0,10,{'covered':0,'rejected':[]}),
 ('invalid',[[1,1],[7,2],[True,5],[2,3.0],[1],[1,2,3],'12',None],0,10,{'covered':0,'rejected':list(range(8))}),
 ('mixed',[[1,4],[2,9],[9,11],[5,5],[0,False]],2,10,{'covered':8,'rejected':[3,4]}),
 ('nested',[(2,8),(3,5),(2,8)],0,10,{'covered':6,'rejected':[]}),
 ('negative',[[-9,-4],[-6,-1]],-8,-2,{'covered':6,'rejected':[]}),
]
results=[]
for name,intervals,start,end,expected in cases:
 before=copy.deepcopy(intervals)
 try:
  got=f(intervals,start,end)
  ok=type(got)==dict and got==expected and type(got.get('covered'))==int and type(got.get('rejected'))==list and intervals==before
  results.append(dict(check=name,pass_=ok,actual=got,expected=expected,input_unchanged=intervals==before))
 except Exception as e:results.append(dict(check=name,pass_=False,error=repr(e)))
for start,end in [(0,0),(10,0),(True,10),(0,False),(0.0,10),(0,10.0)]:
 try:
  f([],start,end);ok=False
 except ValueError:ok=True
 except Exception:ok=False
 results.append(dict(check='invalid_window_'+repr((start,end)),pass_=ok))
# Exhaustive integer-grid oracle independent of the usual merge algorithm.
import random
r=random.Random(81743)
for i in range(100):
 pairs=[]
 for _ in range(r.randrange(10)):
  a,b=sorted(r.sample(range(-10,11),2));pairs.append([a,b])
 start,end=sorted(r.sample(range(-10,11),2))
 expected=sum(any(a<=x<b for a,b in pairs) for x in range(start,end))
 try:
  got=f(pairs,start,end);ok=got=={'covered':expected,'rejected':[]}
 except Exception as e:ok=False;got=repr(e)
 results.append(dict(check='grid_oracle_'+str(i),pass_=ok,actual=got,expected=expected))
print(json.dumps(dict(checks=len(results),passed=sum(x['pass_'] for x in results),results=results),ensure_ascii=False))
'''

def parse(raw):
    s=raw.strip()
    if s.startswith('```'):
        s=s.split('\n',1)[1];s=s.rsplit('```',1)[0]
    return json.loads(s)

def safe_source(code):
    tree=ast.parse(code)
    for n in ast.walk(tree):
        if isinstance(n,(ast.Import,ast.ImportFrom)):
            names=[x.name for x in n.names] if isinstance(n,ast.Import) else [n.module or '']
            if any(x.split('.')[0] not in ['typing','collections','copy','unittest','math','functools','itertools'] for x in names):return False
        if isinstance(n,ast.Name) and n.id in ['open','eval','exec','compile','__import__','getattr','globals','locals','vars','input']:return False
        if isinstance(n,ast.Attribute) and n.attr.startswith('__'):return False
    return True

def main():
    ap=argparse.ArgumentParser(__doc__);ap.add_argument('--runs',type=Path,required=True);args=ap.parse_args()
    out=args.runs.resolve();ledger=json.loads((out/'ledger.json').read_text());results=[]
    for run in ledger:
        name=run['name'];raw=(out/(name+'.raw.txt')).read_text()
        result=dict(name=name,label=run['label'],task=run['task'],replicate=run['replicate'],model_run_success=run['success'])
        try:
            data=parse(raw);result['json_format_pass']=True
            if run['task'].startswith('technical'):
                code=data['code'];tests=data['tests'];result['source_safety_screen_pass']=safe_source(code) and safe_source(tests)
                (out/(name+'.solution.py')).write_text(code)
                (out/(name+'.worker-tests.py')).write_text(tests)
                if result['source_safety_screen_pass']:
                    with tempfile.TemporaryDirectory(prefix='pr6-code-check-') as d:
                        root=Path(d);(root/'solution.py').write_text(code);(root/'worker_tests.py').write_text(tests)
                        (root/'check.py').write_text(TECH_CHECKER)
                        cmd=[sys.executable,'-I',str(root/'check.py'),str(root/'solution.py')]
                        r=subprocess.run(cmd,capture_output=True,text=True,cwd=root,timeout=10)
                        (out/(name+'.external-tests.stdout.txt')).write_text(r.stdout)
                        (out/(name+'.external-tests.stderr.txt')).write_text(r.stderr)
                        result['external_test_exit_code']=r.returncode
                        if r.returncode==0:result['external_tests']=json.loads(r.stdout)
                        # -I ignores PYTHONPATH; explicitly supply only the fresh temp dir.
                        cmd=[sys.executable,'-I','-c',"import sys,runpy;sys.path.insert(0,sys.argv[1]);runpy.run_path(sys.argv[2],run_name='__main__')",d,str(root/'worker_tests.py')]
                        r=subprocess.run(cmd,capture_output=True,text=True,cwd=root,timeout=10)
                        (out/(name+'.worker-tests.stdout.txt')).write_text(r.stdout)
                        (out/(name+'.worker-tests.stderr.txt')).write_text(r.stderr)
                        result['worker_test_exit_code']=r.returncode
                checks=result.get('external_tests',{})
                result['deterministic_pass']=checks.get('checks')==115 and checks.get('passed')==115 and result.get('worker_test_exit_code')==0
            else:
                answer=data['answer'];result['characters']=len(answer)
                result['length_pass']=isinstance(answer,str) and len(answer)<=220
                result['deterministic_pass']=result['length_pass']
                result['semantic_review']='PENDING_SEPARATE_CONTEXT_REVIEW'
        except Exception as e:result.update(deterministic_pass=False,error=repr(e))
        results.append(result)
    (out/'deterministic-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([dict(name=x['name'],pass_=x['deterministic_pass'],chars=x.get('characters'),checks=x.get('external_tests',{}).get('passed')) for x in results],ensure_ascii=False))

if __name__=='__main__':main()
