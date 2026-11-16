# Feature-engineering dataset outputs

This archive preserves the generated JSON outputs from the completed
feature-engineering phase. The source AIS CSV files are not included; they are
local inputs under `CODE/database/`.

The archive contains:

- `database/full/128_fishing_trajs.json`
- `database/full/128_fishing_trajs_ordered_by_id.json`
- `database/full/128_fishing_trajs_wo_redundant_features.json`
- `database/partial/small_fishing_trajs.json`
- `database/partial/small_fishing_trajs_ordered_by_id.json`
- `database/partial/small_fishing_trajs_wo_redundant_features.json`
- `1_training/train.json`
- `2_testing/test.json`
- `3_validation/validation.json`

The compressed tar archive is split into three parts to keep each Git file
below the hosting limit. From the project root, restore the generated files
with:

```bash
cat CODE/phase_artifacts/features_engineering/datasets.tar.gz.part-* \
  | tar -xz -C CODE
```

The concatenated archive SHA-256 is:

```text
7b005121a6166279465e85e0a75c9fb4e86f4853a4ddc5c9630912c3e6345968
```
