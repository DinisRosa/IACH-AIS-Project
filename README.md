# IACH AIS Project

Project on fishing-activity detection from AIS vessel trajectories, developed
for the Human-Centred Artificial Intelligence course.

## Project map

- `CODE/` — Python pipeline, data preparation, experiments, and detailed usage
  instructions in [`CODE/README.md`](CODE/README.md).
- `docs/` — proposal reviews, project plans, and design notes.
- `bibliografia/` — research papers used by the project.
- `latex/` — proposal sources, bibliography, and final proposal PDF.
- `FormattingGuidelines-IJCAI-ECAI-26/` — conference LaTeX style files.

## Phase branches

- `main` — project baseline and shared materials.
- `features_engineering` — completed feature-engineering phase, including its
  figures and archived generated datasets.
- `model_training` — next phase; feature-engineering outputs are omitted from
  this working tree and remain available on `features_engineering`.

Check the current branch before working with phase outputs:

```bash
git status --short --branch
```

Keep phase-specific results on their phase branch. Push updates normally; do
not force-push or rewrite shared branch history.

## Data and setup

Downloaded AIS CSV inputs and generated datasets are local under `CODE/` and
are ignored by Git. The generated feature-engineering JSONs can be restored
from the archive on the `features_engineering` branch; see
`CODE/phase_artifacts/features_engineering/README.md`.

For dependencies and pipeline commands, follow [`CODE/README.md`](CODE/README.md).
