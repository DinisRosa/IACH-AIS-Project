# Project repository organization

## Intent

Make the project easier for people and agents to navigate, and preserve the
best state of each project phase on its own Git branch. Feature-engineering
outputs should remain recoverable on that phase's branch but should not clutter
the working tree for the next phase.

## Goals

- Use one Git root for the complete project so agents find code, proposal,
  literature, and project instructions from one checkout.
- Preserve the existing `CODE/` Git history and its phase branches.
- Keep generated feature-engineering artifacts in the
  `features_engineering` branch; omit obsolete outputs from the next-phase
  working branch.
- Make generated data, caches, virtual environments, and LaTeX build products
  easy to recognize and keep out of the normal working tree/versioned files.
- Add concise root-level instructions and a project map for agents.

## Non-goals

- Force-pushing or replacing remote history.
- Deleting source material or permanently destroying the old Git metadata.
- Redesigning the AIS processing code or changing research results.

## Constraints and current state

- The current Git repository is `CODE/`, with local branches `main` and
  `features_engineering`, and remote `origin`.
- The `features_engineering` history already contains commits adding and
  restoring its generated figures. The local `features_engineering` checkout
  has three pending deletions: `0_features_eng/constants.py`,
  `0_features_eng/partition_dataset.py`, and `0_features_eng/visualizations.py`.
  These must be preserved as pending user changes and not silently committed or
  discarded.
- Local `main` and `features_engineering` point at different historical
  snapshots; this needs an explicit branch migration plan.
- The workspace root contains the proposal, reference PDFs, formatting files,
  LaTeX sources/build products, and additional feature-engineering notes.
- The project root has an empty `.git` directory, while Git metadata under
  `CODE/.git` is currently read-only in the sandbox. Git metadata changes may
  require an approved elevated command during implementation.

## Approaches

1. **One repository at the project root (selected).** Import the `CODE/`
   history beneath `CODE/`, preserve phase history, and include the project
   materials in the same repository. This gives agents one root and retains
   the existing work, with a one-time local migration cost.
2. **Keep `CODE/` as the Git root.** This preserves the remote layout and
   requires the least Git migration, but leaves proposal/research materials
   outside the repository and makes the full project harder to navigate from
   a checkout.
3. **Keep two linked repositories.** This avoids history migration but leaves
   agents navigating two roots and adds coordination overhead between them.

The project-root repository is selected because the requested outcome is a
simple project workspace for both people and agents, while the existing code
history can be preserved under a `CODE/` path. The user authorized committing
all project changes and pushing the migrated `main`, `features_engineering`, and
new `model_training` branches to the existing remote. Push only fast-forward
updates; do not force-push or rewrite remote history.

## Proposed branch organization

- Retain a `features_engineering` phase branch containing the completed phase's
  code and generated figures/results that are intentionally part of that
  phase's record.
- Create a next-phase branch from that state, presumed to be `model_training`
  based on the existing `1_training/` structure. The branch begins with the
  feature-engineering implementation but omits obsolete generated outputs
  from its working tree. The phase branch remains available for historical
  review and recovery.
- Keep `main` as the integration/base branch after reconciling its existing
  history; do not silently reset or overwrite it.
- Do not commit the three pending deletions until their intent is represented
  in the branch design and reviewed in the concrete migration plan.

## File organization and tracking

- Keep source documents, bibliography, proposal sources, and required
  conference style files in the project repository.
- Keep generated datasets, downloaded source datasets, virtual environments,
  Python caches, LaTeX intermediates, and temporary logs out of normal
  version control.
- Keep only phase outputs deliberately selected for the phase record on that
  phase's branch. Remove them from the next-phase checkout through Git history
  on that branch, not by deleting their historical phase-branch versions.
- Add a root `AGENTS.md` with the project map and branch/artifact rules, plus a
  concise root README as the first navigation point.

## Implementation choices left to the builder

- Exact history-import and branch-reconciliation commands, with a recoverable
  backup of the existing `CODE/.git` metadata before any migration.
- Exact file allowlist for generated figures and LaTeX outputs after checking
  references in the source documents.
- Exact `.gitignore` rules and root README/agent-instruction wording.
- Configure the existing origin in the new root repository and push the three
  requested branches only after confirming each update is a fast-forward.

## Approval status

Approved by the user on 2026-11-16. No repository files or Git metadata have
been changed as part of this design.
