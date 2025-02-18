# Security Implications of Wildcard-Based Authentication
## Broad Access Scope
Using wildcards in [federated identity credentials](https://learn.microsoft.com/graph/api/resources/federatedidentitycredentials-overview) increases flexibility but can also inadvertently grant `overly broad access`. For example:

The pattern `claims['sub'] matches 'repo:furmidgeuk/*:ref:*'` allows authentication for `all repositories` within the organization, rather than specific ones.
This increases the risk of unauthorized access if an unintended repository or workflow needs to be restricted.
## Increased Risk of Credential Compromise
If a repository or workflow is compromised (e.g., through a supply chain attack or malicious actor pushing code to an allowed branch), an attacker may be able to exploit the wildcard authorization to gain access to Azure resources.

### Mitigation:

- Restrict credentials to `specific repositories` instead of `*` when possible.
- Use GitHub branch protection rules to prevent unauthorized changes in critical branches.

## Exposure of Secrets via Unauthorized Workflows
By allowing `any branch or environment` to authenticate, an attacker could:

- Fork a repository.
- Push malicious code to a non-monitored branch.
- Trigger a workflow that authenticates using federated credentials.
- Exfiltrate secrets or perform unauthorized Azure actions.
### Mitigation:
- Enforce `protected environments` in GitHub to require manual approvals for sensitive operations.
- Implement `least privilege` access to ensure that federated credentials can only be used for necessary operations.

## Difficulty in Auditing and Monitoring
Wildcards make it harder to track exactly which workflows are using federated credentials. This could lead to:

- Difficulty in identifying and revoking unnecessary access.
- Challenges in enforcing `role-based access control (RBAC)` for different repositories and environments.

### Mitigation:
- Use `Azure Conditional Access Policies` to limit authentication by conditions such as IP address, device compliance, or other risk-based signals.
- Regularly review `audit logs` in both GitHub and Microsoft Entra ID to track authentication attempts.

## Limited Granular Control Over Environments
GitHub Environments modify the sub claim format, making it challenging to enforce `fine-grained controls`. If a single wildcard-based credential is used across multiple environments, an attacker could escalate privileges by switching environments.

### Mitigation:
- Define separate federated credentials for each `critical environment` (e.g., `dev`, `tst`, `val`, `prd`).
- Enforce `GitHub Environment Protection Rules`, requiring approvals before deploying to higher environments.

## Future Proofing Against Azure Policy Changes
While flexible federated credentials provide an efficient way to scale, `Azure may enforce stricter policies in the future`. Over-reliance on wildcards may lead to a `breaking change` if Microsoft updates how federated identity credentials work.

### Mitigation:
- Regularly monitor `Microsoft Entra ID updates` for changes to federated identity authentication.

## Final Recommendations
- `Use specific repository names` where possible instead of `*`.
- Limit `credentials to specific branches` (`refs/heads/main` instead of `refs/heads/*`) where possible.
- `Restrict credentials by environment` rather than using one wildcard for all.
- `Enable environment protection rules` to prevent unauthorized deployments.
- `Monitor and audit federated identity usage` regularly to detect anomalies.
