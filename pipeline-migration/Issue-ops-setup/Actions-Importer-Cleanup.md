<h1>Post-migration cleanup</h1>

<a id="readme-top"></a>

After migrating the pipelines into the target repository, there are a few items that will need cleanup. These items do not impact the repository by remaining, it is only that these items no longer have any use, and so should be removed.

The items that need to be cleaned are:
- Issues created in the Action Importer Issue Ops repo to support the migration
- Issue IDs stored in the target reposistory
- Pipeline tokens that were used to integrate with the pipeline source servers

To clean up the items, use the Cleanup-Migration workflow. The first step is to cean up the issues in the Action Importer IssueOps repo. If the Issue IDs are removed from the target repo first, the worflow will not have Issue ID necessary to close the Action Importer issue.

<h2>Clean up the issues in the Action Importer IssueOps repo</h2>
This should be the first step in the cleanup. The issues will be in an 'Opsn' state after the migration, and will clutter the Action Importer IssueOps' view of Open issues. To alleviate this, run Cleanup on the issues that were opened. If there is more than one pipeline source, run the cleaup for each type.
There is no harm running the cleanup using a Issue ID which has already been closed. Repeat this process for each CI/CD tool which had the pipeline imported.

To close an issue in the Action Importer IssueOps repo:
- Run the Cleanup-Migration Action
- Select the CI/CD tool (Jenkins, Gitlab, CircleCI, TravisCI)
- Select the option 'IssueOps issue'
- Click 'Run Workflow'

  The workflow will execute in less than a minute. Once the workflow is complete, the Issue ID in the Action Importer IssueOps repo will be set to a 'Closed' status. The issue is not deleted, but closing the issue will prevent it from showing on the default Issue webpage.

<h2>Cleanup the Issue_ID variable in the target repo</h2>
After the corresponding issue has been closed in the Action Importer IssueOps repo, there is no need to retain this in the target repository. 

To remove the variable used to store the Issue ID:
- Run the Cleanup-Migration Action
- Select the CI/CD tool (Jenkins, Gitlab, CircleCI, TravisCI)
- Select the option 'This repo'
- Click 'Run Workflow'

  The workflow will execute in less than a minute. Once the workflow is complete, the variable for the Issue ID in the target repo will be removed. Repeat this process for each CI/CD tool which had the pipeline imported.
