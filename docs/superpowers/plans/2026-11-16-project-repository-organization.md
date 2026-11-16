# Project Repository Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` skill to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Put the whole project under one Git root and leave a clean next-phase checkout while preserving the completed feature-engineering results on their own branch.

**Architecture:** Initialize the project folder as the authoritative Git root, import the existing `CODE/` history beneath `CODE/` with `git subtree`, and add the proposal and research materials at the project root. Keep `features_engineering` as the artifact branch, then create `model_training` from it and commit removal of obsolete generated outputs there. Keep downloaded source CSV files and the local virtual environment available for the next phase, but ignore them in Git.

**Tech Stack:** Git, standard `git subtree`, shell `tar`, `gzip`, and `split`.

**Spec:** `docs/superpowers/specs/2026-11-16-project-repository-organization-design.md`

## Global Constraints

- Push `main`, `features_engineering`, and `model_training` to the existing origin with fast-forward updates only; never force-push.
- Preserve all existing Git branch commits and the three pending deletions until their intent is represented in the feature-engineering and next-phase commits.
- Keep generated feature-engineering files and figures recoverable on `features_engineering`.
- Keep each committed artifact file below 90 MiB so the existing GitHub remote can accept future pushes.
- Preserve source CSV inputs and the local Python virtual environment for ongoing work.
- Keep downloaded/generated datasets, Python environments, caches, and LaTeX build intermediates out of normal Git tracking.
- Keep the 3.6 GiB of unreferenced temporary Git objects in the original repository until the root migration and phase branches are verified.

## Review Focus

- A failed migration must leave the original Git branch refs recoverable from a verified bundle and retain the pending deletions as a patch.
- A checkout of `features_engineering` must contain its generated images and the archived generated JSON outputs.
- A checkout of `model_training` must not contain the old figures or feature-engineering data archive, and must preserve the current three file deletions.
- No artifact chunk may exceed 90 MiB; artifact reconstruction instructions must identify all chunks and original paths.
- Existing source CSVs and `AIS_venv/` must remain available locally after migration.

---

### Task 1: Back up current refs and local changes

**Files:**
- Create outside the project: `/tmp/ich-ais-code-before-migration.bundle`
- Create outside the project: `/tmp/ich-ais-code-working-tree.patch`

**Interfaces:**
- Consumes: current repository at `CODE/`, refs `main` and `features_engineering`.
- Produces: a verified Git bundle containing all refs and a binary-safe patch for the three local deletions.

- [ ] **Step 1: Record current state**

Run: `git -C CODE status --short --branch && git -C CODE branch -avv`

Expected: active branch, both local branches, remote-tracking refs, and exactly the three already observed deletions.

- [ ] **Step 2: Save reachable history and working-tree changes**

Run: `git -C CODE bundle create /tmp/ich-ais-code-before-migration.bundle --all`

Run: `git -C CODE diff --binary > /tmp/ich-ais-code-working-tree.patch`

- [ ] **Step 3: Verify the backup**

Run: `git bundle verify /tmp/ich-ais-code-before-migration.bundle`

Expected: bundle verification succeeds and lists the existing refs. Do not remove temporary objects from the original repository.

### Task 2: Package generated feature-engineering datasets

**Files:**
- Create outside the project: `/tmp/ich-ais-fe-datasets.tar.gz`
- Create outside the project: `/tmp/ich-ais-fe-datasets.tar.gz.part-*`

**Interfaces:**
- Consumes: generated JSON files in `CODE/database/` and `CODE/1_training/`, `CODE/2_testing/`, `CODE/3_validation/`.
- Produces: a split gzip-compressed tar archive containing generated JSON outputs, with chunks no larger than 90 MiB and documented extraction instructions.

- [ ] **Step 1: Archive generated JSON outputs**

Package every generated `.json` file currently in the full/partial database directories and the three split directories. Exclude source CSV inputs and the virtual environment. Preserve paths relative to `CODE/` in the archive.

- [ ] **Step 2: Split the compressed archive**

Split `datasets.tar.gz` into sequential parts no larger than 90 MiB. Confirm all parts are present and each is below the limit.

- [ ] **Step 3: Verify archive contents**

List the tar member names and confirm every generated JSON output is included, no CSV input is included, and the archive is readable.

### Task 3: Prepare the project-root repository

**Files:**
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `.gitignore`
- Modify: `docs/superpowers/specs/2026-11-16-project-repository-organization-design.md`
- Keep: `.agents/`, `.aws/`, `.codex/`, and `.vscode/` local and untracked.

**Interfaces:**
- Consumes: project folders `CODE/`, `docs/`, `bibliografia/`, `latex/`, and `FormattingGuidelines-IJCAI-ECAI-26/`.
- Produces: a root navigation page, agent instructions, and root-level ignore rules.

- [ ] **Step 1: Write the root project map**

Create `README.md` with the project purpose, branch map (`features_engineering`, `model_training`), where code/proposal/references live, and the command to enter `CODE/` for Python work.

- [ ] **Step 2: Write shared agent instructions**

Create `AGENTS.md` with the project map, source-vs-generated data rules, phase-branch rules, and an instruction to inspect the active branch before editing phase artifacts.

- [ ] **Step 3: Add root ignore rules**

Ignore local editor/agent state, `.superpowers/`, `CODE/AIS_venv/`, `CODE/database/`, `CODE/1_training/`, `CODE/2_testing/`, `CODE/3_validation/`, Python caches, pytest caches, `CODE/figures/`, LaTeX build directories/intermediates, `.migration/`, and temporary logs. Do not ignore root `docs/`, source PDFs, BibTeX, or `.tex` sources.

- [ ] **Step 4: Confirm source and output boundaries**

Run: `find CODE/database CODE/1_training CODE/2_testing CODE/3_validation -type f -printf '%p %s bytes\\n'`

Expected: source inputs are the two CSV files; generated `.json` files and split JSONs are listed for packaging in Task 2.

### Task 4: Import the existing code repository history

**Files:**
- Create/update: project-root Git metadata and root project files.
- Preserve: old repository history in the verified bundle from Task 1.
- Preserve: the original `CODE/.git` temporary objects until final verification.

**Interfaces:**
- Consumes: root project files, `CODE/` history, and verified bundle.
- Produces: root Git history with imported `CODE/` history and local branches `main` and `features_engineering`.

- [ ] **Step 1: Create a local clone for subtree import**

Clone `CODE/` to a temporary directory outside the project. Confirm the clone has both branches and no uncommitted changes.

- [ ] **Step 2: Initialize the project root**

Initialize Git in the project folder. Record the original `origin` URL for Task 8. Commit only the root project files and materials, excluding `CODE/` and all ignored local state.

- [ ] **Step 3: Move the original working tree out of the target path**

Rename `CODE/` to `.migration/CODE-before-migration/` on the same filesystem. This retains the original metadata, source inputs, environment, and ignored files until final verification.

- [ ] **Step 4: Import the old `main` branch beneath `CODE/`**

Use `git subtree add --prefix=CODE <temporary-clone> main` without `--squash`. Confirm the imported tree contains the old `CODE/` source snapshot.

- [ ] **Step 5: Import feature-engineering history**

Create `features_engineering` from the imported `main` state. Use `git subtree pull --prefix=CODE <temporary-clone> features_engineering` without `--squash`. Confirm the branch contains the existing feature-engineering commits and generated figures.

- [ ] **Step 6: Restore local inputs and environment**

Move the two source CSV files and `AIS_venv/` from `.migration/CODE-before-migration/` into the imported `CODE/`. Do not copy generated JSON outputs; Task 2 archived them.

- [ ] **Step 7: Verify the imported refs and history**

Run: `git branch -avv && git log --oneline --graph --all -12`

Expected: local `main` and `features_engineering` exist and the original commits are visible. Configure the saved origin URL locally, but do not push before Task 8.

### Task 5: Record completed feature-engineering outputs

**Files:**
- Create: `CODE/phase_artifacts/features_engineering/README.md`
- Create: `CODE/phase_artifacts/features_engineering/datasets.tar.gz.part-*`
- Preserve existing tracked images: `CODE/figures/0_features_eng/`
- Modify: `CODE/.gitignore` only if needed for the new root layout.

**Interfaces:**
- Consumes: generated JSON files in `CODE/database/` and `CODE/1_training/`, `CODE/2_testing/`, `CODE/3_validation/`.
- Produces: a split gzip-compressed tar archive containing generated JSON outputs, with chunks no larger than 90 MiB and documented extraction instructions.

- [ ] **Step 1: Document reconstruction**

Write the exact ordered part names, original file paths, and a shell command that concatenates the parts and extracts them beneath `CODE/`.

- [ ] **Step 2: Commit the feature-phase record**

Commit the archive parts and README on `features_engineering`. Keep the existing generated images tracked on that branch. Apply the saved patch from Task 1 and commit the three pending deletions as an explicit cleanup commit, retaining their earlier versions in prior history.

### Task 6: Create the clean next-phase branch

**Files:**
- Create branch: `model_training`
- Remove from this branch: `CODE/figures/0_features_eng/`
- Remove from this branch: `CODE/phase_artifacts/features_engineering/`
- Preserve locally: both source CSVs and `CODE/AIS_venv/`.

**Interfaces:**
- Consumes: completed `features_engineering` branch.
- Produces: a clean `model_training` branch with project materials and current code but without obsolete feature-engineering results.

- [ ] **Step 1: Branch from the completed phase**

Create and check out `model_training` from `features_engineering`.

- [ ] **Step 2: Remove obsolete tracked phase artifacts from this branch**

Delete the tracked feature-engineering figures and artifact archive from this branch and commit the removal. Do not alter the `features_engineering` branch.

- [ ] **Step 3: Confirm generated outputs are absent locally**

The imported code tree does not include these ignored JSON outputs. Confirm the archive exists on `features_engineering`, and do not restore generated outputs into the local worktree. Preserve source CSVs and `CODE/AIS_venv/`.

### Task 7: Final structural verification

**Files:**
- Verify only; no tests or code changes.

**Interfaces:**
- Consumes: root repository and both phase branches.
- Produces: a clean `model_training` checkout and evidence that the feature branch retains artifacts.

- [ ] **Step 1: Verify the current branch is clean**

Run: `git status --short --branch`

Expected: current branch is `model_training` with no generated dataset files or old feature-engineering figures in the worktree.

- [ ] **Step 2: Verify phase artifacts remain on their branch**

Run `git ls-tree -r --name-only features_engineering` and confirm the feature-engineering figures and all dataset archive parts are present.

- [ ] **Step 3: Verify artifacts are absent from the next phase**

Run `git ls-tree -r --name-only model_training` and confirm feature-engineering figures and archive parts are absent.

- [ ] **Step 4: Verify local source inputs remain available**

Run: `find CODE/database -type f -name '*.csv' -printf '%p %s bytes\\n' && test -d CODE/AIS_venv`

Expected: both source CSV files and the local virtual environment remain available.

- [ ] **Step 5: Remove the temporary old worktree after verification**

After the Git bundle, phase archive, branch refs, source CSVs, and virtual environment have all been verified, remove `.migration/CODE-before-migration/` so duplicate outputs and old repository metadata do not remain in the project. Keep the verified bundle and artifact archive in `/tmp` until the final checks pass.

### Task 8: Push the completed branches

**Files:**
- Update remote refs only: `main`, `features_engineering`, `model_training`.

**Interfaces:**
- Consumes: verified local root repository and existing `origin` URL.
- Produces: the three requested branches on the existing GitHub remote.

- [ ] **Step 1: Check push eligibility without writing remote refs**

Run: `git push --dry-run origin main features_engineering model_training`

Expected: all three updates are fast-forward; if any branch is rejected or requires force, stop without pushing that branch.

- [ ] **Step 2: Push all three branches**

Run: `git push -u origin main features_engineering model_training`

Expected: each branch updates successfully without force. Confirm `git status -sb` reports each branch tracking the corresponding `origin` branch.
