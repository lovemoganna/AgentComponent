#!/usr/bin/env python3
"""MetaLoop asset/feedback lifecycle. Stdlib only; never executes model calls or edits prompts."""
import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

STATUSES = {"stable", "candidate", "catalogued", "deprecated"}
OUTCOMES = {"PASS", "FAIL", "BLOCKED", "UNKNOWN"}
EVENT_FIELDS = {"event_id", "task_id", "domain", "event_time", "origin", "outcome",
                "prompt_path", "need_key", "failure_code", "evidence_ref",
                "elapsed_ms", "cost_usd"}
REQUIRED = {"event_id", "task_id", "domain", "event_time", "origin", "outcome", "evidence_ref"}

def blob_sha(content):
    raw = content.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def audit_registry(root, registry):
    root = Path(root)
    disk = {p.relative_to(root).as_posix(): p for p in (root / "prompts").rglob("*.md")}
    records = registry.get("prompt_assets", [])
    seen, errors, coverage = set(), [], {}
    for item in records:
        path = item.get("path", "")
        if not isinstance(path, str) or not path.startswith("prompts/") or ".." in Path(path).parts:
            errors.append("invalid_path:" + str(path))
            continue
        if path in seen:
            errors.append("duplicate_registry:" + path)
        seen.add(path)
        if item.get("status") not in STATUSES:
            errors.append("invalid_status:" + path)
        if path not in disk:
            errors.append("missing_file:" + path)
            continue
        sha = blob_sha(disk[path].read_text(encoding="utf-8"))
        if sha != item.get("blob_sha"):
            errors.append("hash_mismatch:" + path)
        coverage[path] = item.get("status")
    for path in sorted(disk.keys() - seen):
        errors.append("unregistered:" + path)
    duplicates = defaultdict(list)
    for path, f in disk.items():
        duplicates[blob_sha(f.read_text(encoding="utf-8"))].append(path)
    exact_duplicates = [sorted(v) for v in duplicates.values() if len(v) > 1]
    return {"status": "PASS" if not errors else "FAIL", "prompt_files": len(disk),
            "registered": len(seen), "by_status": {s:sum(v == s for v in coverage.values())
                                                 for s in sorted(STATUSES)},
            "errors": sorted(errors), "exact_duplicate_groups": exact_duplicates}

def validate_event(event, registry):
    if not isinstance(event, dict):
        raise ValueError("event must be an object")
    if event.keys() - EVENT_FIELDS:
        raise ValueError("raw/unapproved fields forbidden: " + ", ".join(sorted(event.keys()-EVENT_FIELDS)))
    if REQUIRED - event.keys():
        raise ValueError("missing required event fields")
    for key in REQUIRED - {"outcome", "origin"}:
        value = event[key]
        if not isinstance(value, str) or not value.strip() or len(value) > 350:
            raise ValueError("invalid field: " + key)
    if event["origin"] not in ("real", "synthetic") or event["outcome"] not in OUTCOMES:
        raise ValueError("invalid origin/outcome")
    dt = datetime.fromisoformat(event["event_time"].replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timestamp requires timezone")
    registered = {x["path"] for x in registry["prompt_assets"]}
    path = event.get("prompt_path")
    need = event.get("need_key")
    if bool(path) == bool(need):
        raise ValueError("provide exactly one prompt_path or need_key")
    if path and path not in registered:
        raise ValueError("unknown prompt path")
    if need and (not isinstance(need, str) or len(need)>80 or not need.strip()):
        raise ValueError("invalid need_key")
    if event["outcome"] == "FAIL" and (not isinstance(event.get("failure_code"), str)
                                     or not event["failure_code"].strip()):
        raise ValueError("failed event needs failure_code")
    if "failure_code" in event and (not isinstance(event["failure_code"], str)
                                   or len(event["failure_code"])>80):
        raise ValueError("invalid failure_code")
    for key in ("elapsed_ms", "cost_usd"):
        if key in event and (type(event[key]) not in (int, float) or event[key] < 0):
            raise ValueError("invalid cost/timing")
    return dict(event)

def read_events(path, registry):
    if path is None:
        return []
    events, ids = [], set()
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = validate_event(json.loads(line), registry)
        if item["event_id"] in ids:
            raise ValueError("duplicate event_id at line " + str(n))
        ids.add(item["event_id"])
        events.append(item)
    return events

def discover(events, registry):
    """Suggestions are unverified opportunities; observations aren't authenticated outcomes."""
    for e in events:
        validate_event(e, registry)
    seen = set()
    for e in events:
        if e["event_id"] in seen:
            raise ValueError("duplicate event_id")
        seen.add(e["event_id"])
    real = [e for e in events if e["origin"] == "real"]
    failures, usages = defaultdict(list), defaultdict(list)
    opportunities = []
    for e in real:
        key = e.get("prompt_path") or ("need:" + e["need_key"])
        usages[key].append(e)
        if e["outcome"] == "FAIL":
            failures[(key, e["failure_code"])].append(e)
    for (key, code), group in sorted(failures.items()):
        tasks = {x["task_id"] for x in group}
        if len(tasks) < 2:
            continue
        kind = "new_capability_candidate" if key.startswith("need:") else "repair_candidate"
        opportunities.append(dict(kind=kind, key=key, failure_code=code,
          distinct_tasks=len(tasks), evidence_refs=sorted({x["evidence_ref"] for x in group}),
          status="needs_independent_evaluation",
          next_action="prepare held-out paired trials; no automatic prompt mutation"))
    for key, group in sorted(usages.items()):
        if key.startswith("need:"):
            continue
        # A task is a failure only when all its observations are FAIL.
        # A later PASS, BLOCKED or UNKNOWN must not be overwritten by file order.
        by_task = defaultdict(list)
        for e in group:
            by_task[e["task_id"]].append(e)
        failed_tasks = {task for task, observations in by_task.items()
                        if all(e["outcome"] == "FAIL" for e in observations)}
        if len(by_task) >= 4 and len(failed_tasks) >= 3:
            opportunities.append(dict(kind="retirement_review_only", key=key,
              distinct_tasks=len(by_task),
              failed_distinct_tasks=len(failed_tasks),
              evidence_refs=sorted({e["evidence_ref"] for e in group}),
              status="not_authorized_to_delete",
              next_action="check coverage/confounders and request human retirement decision"))
        passes = [e for e in group if e["outcome"]=="PASS"]
        if len({e["task_id"] for e in passes}) >= 2 and len({e["domain"] for e in passes}) >= 2:
            opportunities.append(dict(kind="reuse_candidate", key=key,
              distinct_tasks=len({e["task_id"] for e in passes}),
              evidence_refs=sorted({e["evidence_ref"] for e in passes}),
              status="needs_independent_evaluation",
              next_action="test transfer on fresh unseen tasks"))
    opportunities.sort(key=lambda x:(x["kind"],x["key"],x.get("failure_code","")))
    return {"verified_usage": 0, "reported_real_events": len(real),
            "synthetic_events_excluded": len(events)-len(real),
            "evidence_authentication": "NOT_PERFORMED",
            "opportunities": opportunities,
            "decision": "NO_EVIDENCE" if not real else "REVIEW_ONLY",
            "zero_usage_cannot_establish_low_value": True}

def plan_probes(registry, events, slot=None, max_items=2, changed_paths=()):
    """Bounded, rotating *plans*, never proof that an evaluation ran.

    Stable UTC-hour slots rotate even with zero observations; changed assets use
    at most one urgent seat, leaving the other seat for coverage. This function
    never executes a prompt, measures latency, or authenticates evidence.
    """
    from datetime import timezone
    if slot is None:
        slot = int(datetime.now(timezone.utc).timestamp() // 3600)
    if type(slot) is not int or slot < 0:
        raise ValueError("slot must be a non-negative UTC hour index")
    if type(max_items) is not int or not 1 <= max_items <= 2:
        raise ValueError("max_items must be 1 or 2")

    usage = defaultdict(set)
    for e in events:
        if e["origin"] == "real" and e.get("prompt_path"):
            usage[e["prompt_path"]].add(e["task_id"])

    assets = {a["path"]: a for a in registry["prompt_assets"]
              if a["status"] != "deprecated"}
    unknown = set(changed_paths) - set(assets)
    if unknown:
        raise ValueError("unknown changed paths: " + ", ".join(sorted(unknown)))

    def track(path):
        domain = path.split("/")[1]
        return "technical" if domain in {"coding", "meta-prompt", "workflow"} else "nontechnical"

    plan, chosen = [], set()
    def add(path, reason):
        if path in chosen or len(plan) >= max_items:
            return
        chosen.add(path)
        item = assets[path]
        plan.append({"track": track(path), "prompt_path": path,
                     "blob_sha": item["blob_sha"],
                     "observed_distinct_tasks": len(usage[path]),
                     "selection_slot_utc_hour": slot, "reason": reason,
                     "status": "PLANNED_NOT_RUN",
                     "required": "run a real task with retained output and independently verifiable outcome"})

    changed = sorted(set(changed_paths))
    if changed:
        add(changed[slot % len(changed)], "changed_asset_priority")

    def choose(paths, reason):
        options = sorted(p for p in paths if p not in chosen)
        if not options:
            return
        least = min(len(usage[p]) for p in options)
        equally_due = [p for p in options if len(usage[p]) == least]
        add(equally_due[slot % len(equally_due)], reason)

    if not changed and max_items == 2:
        # One seat from each track. Each track advances hourly and all members
        # are visited, even when there is no feedback evidence.
        for group in ("technical", "nontechnical"):
            choose([p for p in assets if track(p) == group], "rotating_coverage")
    if len(plan) < max_items:
        # If a changed asset consumed a seat, reserve one for *all* other
        # assets, not only the same track: repeated changes cannot monopolize.
        choose(assets, "rotating_coverage")
    if len(plan) < max_items:
        choose(assets, "rotating_coverage")
    return plan

def run_report(root, registry, events, slot=None, max_items=2, changed_paths=()):
    audit = audit_registry(root, registry)
    feedback = discover(events, registry)
    return {"audit": audit, "feedback": feedback, "probe_plan": plan_probes(registry, events, slot, max_items, changed_paths),
            "production_prompt_changed": False,
            "next_priority": ("repair registry mismatch" if audit["errors"]
                else "collect real cross-domain execution evidence with provenance"
                if not feedback["reported_real_events"] else
                "evaluate highest-priority candidate on held-out tasks")}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command", choices=("audit","report","record"))
    p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument("--registry",type=Path)
    p.add_argument("--events",type=Path,help="explicit JSONL observations path")
    p.add_argument("--event",type=Path,help="a single event JSON for record")
    p.add_argument("--strict",action="store_true")
    p.add_argument("--slot",type=int,help="UTC hour index; default is current UTC hour")
    p.add_argument("--max-items",type=int,default=2,help="maximum planned deep reviews (1 or 2)")
    p.add_argument("--changed-path",action="append",default=[],help="confirmed changed Prompt path; repeatable")
    args=p.parse_args()
    registry=json.loads((args.registry or args.root/"systems/metaloop/registry.json").read_text(encoding="utf-8"))
    if args.command == "record":
        if args.event is None or args.events is None:
            p.error("record requires --event and --events")
        event=validate_event(json.loads(args.event.read_text(encoding="utf-8")),registry)
        old=read_events(args.events,registry) if args.events.exists() else []
        if event["event_id"] in {x["event_id"] for x in old}:
            p.error("duplicate event_id")
        args.events.parent.mkdir(parents=True,exist_ok=True)
        with args.events.open("a",encoding="utf-8") as fh:
            fh.write(json.dumps(event,ensure_ascii=False,sort_keys=True)+"\n")
        result={"recorded_id":event["event_id"],"source_claim":event["origin"],
                "evidence_verified":False}
    elif args.command=="audit":
        result=audit_registry(args.root,registry)
    else:
        result=run_report(args.root,registry,read_events(args.events,registry),
                          args.slot,args.max_items,args.changed_path)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.strict and result.get("status",result.get("audit",{}).get("status"))=="FAIL":
        raise SystemExit(1)

if __name__=="__main__":
    main()
