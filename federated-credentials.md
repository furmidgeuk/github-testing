# Report on Federated Credentials Limitations and Solutions in Azure

## **Background**
Azure imposes a hard limit of `20 federated credentials` per `service principal`, which presents challenges when authenticating multiple GitHub repositories across various environments. To address this limitation, we explored several strategies and tested configurations to identify a scalable and secure solution.

## **Strategies Considered**

### **1. Use Multiple Service Principals**
- **Approach:** Instead of relying on a single service principal, multiple service principals handle different subsets of repositories and environments.
- **Example:**
  - `service-principal-1` → Handles `Repo A`, `Repo B`, `Repo C` (DEV, TST)
  - `service-principal-2` → Handles `Repo A`, `Repo B`, `Repo C` (VAL, PRD)
- **Pros:**
  - Avoids hitting the federated credentials limit.
  - Aligns with RBAC and security best practices.
- **Cons:**
  - Increased management overhead due to multiple SPs.

### **2. Use a Wildcard Subject Claim**
- **Approach:** Utilize wildcard claims (e.g., `repo:org/*`) to include multiple repositories under a single credential.
- **Pros:**
  - Reduces the number of federated credentials required.
  - Automatically includes new repositories.
- **Cons:**
  - Less granular control.
  - Potential security risks if improperly restricted.

### **3. Use Environment-Level Federation**
- **Approach:** Assign federated credentials based on environments rather than repositories.
- **Example:**
  - `dev-federated-cred`: Covers all repositories for DEV.
  - `tst-federated-cred`: Covers all repositories for TST.
  - `val-federated-cred`: Covers all repositories for VAL.
  - `prd-federated-cred`: Covers all repositories for PRD.
- **Pros:**
  - Simplifies credential management.
- **Cons:**
  - Still limited to 20 federated credentials.
  - Requires environment-based GitHub Actions conditions.

### **4. Combine Strategies**
- **Approach:** Implement a mix of multiple service principals, wildcard claims, and environment-based federation.

## **Testing and Findings**

To leverage Azure's **Flexible Federated Identity**, we configured **Claims Matching Expressions (Preview)** and tested various approaches.

### **Tested Claims (Unsuccessful Attempts)**
- `claims['sub'] matches 'repo:<organisation>/*' and claims['sub'] matches 'environment:*'`
- `claims['sub'] matches 'repo:<organisation>/*' and claims['sub'] eq 'environment:dev'`
- `claims['sub'] matches 'repo:<organisation>/*:ref:refs/heads/main'`
- `claims['sub'] matches 'repo:<organisation>/*:ref:*'`
- `claims['sub'] matches 'repo:<organisation>/*:ref:refs/heads/*'`

### **Final Working Solution**
Since GitHub Environments modify the `sub` claim format, we created **two separate federated identity credentials**:

#### **Federated Credential 1 (Branch-Based Workflows)**
```plaintext
claims['sub'] matches 'repo:<organisation>/*:ref:*'
```
- Allows authentication for any repository in the organization for branch-based workflows.

#### **Federated Credential 2 (Environment-Based Workflows)**
```plaintext
claims['sub'] matches 'repo:<organisation>/*:environment:*'
```
- Allows authentication for GitHub Environments.

### **Further Refinements**
To increase granularity, we can:

1. Restrict to the **main branch only**:
   ```plaintext
   claims['sub'] matches 'repo:<organisation>/*:ref:refs/heads/main'
   ```

2. Specify **individual environments**:
   ```plaintext
   claims['sub'] matches 'repo:<organisation>/*:environment:dev'
   claims['sub'] matches 'repo:<organisation>/*:environment:tst'
   claims['sub'] matches 'repo:<organisation>/*:environment:val'
   claims['sub'] matches 'repo:<organisation>/*:environment:prd'
   ```

3. Attempting to combine environments into a single claim failed:
   ```plaintext
   claims['sub'] matches 'repo:<organisation>/*:environment:dev' and claims['sub'] matches 'repo:<organisation>/*:environment:tst'
   ```
   - The `and` operator does not work with multiple `sub` claims.

### **Testing Results**
The solution was tested successfully in the `https://github.com/innersource-nn/nn-databricks-playground` repository with the following claims:
```plaintext
claims['sub'] matches 'repo:innersource-nn/*:ref:*'
claims['sub'] matches 'repo:innersource-nn/*:environment:*'
```
- Authentication worked across all repositories and branches in combination with all environments.

## **Conclusion and Next Steps**
This approach provides a **scalable** and **manageable** solution to Azure’s federated credential limit. While it is currently well within the `20` federated credential limit, continuous monitoring and refinements may be required as the number of repositories and environments grow.

### **Next Steps:**
1. Further **granular control** by refining claims.
2. Evaluate **security implications** of wildcard-based authentication.
3. Automate **credential provisioning** to streamline future updates.

This approach balances **security**, **scalability**, and **manageability** while complying with Azure’s limitations on federated credentials.

