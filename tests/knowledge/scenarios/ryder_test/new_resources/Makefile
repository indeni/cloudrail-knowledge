.PHONY: init
init:
	@terraform init

.PHONY: plan
plan:
	@terraform plan --var-file="demo.tfvars"

.PHONY: test
test:
	@echo "Running static assessment"
	@cloudrail run --auto-approve

.PHONY: apply
apply:
	@AWS_PROFILE=indeni terraform apply --auto-approve --var-file="demo.tfvars"

.PHONY: destroy
destroy:
	@AWS_PROFILE=indeni terraform destroy --auto-approve --var-file="demo.tfvars"
