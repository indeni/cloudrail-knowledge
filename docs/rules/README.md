# Cloudrail Rules

If you're arrived at this page before reading the [Overview](../README.md), please head there first and come back.

Rules in Cloudrail are written using Python code. All rules inherit from [BaseRule](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/rules/base_rule.py)
which provides a set of basic capabilities and requirements. Generally, rules don't inherit
from other classes, unless there's a set of rules that are largely the same with minor
parameter differences.

## Metadata

Every rule has metadata information that is required:

* **rule_id** - this is the unique machine-readable identifier of the rule. No two
    rules may have the same ID. 
    Should follow the syntax : [car/non_car]_[rule abbreviated].
    For example: non_car_iam_no_permissions_directly_to_user
  
  
* **name** - this is the human-friendly name of the rule. It will be presented anywhere
    the rule is shown to the user. It should be kept short, one sentence, without the period,
    and be one-line only.

  
* **description** - a multi-line human-friendly description of what the rule is about - 
    why it exists and what it's trying to catch. Normally, this field does not contain
    how the rule actually works.


* **rule_type** - either `context_aware` or `non_context_aware`. Context-aware rules
    are ones that use data from more than one resource to make a determination. For example,
    if a logic requires the rule to check resource A, find its reference to resource B,
    then check B, then it's a context-aware rule. For more information, see 
    [What is considered a "Context Aware Rule"?](context-aware.md).


* **severity** - the severity of the rule, one of Major, Medium, Low.
    * Major - The rule should be enabled ASAP.
    * Medium - The rule should be enabled soon, but requires more input and does not present an immediate security risk.
    * Low - General best practices that can be tackled later on. These rules tend to have more negligible if left untouched for a month.


* **security_layer** - for the purpose of categorizing rules, we identify the layer
    that is being inspected. For a full list of options, look at SecurityLayer under
    the [rule_metadata](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/rules/rule_metadata.py). You may ask
    for more options to be added to the list.


* **resource_types** - for the purpose of categorizing rules, we identify the type of
    resource the rule is targeting. For a full list of options, look at ResourceType under
    the [rule_metadata](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/rules/rule_metadata.py). You may ask
    for more options to be added to the list.
  

* **cloud_provider** - rules generally target only one specific cloud provider. 
    For a full list of options, look at the 
    [CloudProvider enum](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/context/cloud_provider.py).
  

* **logic** - describes the busines logic behind the rule. For example, if the rule 
    requires that Cloudrail should look at every region to see if an S3 bucket exists 
    and if certain ACLs are in place, you would describe it as 
    “Cloudrail will scan for S3 buckets used within each region and for each bucket, 
    identify what bucket ACL is used. For each Bucket and Bucket ACL, 
    Cloudrail will look at the permissions to identify if the Bucket is accessible.”
  

* **compliance** - decorates the rule with information on what compliance frameworks,
    and specific controls within them, are addressed by this rule. For example, for
    a rule that addresses control 1.2 in PCI DSS version 3.2.1, as well as control 
    5.2 in CIS version 1.3.0, the metadata will look like this:
```
  compliance:
    "PCI DSS":
      "3.2.1": "1.2"
    "CIS":
      "1.3.0": "5.2"
```
  

* **iac_remediation_steps** - the remediation steps to take within the Terraform code
    to resolve the issue identified by this rule.
  

* **console_remediation_steps** - the remediation steps to take within the cloud console
    (such as AWS console or Azure portal) to resolve the issue identified by this rule.


## Evidence, Exposed and Violating Resources

When a rule finds a violation, it records an [Issue](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/rules/base_rule.py). The Issue contains
three important fields:

* **violating** - a pointer to the resource that was found to be violating the rule. 
    It is the object with the configuration that was necessary to determine the violation.

  
* **exposed** - a resource is “exposed” if it is “affected” by the violation. 
    The exposed resource should be treated as the resources that would be “affected” as a 
    result of the violation itself.
  

* **evidence** - The evidence field is responsible for surfacing all the data points used as part of the evaluation.
    There's a bit of logic that goes into the creation of this field and it has a specific 
    formatting syntax. For more details, see [Structure of Evidence Field](evidence.md).
  
## The actual code

The rules are written in Python. You'll notice that the structure of a rule is
pretty straightforward. There are a few main functions that are needed:

* **get_id(self) -> str** - this simply returns the rule_id of this rule. It is used to match
    the rule Python class with the metadata of the rule.
  

* **execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]** -
    this is where the main rule logic actually runs. The rule gets the environment context
    and can access all of the context information within it (for more information on context, 
    see [Context](../context/README.md)). At the moment, the `parameters` are ignored. The exeecute function
    returns a list of issues it found (the list may be empty, if no issues found).


* **should_run_rule(self, environment_context: EnvironmentContext) -> bool** - 
    before running a rule, the rule should make sure it has resources in the context to run on.
    We do this to not only improve performance, but also flag rules as "skipped" if this function returns
    False. That way, we can convey to users what actual rules were relevant for their environment.

  
## Writing rules

You can write and use your own code in two main ways:

* Contribute new rules, or modifications to existing ones, straight into the 
  [cloudrail-knowledge](https://github.com/indeni/cloudrail-knowledge) repository. These contributions
  will be made available to all Cloudrail users.
  
  
* Create custom rules that are used only in your environment. A sample of such
    rules is available in the [cloudrail-sample-custom-rules](https://github.com/indeni/cloudrail-sample-custom-rules)
    repository.
  
The easiest way to start writing a rule is by copying an existing one that does something
similar. Notice that a rule also has a test associated with it under the [tests](/tests) directory.

Want to get started with your first rule? Follow [our tutorial](tutorial/README.md).