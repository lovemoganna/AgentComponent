import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"systems/metaloop"))
from lifecycle import audit_registry, blob_sha, discover, run_report, validate_event, read_events, plan_probes

REGISTRY=json.loads((ROOT/"systems/metaloop/registry.json").read_text(encoding="utf-8"))

def event(event_id, task_id, outcome="FAIL", path="prompts/writing/explain/explain-with-asd-ste100.md",
          domain="nontechnical", origin="real", failure_code="missing_fact", need_key=None):
    e={"event_id":event_id,"task_id":task_id,"domain":domain,
       "event_time":"2026-11-10T10:30:00+08:00","origin":origin,"outcome":outcome,
       "evidence_ref":"artifact:"+event_id}
    if need_key:
        e["need_key"]=need_key
    else:
        e["prompt_path"]=path
    if outcome=="FAIL":
        e["failure_code"]=failure_code
    return e

class LifecycleTests(unittest.TestCase):
    def test_probes_cover_technical_and_nontechnical(self):
        plan=plan_probes(REGISTRY,[])
        self.assertEqual({x["track"] for x in plan},{"technical","nontechnical"})
        self.assertTrue(all(x["status"]=="PLANNED_NOT_RUN" for x in plan))
        self.assertTrue(all(x["observed_distinct_tasks"]==0 for x in plan))

    def test_probes_shift_to_less_observed_asset(self):
        original=plan_probes(REGISTRY,[])
        writing=next(x for x in original if x["track"]=="nontechnical")
        observed=event("w1","actual_task_1","PASS",path=writing["prompt_path"])
        changed=plan_probes(REGISTRY,[observed])
        self.assertNotEqual(writing["prompt_path"],
          next(x for x in changed if x["track"]=="nontechnical")["prompt_path"])

    def test_registry_complete_and_hash_frozen(self):
        audit=audit_registry(ROOT,REGISTRY)
        self.assertEqual(audit["status"],"PASS",audit["errors"])
        self.assertEqual(audit["prompt_files"],14)
        self.assertEqual(audit["registered"],14)
        self.assertEqual(audit["by_status"]["stable"],1)
        self.assertEqual(audit["by_status"]["candidate"],1)

    def test_sha_verifies_git_blob(self):
        self.assertEqual(blob_sha("test\n"),"9daeafb9864cf43055ae93beb0afd6c7d144bfa4")

    def test_missing_registry_detected(self):
        reg=json.loads(json.dumps(REGISTRY))
        reg["prompt_assets"].pop()
        self.assertEqual(audit_registry(ROOT,reg)["status"],"FAIL")

    def test_hash_tamper_detected(self):
        reg=json.loads(json.dumps(REGISTRY))
        reg["prompt_assets"][0]["blob_sha"]="0"*40
        self.assertTrue(any("hash_mismatch" in x for x in audit_registry(ROOT,reg)["errors"]))

    def test_no_observations_means_no_claims(self):
        out=run_report(ROOT,REGISTRY,[])
        self.assertEqual(out["feedback"]["decision"],"NO_EVIDENCE")
        self.assertEqual(out["feedback"]["opportunities"],[])
        self.assertFalse(out["production_prompt_changed"])

    def test_repeated_real_failure_becomes_candidate(self):
        out=discover([event("a","one"),event("b","two")],REGISTRY)
        self.assertEqual(out["opportunities"][0]["kind"],"repair_candidate")
        self.assertEqual(out["opportunities"][0]["status"],"needs_independent_evaluation")

    def test_single_task_duplicates_do_not_trigger(self):
        out=discover([event("a","one"),event("b","one")],REGISTRY)
        self.assertEqual(out["opportunities"],[])

    def test_synthetic_events_excluded(self):
        out=discover([event("a","one",origin="synthetic"),event("b","two",origin="synthetic")],REGISTRY)
        self.assertEqual(out["opportunities"],[])
        self.assertEqual(out["synthetic_events_excluded"],2)

    def test_new_missing_capability_candidate(self):
        out=discover([event("a","one",need_key="cross_language_qa"),
                      event("b","two",need_key="cross_language_qa")],REGISTRY)
        self.assertEqual(out["opportunities"][0]["kind"],"new_capability_candidate")

    def test_transfer_candidates_require_two_domains(self):
        p=event("a","one","PASS")
        q=event("b","two","PASS",domain="technical")
        out=discover([p,q],REGISTRY)
        self.assertEqual(out["opportunities"][0]["kind"],"reuse_candidate")

    def test_low_value_review_not_delete(self):
        ev=[event(str(i),str(i)) for i in range(4)]
        out=discover(ev,REGISTRY)
        self.assertTrue(any(x["kind"]=="retirement_review_only" for x in out["opportunities"]))
        self.assertFalse(any(x["status"]=="deleted" for x in out["opportunities"]))

    def test_reject_raw_user_content(self):
        x=event("a","one")
        x["raw_prompt"]="sensitive data"
        with self.assertRaises(ValueError):
            validate_event(x,REGISTRY)

    def test_reject_unknown_asset(self):
        x=event("a","one",path="prompts/unknown.md")
        with self.assertRaises(ValueError):
            validate_event(x,REGISTRY)

    def test_reject_unaware_timestamp(self):
        x=event("a","one")
        x["event_time"]="2026-11-10T10:30:00"
        with self.assertRaises(ValueError):
            validate_event(x,REGISTRY)

    def test_record_duplication_detection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"events.jsonl"
            item=event("a","one")
            p.write_text(json.dumps(item)+"\n"+json.dumps(item)+"\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                read_events(p,REGISTRY)

if __name__=="__main__":
    unittest.main()
