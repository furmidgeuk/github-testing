# GitHub Repository Migration Process

This document outlines the process for migrating repositories from the `NovoNordisk-DataCore` organisation to `NN-Databricks` while supporting incremental updates.

---

## 📋 **Migration Workflow**

```mermaid
graph TD
  A[Old GitHub Organization] -->|Initial Clone & Push| B[New GitHub Organization]
  A -->|Changes after Migration| C[Local Clone with Dual Remotes]
  C -->|Fetch Changes| A
  C -->|Push Updates| B
  B -->|Ongoing Development| B
  
  subgraph Final Migration Steps
    D[Final Sync]
    A -->|Fetch Latest Changes| D
    D -->|Push to New Org| B
    D -->|Archive Old Repo| E[Archive Old Repository]
  end

  subgraph Automation Option
    F[GitHub Actions Workflow]
    F -->|Scheduled Sync| A
    F -->|Auto Push| B
  end



1. Initial Migration
For the initial migration, you can either use GitHub’s built-in transfer feature (if you want to keep issues, PRs, stars, etc.) or manually clone and push (if you prefer more control). Here’s the manual approach that works well for selective control:

Manual Migration Steps
