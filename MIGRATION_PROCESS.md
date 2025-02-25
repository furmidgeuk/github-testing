# GitHub Repository Migration Process

This document outlines the process for migrating repositories from the `NovoNordisk-DataCore` organisation to `NN-Databricks` while supporting incremental updates.

---

## 📋 **Migration Workflow**

```mermaid
graph TD
  A[NovoNordisk-DataCore] -->|Initial Clone & Push| B[NN-Databricks]
  A -->|Changes after Migration| C[Local Clone with Dual Remotes]
  C -->|Fetch Changes| A
  C -->|Push Updates| B
  B -->|Ongoing Development| B
  
  subgraph Final Migration Steps
    D[Final Sync]
    A -->|Fetch Latest Changes| D
    D -->|Push to NN-Databricks| B
    D -->|Archive Old Repo| E[Archive Old Repository]
  end

  subgraph Automation Option
    F[GitHub Actions Workflow]
    F -->|Scheduled Sync| A
    F -->|Auto Push| B
  end
```

## Initial Migration
For the initial migration, we can clone and push.

### Migration Steps
```
# Clone the repository from NovoNordisk-DataCore
git clone --mirror https://github.com/NovoNordisk-DataCore/repo-name.git
cd repo-name.git

# Push to the NN-Databricks
git remote set-url origin https://github.com/NN-Databricks/repo-name.git
git push --mirror
```
- `--mirror` ensures all branches, tags, and history are copied.

## Tracking Changes After Migration
Since changes may happen in both repositories, setting up a way to sync differences later is crucial. The best way is to periodically pull from `NovoNordisk-DataCore` and push to `NN-Databricks`.

### Add Remotes for Tracking

On your local machine or in a github action:
```
# Clone from NN-Databricks
git clone https://github.com/NN-Databricks/repo-name.git
cd repo-name

# Add NovoNordisk-DataCore as a remote
git remote add old-origin https://github.com/NovoNordisk-DataCore/repo-name.git

# Fetch latest changes from NovoNordisk-DataCore
git fetch old-origin
```
## Merging Changes Before Final Cutover

When you're ready to finalize the migration:

### Pull and Push New Changes

```
# Fetch and merge changes from old org
git fetch old-origin
git merge old-origin/main  # or replace 'main' with the relevant branch

# Push changes to the new organization
git push origin main
```
For multiple branches:
```
git branch -r  # List all remote branches
git checkout feature-branch
git merge old-origin/feature-branch
git push origin feature-branch
```
## Automate Incremental Sync with GitHub Actions 
We could set up a GitHub Action in `NN-Databricks` to pull changes from `NovoNordisk-DataCore` automatically:

```
name: Sync from NovoNordisk-DataCore

on:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at midnight
  workflow_dispatch:     

jobs:
  sync-repositories:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo-name: [repo1, repo2, repo3]  # List of repositories to sync

    steps:
      - name: Checkout NN-Databricks Repo
        uses: actions/checkout@v4
        with:
          repository: NN-Databricks/${{ matrix.repo-name }}
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set Up Git
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"

      - name: Add NovoNordisk-DataCore Remote and Sync
        run: |
          git remote add old-origin https://github.com/NovoNordisk-DataCore/${{ matrix.repo-name }}.git
          git fetch old-origin
          git merge old-origin/main --allow-unrelated-histories || echo "No changes to merge"
          git push origin main



```

