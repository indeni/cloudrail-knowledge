## Sample rules
A few rules that use objects from this package:

<details>
<summary>s3_acl_disallow_public_and_cross_account</summary>

```python
--8<--
cloudrail/knowledge/rules/aws/context_aware/public_access_validation_rules/s3_acl_allow_public_access_rule.py
--8<--
```
</details>
<details>
<summary>s3_lambda_indirect_exposure</summary>

```python
--8<--
cloudrail/knowledge/rules/aws/context_aware/indirect_public_access_rules/s3_bucket_lambda_indirect_exposure_rule.py
--8<--
```
</details>
<details>
<summary>vpc_endpoint_s3_exposure</summary>

```python
--8<--
cloudrail/knowledge/rules/aws/context_aware/vpc_endpoints/vpc_endpoint_gateway_not_used_rule.py
--8<--
```
</details>

## ::: cloudrail.knowledge.context.aws.s3.public_access_block_settings
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_acl
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_bucket
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_bucket_access_point
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_bucket_encryption
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_bucket_object
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_bucket_regions
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true

## ::: cloudrail.knowledge.context.aws.s3.s3_bucket_versioning
    rendering:
      show_root_toc_entry: false
    selection:
      inherited_members: true
