# User guide 
**This guide expand the document [User Guide](https://github.com/NovoNordisk-DataCore/github/blob/main/documentation/user_guide.md)**
## Objective: Manage the organization's configuration.
  - The `github` repository implements the code to deploy the repositories, Teams, Members,... 
    - The action to refresh the deployment: `.github/workflows/main.yaml`
  - The `dc-terraform-bootstrap` repository has the terraform code to support the `github` deployments.
    - This repository will be used from other workflows(outside this repository) to Init, Plan, or Apply terraform infrastructure.

## Bootstrap your organization
Prerequisites:
  - You must have the following:
    1. You request a GitHub organization (request from NN GitHub's Service Now).
       - You are the Admin of the organization. 
         - You need this role for step iii.
         - This role allows you to check what will be implemented in the GitHub organization.
    2. You have or request an Azure subscription (request from NN Azure's Service Now)
       - Service Now Creates the `Entra ID application(EntraApp)` and related `Service Principal(EntraSP)` with a custom `Contributor` role assigned at the Azure subscription level.
       - You need to create or use an existing storage account to save the terraform state file of the deployments.
    3. You create, manually a __GitHub App__ with the configuration values `apps.admin` in [configuration.yaml](https://github.com/NovoNordisk-DataCore/github/blob/main/configuration.yaml) file.
        - The link to creates the **GitHub App** will be: https://github.com/organizations/ORG/settings/apps, where ORG = your new organization.
        - At the organization level, in actions you create 3 secrets, with the `GH_ADMIN_APP_ID`, `GH_ADMIN_APP_INST_ID`, and `GH_ADMIN_PRIVATE_KEY` value of the __GitHub App__.
          -  `GH_ADMIN_APP_ID` is the ID of the GitHub App.
          -  `GH_ADMIN_APP_INST_ID` is the installation ID of the GitHub App(different from App ID).
          -  `GH_ADMIN_PRIVATE_KEY` is Base64 encoded of the pem(Private key) generated for the GitHub App.
              -  You can generate the Base64 encoded value using [base64encode.org](https://www.base64encode.org)
          - The `.github/actions/token/action.yaml__` in the `github` repository uses the `GH_ADMIN_APP_ID` and the `GH_ADMIN_PRIVATE_KEY` values to generate a temporary token to access the organization.   
       - `configuration.yaml`
         ```             
         apps:
           ...

         admin:
           # NOTE: this app must be deployed _before_ this repository is first deployed. This is part of a common
           # "bootstrap circular problem" is addressed by doing this deployment manually first.
           # See installation verification in the test strategy for how to bootstrap.
           name: DataCore GitHub Admin
           description: System identity of DataCore to read from GitHub
           home_url: https://novonordisk.com
           # no webhook
           permissions:
             repository_permissions:
               administration: read_and_write
               contents: read_and_write
               metadata: read
               # so environments can be read and created in the repository
               environments: read_and_write
               actions: read
               issues: read_and_write
               pull_requests: read_and_write
             organization_permissions:
               administration: read_and_write
               custom_organization_roles: read_and_write
               metadata: read
               members: read_and_write
               # to manage org variables
               variables: read_and_write
           scope: enterprise # Where can this GitHub App be installed? -> This enterprise
         ```

 
This organization configuration will be made in three phases.
- Phase 1: Download the `dc-terraform-bootstrap` and `github` repositories from an existing organization ex: `NovoNordisk-DataCore`
- Phase 2: Deploy from local machine 
  - `dc-terraform-bootstrap` 
    - The user must have a Contributor role in the Azure subscription or resource group where the storage account will be created.
  - `github`
    - The user must have a `Storage Blob Data Contributor` role in the storage account container created from the `dc-terraform-bootstrap` deployment.
      - In this way, you can have the terraform state file saved in the storage account container by setting up the terraform backend configuration.
        - If it's not possible to have this role you can deploy saving the state file locally and after the deployment is done you can copy the state file in the storage account container.
- Phase 3: You push the `dc-terraform-bootstrap` and `github` repositories from the local machine to the new GitHub organization.
  - If there is any problem pushing from the local repositories to the new ones created:
    - Download the new empty repositories `github` and `dc-terraform-bootstrap`.
    - Create a branch and check out the branch
    - Copy the files, commit, and push.
    - Create a pull request
- Phase 4: Deploy and refresh the organization configuration with the `github` actions.   
  - You must assign to the `EntraSP` the `Storage Blob Data Contributor` role in the container where the terraform state file will be.
       - You need to implement the **Federated credentials** for the `EntraApp`. 
         - The `Federated credentials` can be set in the `Certificates & secrets` of the `EntraApp`.
         - The configuration must done for the `github` and `dc-terraform-bootstrap` repository.

### Steps

1. Clone [`dc-terraform-bootstrap`](https://github.com/NovoNordisk-DataCore/dc-terraform-bootstrap) and deploy it (from local machine)
  - You can execute the code below(`sh deploy.sh`) if you have enough permissions(Contributor role) in the resource group where the storage account will be created. 
  - In Novo Nordisk, you must belong to a Entra ID group, to deploy into Azure,
  - The `main.bicep` and `<environment>.bicepparam` files deploy a storage account.
      - `deploy.sh`:
        ```
        set -euo pipefail
        resourceGroup=$1
        environment=$2

        az group create --name ${resourceGroup} --location westeurope

        az deployment group create \
          --resource-group ${resourceGroup} \
          --template-file main.bicep \
          --parameters ${environment}.bicepparam
        ```
      - `dev.bicepparam`:
        ```
        using 'main.bicep'

        param environment = 'dev'
        param principalId = '4a7ee345-16e0-4a08-a191-7e4959ca8888' // IaCAgent-datacore-DEV
        param principalType = 'ServicePrincipal'
        param principalGroupId = '7343aeaf-1b60-4b29-9179-50f20a53be2a' // clinical_data_datacore-platform_admins
        ```      
    - Some improvements can be made in the bicep files:
       - enable a delete lock at the storage account level or resource group level
         - Increase the security by preventing resource deletion.
2. Clone [`github`](https://github.com/NovoNordisk-DataCore/github)
3. Change `configuration.yaml` so both `github` and `dc-terraform-bootstrap` repositories are of type `mirror`
  - The  `configuration.yaml` file has a section to configure the **variables** for actions at the organization(GitHub) level:
    - These variable will be used by the pipelines.
    ```
    variables:
      # non-secrets common across the repositories
      ARM_SUBSCRIPTIONS:
        value: |
          {
            "dev": "...subscription_id...",
            "tst": "...subscription_id...",
            "val": "...subscription_id...",
            "prd": "...subscription_id..."
          }
        visibility: all
      TF_REMOTE_STATE:
        value: |
          {
            "dev": {
                "resource_group_name": "...",
                "storage_account_name": "...",
                "container_name": "...",
                "tenant_id": "...",
                "subscription_id": "..."
            },   
            "tst": { ... }
            "val": { ... }
            "prd": { ... }
    ```
  - The  `configuration.yaml` file has a section to configure the **secrets** for actions at the organization(GitHub) level:
    - At the moment this section is not deployed by the terraform code.
      - Unfortunately, this resource has a serious bug that makes it unusable for us, check the [issue](https://github.com/integrations/terraform-provider-github/issues/1383)
    - <ins>Before running the pipelines you must manualy create the secrets presents in the `configuration.yaml` in the organization's actions<ins>.
4. deploy `github` (from local machine)
  - The terraform backend state will be saved in the storage account created by the bicep code above.
  - Before running the commands below you must have the Azure roles:
    - Contributor at Subscription level.
    - Storage Blob Data Contributor at the container level.
      - Container where the state file will be saved.
  - Configure the terraform `github` provider as below:
     ```
     provider "github" {
       owner = local.configuration.name
       app_auth {
         id              = GitHub App ID
         installation_id = GitHub App installation ID
         pem_file        = file('GitHub App primary key file')
      }
    }
     ```
  - Commands: 
    ```
       az login -t '<tenant-id>' 
       az account set -s '<subscription-id>'
       terraform fmt --recursive
       terraform init \
       -backend-config="storage_account_name=<bicep created>" \
       -backend-config="container_name=<bicep created>" \
       -backend-config="key=<environment>.tfstate" \
       -backend-config="resource_group_name=$resourceGroup" 
       terraform validate
       terraform plan -out="<environment>.plan"
       terraform apply <environment>.plan
    ```
    - **After the deployment and before push you must remove the `app_auth` section.**
5. Push `dc-terraform-bootstrap` from your local machine to the new GitHub organization.
   -   or copy the files as mentioned in 'Phase 3'
6. Push `github` from your local machine to the new GitHub organization.
   -   or copy the files as mentioned in 'Phase 3'

At this point, you have:

1. An Azure remote state backend and GitHub workflow template to use it.
2. A git repository `github` that, when deployed from the `main` branch, updates your GitHub configuration.
   - For the 'github' repository, we should consider the following:
     - Create a recurring action, such as every 6 hours, to verify the repository configurations and identify any changes.
3. A GitHub organization configured to meet specific process controls required for using DataCore's release framework.
