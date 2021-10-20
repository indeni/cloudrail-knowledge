# # Overrides the vpc module in the modules.tf, just loads the variables defined for the existing vpc and reuses those
# #
# # Uncomment to enable the override
module "vpc" {
   source = "./modules/vpc-existing"
   azs = "us-east-1a"
   cidr = "10.1.1.0/24"
   name = "sfdc-somestage-consoleme"
   region = "us-east-1"
   id = "vpc-033a54f26ef5e2b4a"
   gateway-id = "${ var.vpc-existing["gateway-id"] }"
   subnet-ids-public = "${ var.vpc-existing["subnet-ids-public"] }"
   subnet-ids-private = "${ var.vpc-existing["subnet-ids-private"] }"
 }
