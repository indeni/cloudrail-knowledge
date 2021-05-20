# Cloudrail's Context Model

If you're arrived at this page before reading the [Overview](../README.md), please head there first and come back.

Cloudrail's context model is a set of Python classes, with attributes and methods. When a context is provided by the 
Cloudrail engine to a rule, it will contain many instances of these classes, reflecting the cloud environment being 
analyzed.


## The Mergeable

All context classes inherit, either directly or indirectly, from the 
[Mergeable](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/context/mergeable.py) class. This class implements certain basic concepts needed
to build the context. Specifically:


### Attributes:
* `terraform_state` - an Optional that will contain information about the object's state in Terraform,
if it was loaded from a Terraform plan.
  

* `is_pseudo` - when building the context and connecting objects together, there may be a need to "fill the blanks". For
example, in AWS, we know that an auto-scaling group created through infrastructure-as-code will generate EC2 instances.
How many, and where, depends on the settings of the ASG. Cloudrail parses these settings and generates "pseudo" EC2 
instance objects to represent those instances we know will be spun up once the ASG is actually created. This helps
rules be consistent, without a requirement to do any of these calculations on their own.
  

* `tags` - these are the tags assigned to this resource, whether in the live environment or infrastructure-as-code. Note 
that Cloudrail refrains from collecting most content under tags and so there may be many tags whose name appears 
  correctly, but the value is a result of a hashing function. For example, if you use a tag
  called "my-project-aspect" with the value "foobar-1", Cloudrail will see the tag name but
  will not collect the value "foobar-1".
  

* `aliases` - a context object always has a name. But, sometimes it may be referred by more than one name. If this is 
the case, the other ways to identify the object are stored in aliases. You can look at various classes's code to see 
  where and how aliases are updated.
  `

* `invalidation` - this relates to an internal mechanism of cascading invalidation used within Cloudrail. For example,
imagine a case where Cloudrail scanned a live cloud environment and generated a snapshot. Depending on how dynamic the
  environment is, that snapshot may be internally inconsistent. For example, it's possible that an EC2 instance in it 
  will reference a subnet that no longer exists (as both it, and the EC2 instance, were deleted during snapshot 
  generation). The invalidation mechanism handles this. Any objects that were invalidated will be removed from the 
  context, and so you should never encounter an object with invalidation set. It's here because the same classes are 
  used during context building as well as rule evaluation.
  

### Methods:
* `get_keys()` - generally this is something you wouldn't need in the rule evaluation. This is used by the context's 
  merge functionality to understand two objects are actually the same resource. For example, consider a resource 
  described in Terraform that already exists in the live cloud environment (because `terraform apply` was already run).
  How will Cloudrail understand that both are the same object? In AWS, for example, you could use the ARN 
  (from the Terraform state and the live environment), but many objects don't have an ARN. So, we use "keys" - 
  each resource has a unique way to be identified within an account/region that is not the ARN (or a resource ID in 
  Azure).
  

* `get_type()` - returns the human-friendly text representing the type of this object. This is used for presentation 
purposes.
  

* `get_name()` - the primary name of the object, used for presentation purposes.


* `get_friendly_name()` - used for presentation purposes. Generally, whenever you want to show a resource's name, better
to use this function than `get_name()`, as this function guarantees the output is mean for human consumption.
  

* `get_id()` - the cloud-provided ID of the object if it's from a live environment, or the Terraform id 
if it was generated from a Terraform plan.
  

* `get_extra_data()` - provides additional data about the resource when printed. This is useful in logging, debug 
  information, error messages, etc., and is generally not used in rules.
  

* `get_cloud_resource_url()` - if a resource is from a live environment, this will be the URL that can be used to view
the resource directly in the cloud environment's console. If the resource doesn't exist yet, will return None. This is also
  used for presentation purposes and normally not used in rules.
  

* `is_new_resource()` - returns True if a resource does not yet exist, and the plan calls for it to be created now.


### Properties:
* `origin()` - returns the source of this object - whether from the live environment (through a Dragoneye scan, for 
  example), from infrastructure-as-code, or pseudo (see information about pseudo further above).
  

* `is_managed_by_iac()` - returns True if the resource is managed by infrastructure-as-code (either being created, or 
  already) created.
  

## Supported Cloud Environments

Currently, Cloudrail supports the following cloud environments. We're constantly working to add support for more
environments, more infrastructure-as-code languages, more resource types, and more attributes within resources. (if you want
to join the effort, we're hiring!)

### Amazon Web Services (AWS)

All context objects for AWS inherit from [AwsResource](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/context/aws/aws_resource.py), which in turn 
inherits from [Mergeable](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/context/mergeable.py). You'll notice that it has an attribute of type 
[AwsServiceName](https://github.com/indeni/cloudrail-knowledge/tree/main/cloudrail/knowledge/context/aws/service_name.py), which helps connect the object to the service it 
belongs to. The naming convention used is based on Terraform, but that's just for convenience.

If you're interested in AWS, look at the navigation menu to the left and expand the section called AWS Context.
