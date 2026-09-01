# Terraform Networking Interview Track

## A. Purpose and audience

This standalone track prepares SDE2 and Staff candidates to explain how Terraform models, plans, owns, tests, and safely changes networking infrastructure across AWS, Google Cloud, and F5 BIG-IP. It is an educational learning track, not a production runbook. Provider names and versions are examples; verify current behavior before using any command.

## B. Ordered learning path

1. [Terraform core and execution model](01-terraform-core-and-execution-model.md)
2. [Providers, versions, and authentication](02-providers-versions-and-authentication.md)
3. [State, backends, locking, and workspaces](03-state-backends-locking-and-workspaces.md)
4. [Resources, data sources, modules, and composition](04-resources-data-modules-and-composition.md)
5. [Plan, apply, lifecycle, and safe change](05-plan-apply-lifecycle-and-safe-change.md)
6. [Import, moved blocks, and drift recovery](06-import-moved-blocks-and-drift-recovery.md)
7. [AWS networking with Terraform](07-aws-networking-with-terraform.md)
8. [GCP networking with Terraform](08-gcp-networking-with-terraform.md)
9. [F5 BIG-IP provider and AS3 boundaries](09-f5-big-ip-provider-and-as3-boundaries.md)
10. [Multi-provider platform patterns](10-multi-provider-platform-patterns.md)
11. [Testing, policy, CI/CD, and security](11-testing-policy-cicd-and-security.md)
12. [Debugging, rollback, cost, and interview loops](12-debugging-rollback-cost-and-interview-loops.md)
13. [Real-world Terraform exercises](14-real-world-terraform-exercises.md)
14. [Real-world exercise answer key](15-real-world-exercise-answer-key.md)
15. [A10 load balancers and Terraform](16-a10-load-balancers-and-terraform.md)
16. [Cisco networking and Terraform](17-cisco-networking-and-terraform.md)
17. [Spine-leaf switching and fabric as code](18-spine-leaf-switching-and-fabric-as-code.md)
18. [Cisco NSO service models and Terraform](19-cisco-nso-service-models-and-terraform.md)

## C. How this track fits the repository

The [cloud networking track](../cloud-networking-interview/00-README.md) explains network architecture and provider setup. The [F5 automation topic](../book/topics/33-f5-api-and-automation-toolchain.md) explains API/tooling choices. This track adds the Terraform ownership layer: state addresses, provider schemas, plans, imports, drift, lifecycle, policy gates, and safe orchestration. Cross-link rather than memorize duplicate definitions.

## D. Safety and example posture

Examples use placeholder accounts, projects, partitions, IDs, and documentation addresses. They may create billable or mutable resources if adapted. Never place credentials in HCL, variables committed to Git, plan artifacts, screenshots, or shell history. Prefer short-lived identity, disposable environments, reviewed plans, explicit approvals, and read-back verification. Examples intentionally avoid broad deletion and `-auto-approve`; cleanup is discussed as a separate, dependency-aware decision.

## E. Entry diagnostic and completion gates

Before starting, explain the difference between configuration, state, remote reality, and application health; explain why a plan is not a guarantee; and describe why an F5 AS3 declaration and individual `bigip_*` resources must not co-own the same object.

You are ready for SDE2 interviews when you can produce a reviewed plan, trace a provider error to evidence, explain import and drift, and define a rollback boundary. You are ready for Staff interviews when you can also separate state ownership across teams/providers, quantify blast radius and cost, design a CI approval model, and defend a migration with measurable gates and recovery evidence.

## F. Practice method

For every module, read the portable model before provider names. Then inspect the HCL, predict the plan, state what the provider would verify, identify what the plan cannot prove, and answer the questions aloud. Finish both exercises: one plan/design drill and one debugging/rollback drill. Add a **Fact**, **Vendor terminology**, or **Inference** label to each provider-specific claim.

The final two files are deliberately practice-heavy. Attempt the eight real-world scenarios without opening the answer key, draw the relevant architecture, write the expected Terraform plan shape, and state the evidence that would falsify your first hypothesis. Then compare your answer with the key and score it using the constraints, safety, ownership, and communication rubric embedded in the exercises.

The final four platform modules extend the same method to A10 ADCs, Cisco device automation, Clos/spine-leaf fabrics, and Cisco NSO. Read the platform-neutral mechanics first, then compare Terraform with device APIs, NDFC, NETCONF/RESTCONF, YANG service models, and AS3-style ownership. Treat each controller, state store, and device partition as an explicit owner.

## G. Related tracks

- [Repository map](../README.md)
- [Cloud networking](../cloud-networking-interview/00-README.md)
- [Integrated platform labs](../platform-integration-labs/00-README.md)
- [Book automation topic](../book/topics/33-f5-api-and-automation-toolchain.md)
