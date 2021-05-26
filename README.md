![CD](https://github.com/indeni/cloudrail-knowledge/actions/workflows/ci.yaml/badge.svg) 
![PyPI](https://img.shields.io/badge/python-3.7+-blue.svg)
![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

# Cloudrail Knowledge
[Cloudrail](https://www.indeni.com/cloudrail) is a tool for doing security analysis of infrastructure-as-code before 
its deployment. For example Cloudrail can inspect Terraform plans and identify configurations 
that violate company policy and best practices, and stop the CI pipeline accordingly.

This repository contains the rules that Cloudrail runs to conduct this analysis, as well as the context model the rules 
evaluate against. You can use this repository for a few purposes:
1. Review the rules Cloudrail has and how they work.
2. Propose additions/changes to rules (just open a PR).
3. Build your own custom rules using the same context model existing rules use (for examples see 
   [cloudrail-sample-custom-rules](https://github.com/indeni/cloudrail-sample-custom-rules))
   
Want to understand how Cloudrail's knowledge works? Our documentation is available at 
[https://knowledge.docs.cloudrail.app/](https://knowledge.docs.cloudrail.app/).

## Contributing
We welcome all contributions. Simply open an issue and a PR with your additions or changes. Some requirements:
* Branch names should be `<ticket-id>_<what_it's_trying_to_solve>`. Such as `issue_40_add_docdb_encryption_rule` or 
  `40_add_docdb_encryption_rule`.
* Any rule must have tests, see the `tests` directory on how these are built.

## Releases
This repository has frequent releases. Those with "beta" or "b" in their name are considered still in development,
not yet included in the production Cloudrail code (running in the Cloudrail SaaS). The latest non-beta release is
the one currently running within Cloudrail's production service.