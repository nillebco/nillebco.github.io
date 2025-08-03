---
tags:
  - terraform
date: 2024-12-16
published: true
---

# Terraform Cloud sensitive variables? forget about that

In Terraform Cloud you have the possibility to mark variables as **sensitive**. This is supposed to hide them from outputs and only allow you to set a new value.

In reality, you can proceed as follows to get the sensitive variable value. This procedure assumes that you already have a sensitive variable defined, and that its value is set

1. define a new variable, check hcl
2. let its value empty
3. trigger a plan

In the plan's error message you'll get the sensitive variable output.

This has been shared with Terraform Cloud support and flagged as **intended design**. I find this disappointing in the sense that

- secrets and sensitive values are supposed to be safe under all circumstances
- if, for organizational reasons, the person who sets the secrets is not the same managing runs and applies, this issue makes your processes unsafe
- a fix would be easy to implement (group the variables by sensitive, and use two distinct variable groups; if the sensitive group fails, then hide its output)
