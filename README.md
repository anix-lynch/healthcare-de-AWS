# healthcare-de-AWS

> **openFDA drug-safety on AWS serverless — the same data, the AWS outfit (Bullet 6 / multicloud portability).**
> The exact openFDA fact that runs on GCP BigQuery and Microsoft Fabric is landed in **S3** (typed Parquet)
> and served from **DynamoDB** (PAY_PER_REQUEST) — then reconciled so counts, business metrics, and the
> contract-column schema match across all three clouds. Cost < $0.0001, teardown documented.

## Repo Map
```
healthcare-de-AWS/
├── aws/         aws_portability.py — land openFDA in S3 + serve from DynamoDB (--teardown to remove)
├── contracts/   the shared openFDA fact contract (same one GCP + Fabric load)
├── reconcile/   reconcile_3cloud.py — read each cloud's ACTUAL schema, validate, reconcile metrics
├── terraform/   the AWS slice as IaC (S3 + DynamoDB, 30-day expiry)
├── proofs/      AWS portability receipt + 3-cloud business reconciliation + reconcile diagram
├── tests/       contract + cross-cloud metric checks (pytest)
├── README.md
└── LICENSE
```

## What it proves
- **Two serverless services** — openFDA lands in S3 (typed Parquet) and serves from DynamoDB (on-demand); no RDS/OpenSearch/ECS/always-on.
- **The truth survives the move** — record_count, serious_count, serious_rate, distinct_drugs, total_reactions reconcile exactly GCP = Fabric = AWS (`proofs/proof_3cloud_business.json`), each computed independently on its own cloud.
- **Schema is enforced, not asserted** — each cloud's ACTUAL schema is fingerprinted from real data and validated against the contract file.
- **Cheap + reversible** — cost < $0.0001 (on-demand + tiny S3), with `--teardown` / `terraform destroy`.

## Run (creds: AWS `~/.aws` default profile, GCP SA, Fabric owner `az login`)
```bash
pip install boto3 pandas pyarrow google-cloud-bigquery deltalake
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
AWS_REGION=us-east-1 GCP_PROJECT_ID=<proj> python3 aws/aws_portability.py   # S3 + DynamoDB
python3 reconcile/reconcile_3cloud.py                                       # actual-schema + metric reconcile
```

## Honest scope
n=300 real openFDA reports. Terraform is a definition (validate in CI; this env has no terraform binary).
