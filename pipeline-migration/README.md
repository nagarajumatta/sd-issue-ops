## **GitHub IssueOps Actions Importer**

This repository demonstrates the functionality necessary to run GitHub Actions Importer through IssueOps, allowing a user to migrate CI/CD workflows without installing additional software. This approach is especially useful for organziations that want to enable self-service migration to GitHub actions and is designed to work with popular CI/CD solutions such as Jenkins and GitLab. 

Any workflow that is converted by the GitHub Actions Importer should be inspected for correctness before using it as a production workload. The goal is to achieve an 80% conversion rate for every workflow; however, the actual conversion rate will depend on the makeup of each pipeline that is converted.

This repository also contains examples of validations for Jenkins and Gitlab.

## Getting started

1. [IssueOps Action Importer Setup](./Issue-ops-setup/Actions-Importer-Issue_Ops%20Repository%20Setup.md)

   Start here to set up the Actions workflow for a mass migrations from Jenkins or GitLab to the Actions workflow. Initial environment setup is documented here for adminstrators of the Organization where the migration will occur. Migration users can begin at step 2 below, Issue Ops Migration Tool, to begin their migration.

   **Note:** It is highly recommended to follow this approach when migrating multiple pipelines.

2. [IssueOps Migration Tool](./Issue-ops-setup/IssueOps-Migration-Tool.md) 

   Migration users can start here to set up and execute a pipeline migration via IssueOps.
   
    **Note:** The IssueOps Action Importer MUST be set up within the Organization that contains the migration repository before this work can begin.

3. [View Workflows](../.github/workflows)

   Shortcut to the specific workflows used within this repository, where each workflow will perform a specific functionality.

4. [Actions Workflow Known Migration Issues](./Jenkins%20to%20GitHub%20Actions%20Migration%20Scripts/Actions-Workflow-Validations/)

   Once the migration is completed, there may be certain steps that are not migrated as expected. The above link provides examples of custom actions for Jenkins and GitLab, which give the user an idea of how to write custom actions after the migration.
   
5. [Actions-importer Alternative Approach - Setup Locally](./Issue-ops-setup/Actions-Importer-LocalSetup.md) 

   Guidance on how to set up the Actions Importer locally. The steps outlined in the link will help a user understand the functionality of the importer by running commands such as audit, dry-run, and migrate.

   **Note:** This documentation explains how to set up the actions importer locally, but please note that this approach is intended for experimentation or single pipeline migrations only. It is not recommended for mass pipeline migrations. 

6. [Troubleshooting Guide](./Issue-ops-setup/Troubleshooting-Guide.md)

   A compilation of recommendations on how to resolve common issues when using this tool and other relavant assets to support the end user as they move through migration.
   
7. [Maintaining This Tool](./Issue-ops-setup/Tool-Maintenance.md)

   Administrator resources and guidance on how to maintain this tool through future releases and modifications to the foundational tools that support the IssueOps Migration toolset.
