"""AWS portability checks. Run: pytest -q"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
def test_contract_columns():
    c = json.load(open(ROOT/"contracts/openfda_fact_contract_v1.0.0.json"))
    cols = {x["name"] for x in c["columns"]} if isinstance(c.get("columns"), list) else set(c["columns"])
    assert {"safetyreportid","primary_drug","is_serious","n_reactions"} <= cols
def test_three_cloud_metrics_match():
    r = json.load(open(ROOT/"proofs/proof_3cloud_business.json"))
    recon = r.get("business_metric_reconciliation", {})
    for k,v in recon.items():
        assert v.get("all_match"), f"{k} differs across clouds"
