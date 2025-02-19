## Demo Script: Federated Credentials Limitations & Solutions in Azure
### Introduction (2 min)
“Hello everyone, my name is [Your Name], and today I’ll be demonstrating how we solved a real-world problem using Flexible Federated Identity Credentials in Azure.

#### The Problem:

Azure Entra has a hard limit of 20 federated identity credentials per application or managed identity.
If you’re using GitHub Actions across multiple repositories, branches, and environments, you can quickly hit this limit.

#### The Solution:

Flexible Federated Identity Credentials allow us to define wildcard-based matching expressions instead of creating multiple individual credentials.
This reduces complexity, improves scalability, and simplifies authentication for GitHub workflows.
By the end of this demo, you’ll see:
- How we set up Flexible Federated Identity Credentials
- How they streamline authentication for GitHub workflows
- Key security considerations for implementation

### Understanding the Problem & Solution (3 min)
“Let’s quickly understand how Federated Identity Credentials work and why we need Flexible Federated Identity Credentials.”

📌 Standard Federated Identity Credentials:

Work by matching Issuer (iss), Subject (sub), and Audience (aud).   
Problem? Each workflow requires a separate credential (quickly reaching the 20-credential limit).   

📌 Flexible Federated Identity Credentials:

Introduce a claimsMatchingExpression.   
Allow wildcards (*) and matching patterns to consolidate multiple use cases into fewer credentials.  

💡 Example:
Instead of one credential per branch, we can define a single credential that covers all branches:

```
claims['sub'] matches 'repo:innersource-nn/*:ref:*'
```
This dramatically reduces credential sprawl while maintaining security.

### Live Demo (5 min)
✅ Step 1: Show Federated Credentials in Azure Entra (1 min)   
“Let’s jump into the Azure Portal and take a look at how these credentials are configured.”

- Navigate to `Microsoft Entra ID → App Registrations → Federated Credentials`.
- Show the credentials and highlight the `claimsMatchingExpression` property.

✅ Step 2: Show GitHub Actions Workflow File (1 min)   
“Now, let’s look at how this integrates with GitHub Actions.”

Open your GitHub repository.
Show the workflow YAML file that references federated identity authentication:
```
permissions:
  id-token: write
  contents: read

jobs:
  test-fed-credentials:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    steps:
      - name: Authenticate to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_NETWORK_DEV_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```
Explain: This workflow requests an OIDC token from GitHub, which Azure validates against our federated credentials.   

✅ Step 3: Run the Workflow (or Show Logs) (2 min)   
“Let’s see it in action!”

Option 1: Trigger a manual run in GitHub Actions → Show logs.   
Option 2: Show logs from a recent run with authentication details:
```
Running Azure CLI Login.
Federated token details:
issuer - https://token.actions.githubusercontent.com
subject claim - repo:NN-Databricks/github:environment:prd
Attempting Azure CLI login by using OIDC...
Subscription is set successfully.
Azure CLI login succeeds by using OIDC.
```
Highlight the subject claim and how it matches the claimsMatchingExpression.   

✅ Step 4: Explain the Test Results (1 min)  

✅ Authentication works for all repositories in the organization.  
✅ Authentication works for branches, pull requests, and environments.  
✅ GitHub Environments modify sub claims, requiring separate credentials:  
```
claims['sub'] matches 'repo:innersource-nn/*:environment:*'
claims['sub'] matches 'repo:innersource-nn/*:pull_request'
```
## Security & Scalability Considerations (3 min)
“Let’s talk about security risks and best practices.”

📌 Security Risks of Wildcards (*):

If unrestricted, any repository could gain access.  
Solution: Restrict who can create repositories in GitHub.

📌 Mitigations Implemented:  
- Restricted Repository Creation: Only Admins & GitHub Apps can create repositories.
- Granular Authentication: Instead of *, we explicitly define environment names when needed:

```
claims['sub'] matches 'repo:innersource-nn/*:environment:prd'
```

📌 Scalability Benefits:
- Fewer Credentials: Instead of 20+, we manage authentication with just 3-5.
- Easier Maintenance: New repositories and workflows automatically inherit authentication rules.

## Conclusion & Next Steps (2 min)
“To wrap things up, here’s what we achieved today:”

✅ We tackled Azure’s Federated Credential limit by using flexible federated identity credentials.  
✅ We streamlined authentication for GitHub Actions with wildcards & claim matching.  
✅ We secured the approach by restricting repository creation & refining access.  

📌 Next Steps:

Fine-tune security policies to minimize wildcard exposure.   
Monitor authentication logs to detect anomalies.   
Automate provisioning of federated identity credentials     

“Thank you for your time! I’d love to take any questions you might have.”

