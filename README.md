# maap-organization-buckets

Infrastructure for deploying organization-specific S3 buckets with AWS CDK.

## Project Layout

```text
maap-organization-buckets/
├── app.py
├── stacks/
│   └── buckets_stack.py
│   └── logs_stack.py
├── organizations/
│   └── organization_name/
│       ├── bucket_policies.py (optional)
│       └── lifecycle_rules.py (optional)
├── defaults/
│   ├── lifecycle_rules.py
│   └── bucket_policies.py
├── cdk.json
├── pyproject.toml
├── README.md
└── runtime_config.py
```

## How It Works

- `app.py` discovers org names from folders under `organizations/` and creates one stack per org.
- `stacks/buckets_stack.py` defines a single-org stack that deploys one bucket.
- `stacks/logs_stack.py` defines a single bucket for storing server access logs of all org buckets.
- Bucket naming convention is `nasa-maap-{org}`. {org} is derived from the org folder name.
- `defaults/` stores baseline bucket policy and lifecycle rules.
- `organizations/` stores custom policy statements and lifecycle policies per org.

## Define Organization Buckets

Each org has:

- `bucket_policies.py`: optional org-specific policy statements.
- `lifecycle_rules.py`: optional org-specific lifecycle rules.

Generated bucket names follow:

`nasa-maap-<org-name>`

## Contributing

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Add a new org:

   - Create `organizations/<org-name>/`
   - Optionally add `bucket_policies.py` and `lifecycle_rules.py`

3. Verify changes:

   ```bash
   uv run cdk synth
   ```

4. Run pre-commit hooks:

   ```bash
   pre-commit run --all-files
   ```

5. Commit and push your changes.
