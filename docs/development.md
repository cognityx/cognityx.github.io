# Development

Install the portal documentation dependencies and build the landing site:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs build --strict
```

The production workflow builds component sites before invoking
`scripts/build_portal.py`. To add a component, add an entry to
`components.json`, add its page to `mkdocs.yml`, and add a checkout/build step
to `.github/workflows/publish.yml`.

Keep component content in its component repository. Do not copy generated HTML
into this repository.


# How to update doc manually 
# Manually Updating Cognityx Documentation

This guide describes a **VS Code-first process** for safely updating Cognityx documentation.

The **master documentation repository** is the `cognityx.github.io` portal repository. Its authoritative branch is `main`.

---

## Component Repositories

Use this process for documentation belonging to DataForge, Training, Storage, Ingest, and other Cognityx component repositories.

## 1. Select the Repository

1. Open the Cognityx multi-root workspace in VS Code.

2. Open **Source Control** from the left sidebar, or press:

   ```text
   Ctrl+Shift+G
   ```

3. Under **Repositories**, select the repository you want to update, such as:

   ```text
   cognityx-dataforge
   ```

4. Confirm that the **Changes** section is empty.

> **Important:** If unrelated changes are present, stop and finish or commit that work first. Do not automatically stash, discard, clean, or overwrite existing changes.

---

## 2. Synchronize Before Editing

1. Check the branch name in the lower-left corner of VS Code.

2. Click the branch name.

3. Select:

   ```text
   devbb
   ```

4. In **Source Control**, open the `...` menu.

5. Select **Fetch**.

6. Open **Terminal → New Terminal**.

7. Run:

   ```bash
   git status --short --branch
   git fetch origin
   git rebase origin/main
   ```

Continue only when:

* the rebase succeeds;
* there are no unresolved conflicts; and
* `git status` shows a clean working tree.

> **Do not edit documentation directly on `main`.**

The main conflict-prevention rule is:

> **Synchronize `devbb` before changing documentation, not afterward.**

---

## 3. Add or Edit Documentation

1. Expand the selected repository in the VS Code Explorer.
2. Open the `docs/` directory.
3. Edit an existing Markdown file or create a new `.md` file.
4. When adding a new page, open `mkdocs.yml`.
5. Add the page under `nav`.

Example:

```yaml
nav:
  - Home: index.md
  - Introduction: introduction.md
  - New Guide: new-guide.md
  - Reference: reference.md
```

6. Save the changes with:

   ```text
   Ctrl+S
   ```

Keep the repository landing page at:

```text
docs/index.md
```

The landing page should explain, in ordinary language:

* the purpose of the repository;
* the capability it provides;
* where it appears in the Cognityx application flow; and
* how it relates to other components.

> A Markdown page may exist under `docs/` and still be absent from the navigation menu if it is not included in `mkdocs.yml`.

---

## 4. Preview the Documentation

1. Open **Terminal → New Terminal**.

2. Confirm that the terminal is located in the intended repository.

3. Run:

   ```bash
   uv run mkdocs serve
   ```

4. Hold `Ctrl` and click the local URL displayed in the terminal. It is usually:

   ```text
   http://127.0.0.1:8000/
   ```

5. Review:

   * navigation;
   * headings;
   * internal and external links;
   * code examples;
   * tables;
   * readability; and
   * mobile-width rendering.

6. Press `Ctrl+C` in the terminal when the preview is complete.

---

## 5. Run Validation

Run the standard validation commands:

```bash
uv run pytest
uv run mkdocs build --strict
uv build
```

Do not commit the documentation update if any command fails.

For `cognityx-sdk`, also run:

```bash
uv run python scripts/verify_wheel_install.py
```

---

## 6. Review and Commit

1. Return to **Source Control**.
2. Select each changed file and review its diff.
3. Confirm that generated directories such as `site/` are not included.
4. Hover over each intended file and click `+` to stage it.
5. Enter a focused commit message.

Example:

```text
docs: explain dataset publication workflow
```

6. Click **Commit**.
7. Click **Sync Changes**, or select `... → Push`.

> Do not use **Commit All** unless every displayed change belongs to the documentation update.

---

## 7. Create the Pull Request

### Using the GitHub Pull Requests Extension

If the **GitHub Pull Requests and Issues** extension is installed:

1. Click the GitHub Pull Requests icon in the sidebar.

2. Select **Create Pull Request**.

3. Set the base branch to:

   ```text
   main
   ```

4. Set the compare branch to:

   ```text
   devbb
   ```

5. Review the changed files.

6. Enter a clear title and summary.

7. Create the pull request as **Ready for review**, not **Draft**.

8. Open the pull request and inspect the **Checks** section.

9. Merge only after all required checks are green.

10. Use **Squash and merge** unless the repository requires another merge method.

### Using the Terminal

If the extension is unavailable, run:

```bash
gh pr create --base main --head devbb
gh pr checks --watch
```

---

## 8. Synchronize After Merge

A squash merge creates a new commit on `main`. Do not continue working from the old `devbb` history.

1. Ensure the working tree is clean.

2. Open the VS Code terminal.

3. Fetch the merged branch:

   ```bash
   git fetch origin
   ```

4. Recreate or realign `devbb` from the updated `origin/main` according to the Cognityx branch workflow.

5. Confirm the result:

   ```bash
   git status --short --branch
   git log --oneline --decorate -3
   ```

The expected result is:

* a clean `devbb` branch; and
* a current commit aligned with the merged `main` branch.

---

# Portal Repository

Use the `cognityx.github.io` repository when changing:

* the shared homepage;
* architecture pages;
* the component directory;
* portal styling;
* discovery scripts;
* link-checking scripts; or
* the publication workflow.

> Do not manually copy generated component documentation into the portal repository.

The portal obtains component documentation from the default `main` branch of each component repository.

---

## 1. Select and Synchronize the Portal Repository

1. Open **Source Control**.

2. Select:

   ```text
   cognityx.github.io
   ```

3. Confirm that there are no pending changes.

4. Click the branch name in the lower-left corner.

5. Select:

   ```text
   devbb
   ```

6. Select `... → Fetch`.

7. In the integrated terminal, run:

   ```bash
   git fetch origin
   git rebase origin/main
   ```

Continue only when the branch is clean and synchronized.

---

## 2. Choose the Correct File

Use the following locations:

| Location                        | Purpose                                          |
| ------------------------------- | ------------------------------------------------ |
| `docs/`                         | Shared portal documentation pages                |
| `docs/index.md`                 | Portal landing page                              |
| `docs/architecture.md`          | Overall Cognityx architecture                    |
| `components.json`               | Component names, descriptions, and URL prefixes  |
| `docs/stylesheets/`             | Portal presentation and styling                  |
| `.github/workflows/publish.yml` | Documentation publication automation             |
| `scripts/`                      | Component discovery, assembly, and link checking |
| `site/`                         | Generated output; do not edit or commit          |

Avoid editing generated files under `site/`.

---

## 3. Validate and Publish Portal Changes

1. Edit the required source files.

2. Review every change in **Source Control**.

3. Run the portal's documented validation commands.

4. Stage only the intended files.

5. Commit the changes on `devbb`.

6. Push `devbb`.

7. Create a ready-for-review pull request from:

   ```text
   devbb → main
   ```

8. Wait for the **Publish documentation PR build** to pass.

9. Merge only after all required checks are green.

10. Wait for the subsequent `main` deployment to complete.

---

# Force a Manual Portal Rebuild

Normally, merging component documentation into `main` automatically dispatches a portal rebuild.

To trigger a rebuild manually from VS Code:

1. Open **Terminal → New Terminal**.

2. Run:

   ```bash
   gh workflow run publish.yml \
     --repo cognityx/cognityx.github.io \
     --ref main
   ```

3. Find the new workflow run:

   ```bash
   gh run list \
     --repo cognityx/cognityx.github.io \
     --workflow publish.yml \
     --limit 5
   ```

4. Copy the newest run ID.

5. Watch the run:

   ```bash
   gh run watch RUN_ID \
     --repo cognityx/cognityx.github.io \
     --exit-status
   ```

6. Verify the published component at:

   ```text
   https://cognityx.github.io/<component>/
   ```

Example:

```text
https://cognityx.github.io/dataforge/
```

---

# Conflict-Prevention Rules

* Always fetch and rebase from `origin/main` before editing.
* Never begin when Source Control already shows unrelated changes.
* Never edit directly on `main`.
* Keep one focused documentation commit where practical.
* Avoid editing the same paragraph as another open pull request.
* Check for an existing `devbb → main` pull request before starting.
* Rebase again if `main` advances before you push.
* Never commit generated `site/` output.
* Never use **Discard Changes**, `git clean`, or automatic stashing unless you deliberately intend to remove or relocate that work.
* After a squash merge, recreate or realign `devbb` from the updated `origin/main`.

---

# If a Conflict Appears

1. Stop before pushing.
2. Open **Source Control**.
3. Expand **Merge Changes**.
4. Click each conflicted file to open the VS Code Merge Editor.
5. Compare the local documentation with the incoming `origin/main` version.
6. Preserve both changes when they address different content.

> Do not blindly select **Accept All Current** or **Accept All Incoming**.

7. Save the resolved file.

8. Stage it using the `+` button.

9. Continue the rebase:

   ```bash
   git rebase --continue
   ```

10. Run the complete validation suite again.

11. Push with `--force-with-lease` only when the rebase intentionally rewrote already-pushed `devbb` history:

```bash
git push --force-with-lease origin devbb
```
