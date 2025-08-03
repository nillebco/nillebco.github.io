---
tags:
  - terraform
  - devops
date: 2025-01-17
published: true
---

# terraform: event grid subscription for a service bus topic

When terraforming an event grid subscription to a service bus topic, you might get an error like the following - not very clear.


```shell

Error: creating/updating Scoped Event Subscription
(Scope: "/subscriptions/********---**-**********/resourceGroups/<resource-group>/providers/Microsoft.EventGrid/topics/<event-grid-topic>"
Event Subscription Name: "<event-subscription-name>"): polling after CreateOrUpdate: polling failed: the Azure API returned the following error:
Status: "Failed"
Code: "Internal error"
Message: "The operation failed due to an internal server error. The initial state of the impacted resources (if any) are restored. Please try again in few minutes. If the error still persists, report <error-id>:<timestamp> (UTC) to our forums for assistance or raise a support ticket."
Activity Id: ""

--- API Response: ----[start]----
{
  "id": "https://management.azure.com/subscriptions/********-****-****-****-************/providers/Microsoft.EventGrid/locations/<location>/operationsStatus/<operation-id>?api-version=2022-06-15",
  "name": "<operation-id>",
  "status": "Failed",
  "error": {
    "code": "Internal error",
    "message": "The operation failed due to an internal server error. The initial state of the impacted resources (if any) are restored. Please try again in few minutes. If the error still persists, report <error-id>:<timestamp> (UTC) to our forums for assistance or raise a support ticket."
  }
}
-----[end]-----
```


Such an error may arrive **because you are trying to set an identity for the event grid subscription**.

The shortest sample about an event grid subscription associated to a service bus topic follows. Setting a delivery_identity or a dead_letter_identity will result in an Internal Server error raised by the Azure API, without any other explanation.


```hcl
locals {
	region = {
		nickname = "weu"
		name = "WestEurope"
	}
	env = "dev"
	app = "app"
	tags = ["fun", "learning"]
}

data "azurerm_servicebus_namespace" "ops" {
  name                = "asb-ops-${local.env}-${local.region.nickname}"
  resource_group_name = "rg-ops-${local.env}-${local.region.nickname}"
}

resource "azurerm_eventgrid_topic" "this" {
  name                          = "eg-topic-${local.app}-${local.env}-${local.region.nickname}"
  location                      = var.region.name
  public_network_access_enabled = false
  resource_group_name           = module.resource_group.name
  tags                          = local.tags
}

resource "azurerm_eventgrid_event_subscription" "this" {
  name                 = "test"
  scope                = azurerm_eventgrid_topic.this.id
  included_event_types = ["items.create", "items.update"]

  service_bus_topic_endpoint_id = "${data.azurerm_servicebus_namespace.ops.id}/topics/project"

  retry_policy {
    max_delivery_attempts = 30
    event_time_to_live    = 1440
  }
}

```
