# Instructions for project agents

## Start here

- This repository's root is the project root.
- Use [`README.md`](README.md) for the project map and branch roles.
- Python code and its setup instructions are under `CODE/`; read
  [`CODE/README.md`](CODE/README.md) before changing the pipeline.

## Branch and artifact rules

- Before editing, inspect `git status --short --branch` and preserve existing
  changes.
- Choose the branch for the phase being changed before editing. Use `main` for
  shared project structure and instructions; use the phase branch for phase
  code, analyses, figures, and generated results.
- `features_engineering` is the completed feature-engineering record. Its
  generated figures under `figures/0_features_eng/` and dataset archive under
  `CODE/phase_artifacts/features_engineering/` belong on that branch.
- `model_training` is the next working phase. Do not restore obsolete
  feature-engineering outputs into its working tree.
- Keep future phase outputs on the matching phase branch. Never force-push or
  rewrite shared branch history.
- `CODE/database/`, `CODE/1_training/`, `CODE/2_testing/`, and
  `CODE/3_validation/` contain local inputs or generated data and are ignored
  by Git. Preserve the source CSV inputs; regenerate or restore derived JSON
  data only when needed.

## Researching across branches

- Do not switch branches just to inspect their history or files. Read the
  branch list and commit graph first:

  ```bash
  git branch --list
  git log --oneline --decorate --graph --all
  ```

- Search a path's history across all branches with
  `git log --all --oneline -- <path>`.
- Search a term in another branch with `git grep -n "<term>" <branch> -- <path>`.
- Read a file from another branch without checking it out with
  `git show <branch>:<path>`.
- Compare phase implementations with
  `git diff <older-branch>..<phase-branch> -- <path>`.
- Before starting new work, check whether the code, analysis, or result already
  exists on another branch. Reuse its documented findings where applicable;
  do not copy phase outputs into the active branch just to inspect them.
- If a branch switch is necessary, first make sure the worktree is clean and
  local inputs are safe. Never discard uncommitted work to change branches.

## Commits and pushes

- Keep each commit focused on one phase or one shared project change. Do not
  mix feature-engineering and model-training code or results in the same
  commit.
- Stage only the intended paths. Avoid `git add .`: local datasets and
  generated files may be present even though they are ignored.
- Before committing, inspect `git status --short`,
  `git diff --cached --stat`, and `git diff --cached --check`.
- Use commit messages in the form `type(phase): short action`, for example
  `feat(model_training): add baseline classifier` or
  `docs(project): clarify branch workflow`. For shared instructions, use
  `docs(project)` and commit on `main`.
- Commit phase outputs only on the branch that produced them. Keep the
  feature-engineering archive and figures on `features_engineering`; do not
  add them to `model_training`.
- After a shared change on `main`, merge it into the affected phase branches
  and check that phase-specific outputs remain on their original branch.
- Push only committed work to its matching `origin` branch. Use a normal
  fast-forward push; never force-push. Check `git status --short --branch`
  after pushing.

## Project materials

- Keep research sources in `bibliografia/`, proposal sources in `latex/`, and
  project decisions in `docs/`.
- Leave downloaded datasets, virtual environments, caches, and LaTeX build
  intermediates out of commits.
- Make project-specific changes only when they support the user's current
  request; do not reorganize unrelated code or research material.
