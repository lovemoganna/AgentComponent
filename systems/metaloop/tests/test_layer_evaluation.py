"""Second-wave adversarial tests; authored after baseline implementation.
Only deterministic execution is tested here, not LLM prompt quality.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine import execute, compare, promotion, rollback
REGISTRY = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))
SUITE = json.loads((ROOT / "cases/regression.json").read_text(encoding="utf-8"))

class LayerByLayerTests(unittest.TestCase):
    def test_l1_direct_technical_formula(self):
        out = execute({"id":"percent","operation":"percentage_drop","input":{"high":100.0,"low":85.5},"expected":14.5})
        self.assertEqual(out["status"], "PASS")

    def test_l1_sequence_dependency(self):
        out = execute({"route":"sequence","steps":["dedupe_lines","normalize_unicode"],
                       "input":"  清楚 \n  清楚 \n 准确 ","expected":"清楚\n准确"})
        self.assertEqual(out["status"], "PASS")

    def test_l1_parallel_fanout_is_not_concurrent(self):
        out = execute({"route":"parallel","steps":["normalize_ascii","dedupe_lines"],
                       "input":"alpha  beta","expected":["alpha beta","alpha  beta"]})
        self.assertEqual(out["status"], "PASS")

    def test_l1_failed_acceptance_budget_stops(self):
        out = execute({"operation":"normalize_ascii","input":"a\u00a0b",
                       "expected":"a b","repair_candidates":["normalize_ascii","normalize_unicode"],
                       "max_calls":2})
        self.assertEqual(out["status"],"BUDGET_STOP")
        self.assertEqual(out["calls"],2)

    def test_l1_no_external_code_execution(self):
        out = execute({"operation":"run_shell","input":"touch /tmp/pwn",
                       "expected":"done"})
        self.assertEqual(out["status"], "FAIL")

    def test_l2_cross_domain_multistep_comparison(self):
        # Multi-step routing must be comparable without a top-level operation.
        suite = {"cases": list(SUITE["cases"]) + [
            {"id":"new_chain","domain":"technical-analysis",
             "route":"sequence","steps":["dedupe_lines","normalize_unicode"],
             "input":"A\nA\nB","expected":"A\nB"}]}
        report = compare(suite,"normalize_ascii","normalize_unicode")
        self.assertEqual(report["baseline_pass"],6)
        self.assertEqual(report["candidate_pass"],7)

    def test_l2_regression_blocks_promotion(self):
        out=compare(SUITE,"normalize_unicode","normalize_ascii")
        self.assertFalse(out["promotable"])

    def test_l3_no_production_upgrade_without_independent_evidence(self):
        # An in-sample 5/6 -> 6/6 result is not an independent evaluation.
        out=promotion(REGISTRY,SUITE)
        self.assertFalse(out["promoted"])
        self.assertEqual(out["registry"]["text_normalization"]["stable"],"normalize_ascii")

    def test_l3_rollback_without_history_errors(self):
        with self.assertRaises(ValueError):
            rollback(REGISTRY)

    def test_l3_unchanged_candidate_is_noop(self):
        state=json.loads(json.dumps(REGISTRY))
        state["text_normalization"]["candidate"]=state["text_normalization"]["stable"]
        self.assertFalse(promotion(state,SUITE)["promoted"])

if __name__ == "__main__":
    unittest.main()
