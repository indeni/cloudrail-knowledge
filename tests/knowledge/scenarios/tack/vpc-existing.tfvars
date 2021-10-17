# # This is merged in with terraform.tfvars for override/existing VPC purposes.  Only to be used in conjunction with modules_override.tf

# The existing VPC CIDR range, ensure that the the etcd, controller and worker IPs are in this range
 cidr.vpc = "10.0.0.0/16"

# etcd server static IPs, ensure that they fall within the exisiting VPC public subnet range
 etcd-ips = "10.0.0.10,10.0.0.11,10.0.0.12"

# # Put your existing VPC info here:
 vpc-existing {
 	id = "vpc-033a54f26ef5e2b4a"
 	gateway-id = "igw-0aac1021f62ae6f50"
 	subnet-ids-public = "subnet-0e474b5158094e961"
 	subnet-ids-private = "subnet-0e474b5158094e961"
 }
