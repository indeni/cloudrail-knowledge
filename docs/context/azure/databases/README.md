## Sample rules
A few rules that use objects from this package:

<details>
<summary>non_car_azure_database_public_access</summary>
<summary>non_car_sql_servers_auditing_enabled</summary>
<summary>non_car_mysql_server_enforcing_ssl</summary>
<summary>non_car_postgresql_server_enforcing_ssl</summary>

```python
--8<--
cloudrail/knowledge/rules/azure/non_context_aware/public_access_sql_database_rule.py
cloudrail/knowledge/rules/azure/non_context_aware/my_sql_server_enforcing_ssl_rule.py
cloudrail/knowledge/rules/azure/non_context_aware/ensure_sql_server_audit_enabled_rule.py
cloudrail/knowledge/rules/azure/non_context_aware/postgresql_server_enforce_ssl_rule.py
--8<--
```
</details>

## ::: cloudrail.knowledge.context.azure.databases.azure_sql_server
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.azure.databases.azure_mysql_server
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.azure.databases.azure_mssql_server_extended_auditing_policy
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.azure.databases.azure_postgresql_server
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true