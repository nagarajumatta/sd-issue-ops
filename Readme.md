# GitHub Actions Importer IssueOps

The GitHub Actions Importer IssueOps repository demonstrates the functionality necessary to run GitHub Actions Importer commands through Actions and Issues, allowing you to migrate your CI/CD workflows without needing to install software on your local machine. This approach is especially useful for organizations that want to enable self-service migrations to GitHub Actions.

[GitHub Actions Importer](https://docs.github.com/en/actions/migrating-to-github-actions/automating-migration-with-github-actions-importer) helps plan, forecast, and automate the migration of Azure DevOps, CircleCI, GitLab, Jenkins, and Travis CI pipelines to GitHub Actions. GitHub Actions Importer is distributed as a CLI and offers various commands you can use to migrate pipelines:

- `audit`: An audit will fetch all the pipelines defined in an existing CI server, convert each pipeline to its equivalent in GitHub Actions, and write a report that summarizes how complete of a migration the GitHub Actions Importer can provide.
- `dry-run`: A dry run will fetch a single pipeline definition, convert it to its equivalent in GitHub Actions, and write a file (or files) to disk containing the converted workflow.
- `migrate`: A migration will fetch a single pipeline definition, convert it to its equivalent in GitHub Actions, and open a pull request to a repository with the converted workflow.

## Getting started

Complete the following steps:

1. Create `issueops` repo with `actions/importer-issue-ops` template.
2. Create the following labels in this new repository, if they are not already present: `jenkins`, `azure-devops`, `circle-ci`, `gitlab`, `travis-ci`, and `actions-importer-running`.
3. Add the repository secrets described below that are relevant to the CI/CD providers being migrated.
4. Required authorization secrets for `Jenkins` were updated.

  `JENKINSFILE_ACCESS_TOKEN`: The personal access token used to retrieve the contents of a Jenkinsfile stored in the build repository (requires repo scope).
  `JENKINS_ACCESS_TOKEN`: The access token used to view Jenkins resources.
  `JENKINS_USERNAME`: The username of the user's access token.
  `JENKINS_INSTANCE_URL`: The base URL of your Jenkins instance.

### Repository settings

The repository that is created from this template must have one of the following settings enabled:

- Any action or reusable workflow can be used, regardless of who authored it or where it is defined.
- Any action or reusable workflow that matches the specified criteria, plus those defined in a repository within the enterprise, can be used.
   - Allow actions created by GitHub 
   - Allow actions by marketplace verified creators or icnlude `ruby/setup-ruby@v1` in the allowed list of actions and reusable workflows.

See the [documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#managing-github-actions-permissions-for-your-repository) for more information related to these settings.

### All CI/CD providers

The following secrets are required:

- `GH_ACCESS_TOKEN`: GitHub personal access token to create pull requests (requires `repo` and `workflow` scopes).

Optionally, the following environment variables can be set:

- `GITHUB_INSTANCE_URL`: The base URL of your GitHub instance (only required if it is **not** <https://github.com>).

### Azure DevOps

The following secrets are required:

- `AZURE_DEVOPS_ACCESS_TOKEN`: The personal access token to access the Azure DevOps instance. This token requires the following scopes:
  - Build (Read)
  - Agent Pools (Read)
  - Code (Read)
  - Release (Read)
  - Service Connections (Read)
  - Task Groups (Read)
  - Variable Groups (Read)

Optionally, the following environment variables can be set:

- `AZURE_DEVOPS_INSTANCE_URL`: The base URL of your Azure DevOps instance (only required if it is **not** <https://dev.azure.com>).

### CircleCI 

The following secrets are required:

- `CIRCLE_CI_ACCESS_TOKEN`: The personal access token to access the CircleCI instance.
- `CIRCLE_CI_SOURCE_GITHUB_ACCESS_TOKEN`: The personal access token to access pipeline files stored in GitHub.

Optionally, the following environment variables can be set:

- `CIRCLE_CI_INSTANCE_URL`: The base URL of your CircleCI instance (only required if it is **not** <https://circleci.com>).

### GitLab

The following secrets are required:

- `GITLAB_ACCESS_TOKEN`: The personal access token to access the GitLab instance (requires `read_api` scope).

Optionally, the following environment variables can be set:

- `GITLAB_INSTANCE_URL`: The base URL of your GitLab instance (only required if it is **not** <https://gitlab.com>).

### Jenkins

The following secrets are required:

- `JENKINSFILE_ACCESS_TOKEN`: The personal access token used to retrieve the contents of a `Jenkinsfile` stored in the build repository (requires `repo` scope).
- `JENKINS_ACCESS_TOKEN`: The access token used to view Jenkins resources.
- `JENKINS_USERNAME`: The username of the user's access token.

The following environment variables are required:

- `JENKINS_INSTANCE_URL`: The base URL of your Jenkins instance.

### Travis CI

The following secrets are required:

- `TRAVIS_CI_ACCESS_TOKEN`: The personal access token to access the Travis CI instance.
- `TRAVIS_CI_SOURCE_GITHUB_ACCESS_TOKEN`: The personal access token to access pipeline files stored in GitHub.

Optionally, the following environment variables can be set:

- `TRAVIS_CI_INSTANCE_URL`: The base URL of your Travis CI instance (only required if it is **not** <https://travis-ci.com>).

## Pipeline migration

Once configured, pipelines can be migrated to GitHub Actions by opening an issue with the relevant issue template and following the instructions.
* `/audit `

  `/migrate --source-url :jenkins-job-url --target-url :github-repository-url `

  `/dry-run --source-url :jenkins-job-url `

*Note*: If any options are missing, the command will not be successful.


Below is the process to convert the pipelines to GitHub workflows by adding the below comments and required flags to the issue in the Issue-Ops repo.

### `migrate`
* Converts a single job to its equivalent GitHub Actions.
* Post-processing. 
* Creates a PR with the changes in the target repo.

### `audit`
* Converts all pipelines in an instance or a specific jenkins folder to their equivalent GitHub Actions.
* Post-processing
* Converts jobs to GitHub actions workflows and creates artifacts that can be downloaded from the workflow run.
* Generates an audit summary and adds it in a comment.

### `dry-run`
* Converts a single pipeline definition to its equivalent GitHub Actions.
* Post-processing.
* Creates a comment with the converted workflow file content for each runner.

#### Post-processing: 
* Happens in post_processing.sh.
* Works in `audit`, `migrate`, `dry-run`
* Replaces secrets, variables, search_patterns etc in the converted workflow files.
* Clones and moves the workflows to destination repos. Commits and pushes the changes to target repo and creates PR.
* Example command : `/audit --custom-transformers ./transformers.rb`

### Custom transformers

Custom transformers can be used to customize the behavior of Actions Importer to meet your specific use-case. Custom transformers can be used to:

- Convert items that are not automatically converted.
- Convert items that were automatically converted using different actions.
- Convert environment variable values differently.
- Convert references to runners to use a different runner name in Actions.

Custom transformers must be defined in a file with the `.rb` file extension within a directory named `transformers` in your IssueOps repository. Alternatively, you can provide specific custom transformers to be used by appending the `--custom-transformers` option in the issue comment used to trigger Actions Importer. For example:

```sh
/migrate ... --custom-transformers my-transformers.rb
```

You can learn more about authoring custom transformers by completing the self-guided learning exercises below:

- Custom transformers for Azure DevOps pipelines [exercise](https://github.com/actions/importer-labs/blob/main/azure_devops/5-custom-transformers.md)
- Custom transformers for CircleCI pipelines [exercise](https://github.com/actions/importer-labs/blob/main/circle_ci/5-custom-transformers.md)
- Custom transformers for GitLab pipelines [exercise](https://github.com/actions/importer-labs/blob/main/gitlab/5-custom-transformers.md)
- Custom transformers for Jenkins pipelines [exercise](https://github.com/actions/importer-labs/blob/main/jenkins/5-custom-transformers.md)
- Custom transformers for Travis CI pipelines [exercise](https://github.com/actions/importer-labs/blob/main/travis/5-custom-transformers.md)

## Configuring IssueOps with GitHub Enterprise Server and self-hosted runners

This template can be configured to be used with GitHub Enterprise Server deployments and self-hosted runners by:

1. Updating the [ruby/setup-ruby](https://github.com/ruby/setup-ruby) actions in [issue_ops.yml](./.github/workflows/issue_ops.yml) and [ci.yml](./.github/workflows/ci.yml) to ensure the action runs on the correct OS type.
2. Updating the `runs-on:` statements in [ruby/setup-ruby](https://github.com/ruby/setup-ruby) actions in [issue_ops.yml](./.github/workflows/issue_ops.yml) to dictate the appropriate label(s) for your self-hosted runner.
3. For GitHub Enterprise Server deployments, this repository should be published and [converted to a template repository](https://docs.github.com/en/enterprise-server/repositories/creating-and-managing-repositories/creating-a-template-repository) in your GHES deployment.

## Privacy statement

GitHub Actions Importer will collect anonymous telemetry when running to help us improve the tool. This can be disabled by adding the `--no-telemetry` flag to any command provided to the GitHub Actions Importer CLI.

Additionally, by using this repository you agree to GitHub's [Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement#data-retention-and-deletion-of-data) and the [additional terms for Actions](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#actions).
