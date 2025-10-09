az resource list --resource-type Microsoft.Databricks/accessConnectors -o table


az resource show -g rg-unity-catalog-westeurope -n databricks-connector-unity-catalog-westeurope  --resource-type Microsoft.Databricks/accessConnectors --query id -o tsv
az resource show -g rg-unity-catalog-northeurope -n databricks-connector-unity-catalog-northeurope  --resource-type Microsoft.Databricks/accessConnectors --query id -o tsv

  az resource show \
    -g rg-unity-catalog-westeurope \
    -n databricks-connector-unity-catalog-westeurope \
    --resource-type Microsoft.Databricks/accessConnectors \
    --query identity.principalId -o tsv

  az resource show \
    -g rg-unity-catalog-northeurope \
    -n databricks-connector-unity-catalog-northeurope \
    --resource-type Microsoft.Databricks/accessConnectors \
    --query identity.principalId -o tsv
