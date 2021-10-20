## Cloudrail knowledge workflow

### intro
This document should provide basic steps for a knowledge developer how to develop new rules for Cloudrail.

### Understanding the requirements
The first thing you have to do when being assigned with a ticket, is to make sure you fully understand it.
Contact the Reporter or Yoni, to make sure you know how to do it.

### Data sources ("raw data")
Currently, Cloudrail will fetch and analyze data from 2 sources: Cloudmapper data, Terraform plan data.
* Cloudmapper data is a set of data being parsed after fetched from AWS account using API calls.
* Terraform plan data is the data which is created from a Terraform template, before deploy in the cloud.

We have the option to create the data we need manually, however, we should look first at the folder `tests.knowledge/context/aws/cross_version`, and check if it's already there or not.

You should use AWS and Hashicorp documentation, to make sure how the data you need should look like. 
Useful links:
* https://docs.aws.amazon.com/
* https://registry.terraform.io/providers/hashicorp/aws/latest/docs

### Code structure
The current code has the following flow:
1. Collecting data from the aforementioned data sources.
2. Parse it, and extract all possible data and values.
3. Reconstruct the data needed to run rules over it (created this data is called a "resource" or "entity").
4. If needed, make sure to link between all data and context (Subnets to it's VPC for example).

Our main work will be at step 3, and sometimes step 4 as well.   

### How to create resources
In order to check the way in which our "raw_data" is parsed, and how we can manipulate it, we need to run some code which invoke the "builders", and insert breaking point were we need.
The builders functions for each data source (cloudmapper / Terraform) are located at: `common/environment_context_builder.py`.

* Steps:
    * Enter inside each builder function.
    * Locate the relevant builder you want to add new resource (example: ec2_builder).
    * Get inside this builder, and modify it, in order to have your new resource part of it.

### Create new rule
* Each new rule file should be created under the location: /core/policies/rules/types.
* Each rule must include the following 4 methods:
    * get_id - Will return the name of the rule, as specified in the ticket.
    * execute - The actual logic which will run against the resource, and trigger an alert.
    * get_issue_description - Will return a message with the number of problematic items.
    * get_needed_parameters - Will provide the type of resource, in case needed (can be blank as well).

At the end of the execute function, we need to use the function “Issue”, with the following arguments, which are provided in the Jira ticket:
Evidence String Format, Exposed Resource,  Violating Resource.

The rule description should be add to the file: `core/rules/aws_rules_metadata.yaml`, the needed information to fill, appear in the Jira ticket.
* rule_id - "Rule ID" in the ticket.
* name - "Rule Friendly Name" in the ticket.
* description: "Rule Description" in the ticket.

At the end, you will need to add the new rule class, into the file: `/core/policies/types/internet_connection_policy.py`.
This action will attach the rule into some policy (currently we only have one). 

## Tests
The strategy to test Cloudrail Knowledge is by getting use cases in terraform file from product that showcase the different support scenario that Cloudrail need to support

### Basic test flow
(Before the test start we will download the modified terraform bin from Cloudrail S3 bucket - being done automatically by the test framework)
* run `terraform init`
* run `terraform plan`
* run `terraform show`
* Create context from the created Json
* run the rule
* Assert the results

### How to create new rule test
* Create a new folder for the rule that you would like to test under `tests.knowledge/rules/<your_rule_name>/`
* Create a python file to add your test cases `test_<your_rule_name>.py`
* for each test scenario that product provided create a folder that contain the terraform resources
  * for instance under `tests.knowledge/rules/<your_rule_name>/` we will have the following folders:
    * `test_case_1` that contains `main.tf`
    * `test_case_2` that contains `main.tf`
* Each test case should use a `test_case` folder

### How to create new context test
* Create a new folder for the component that you would like to test for example `tests.knowledge/context/aws/cross_version/ec2`
* Create a new folder for the scenario that you would like to test for example `tests.knowledge/context/aws/cross_version/ec2/in_subnet`
* If the scenario is different on specific terraform version, add a folder for example `tests.knowledge/context/aws/v2.70/ec2/in_subnet`
* Add the tf files under the scenario folder.
* The tf files should not contain region section. The deafult region is `us-east-1`
* Run and apply the tf files on lite environment.
* Run cloud mapper on the environment using `cloud_mapper_collect_helper.py` and copy the output folder to the scenario folder.

### How to run in IntelliJ/PyCharm if you use aws-vault
First of all, you SHOULD use aws-vault :)

Use this plugin to load AWS credentials from aws-vault when running tests: https://pypi.org/project/patch-env/
