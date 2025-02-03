# Get all the OpenAI models (deployments) hosted on your Azure subscriptions

Tags: OpenAI, Azure
Publish Date: September 23, 2024

```python
az cognitiveservices account list --query "[?kind=='OpenAI']" | jq -r '.[] | "\(.name) \(.resourceGroup)"' | xargs -n 2 sh -c 'az cognitiveservices account deployment list --name $0 --resource-group $1' | jq -r '.[] | "\(.name) \(.properties.model.name) \(.properties.model.version) \(.id)"'
```
