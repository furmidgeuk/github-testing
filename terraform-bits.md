cat > backend.tfvars <<'EOF'
resource_group_name  = "rg-terraform-state"
storage_account_name = "epamdbxterraformdev"
container_name       = "tfstate"
key                  = "epam-unity-catalog.tfstate"
tenant_id            = "f4499f23-474a-4e92-bb59-54f5187fb300"
subscription_id      = "ccf37c3d-4ace-4fd7-888f-e989dad8a342"
EOF

az login
az account set --subscription "ccf37c3d-4ace-4fd7-888f-e989dad8a342"

terraform init -input=false -backend-config=backend.tfvars    

terraform plan -refresh=false -lock=false -input=false -var-file prd.tfvars

terraform plan -refresh=false -lock=false -input=false -var-file prd.tfvars -out main.tfplan     


terraform apply -refresh=false -lock=false -input=false -var-file prd.tfvars     
