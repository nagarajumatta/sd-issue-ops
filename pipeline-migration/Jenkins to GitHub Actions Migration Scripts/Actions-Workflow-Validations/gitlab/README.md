# Examples - Items Not Imported from Gitlab Pipelines to GitHub Actions Workflow

Gitlab and GitHub Actions have some differences in their syntax and functionality, so it's not always straightforward to convert a Gitlab pipeline to a GitHub Actions workflow using actions importer. However, Below are some examples of Gitlab yml files and their equivalent GitHub Actions workflows to give you an idea of the differences.

This repository also includes examples of actions that have been migrated from Gitlab, along with custom transforms that have been written for the steps that cannot be imported from gitlab.

## Table of Contents

<!-- !toc (minlevel=2 omit="Table of Contents") -->

* [Gitlab Matrix Builds](#gitlab-matrix-builds)
* [Gitlab Secrets Management](#gitlab-secrets-management)
* [Gitlab specific Environment Variables](#gitlab-specific-environment-variables)
* [Conditional Execution](#conditional-execution)
* [Artifacts](#artifacts)
* [Parallel Jobs](#parallel-jobs)
* [Slack Notification](#slack-notification)

<!-- toc! -->

While Gitlab pipelines and GitHub Actions share many similarities, there are some items that are not imported from gitlab pipelines to GitHub Actions workflows. These items include:

## **Gitlab Matrix Builds**

Gitlab Pipeline example:

```javascript
stages:
  - test

test:
  stage: test
  script:
    - echo "Running tests for $CONFIGURATION"
  variables:
    CONFIGURATION: [linux, macos, windows]
```
In this example, the CONFIGURATION variable is defined as a matrix, with values [linux, macos, windows]. The test job will be executed for each configuration in the matrix, and the $CONFIGURATION variable will have the corresponding value in each run.

Matrix builds in GitLab CI/CD provide a convenient way to define and execute jobs with multiple configurations, allowing parallel execution and testing across different environments or platforms.

GitHub Actions Workflow equivalent:

```javascript
name: Matrix Build

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        configuration: [linux, macos, windows]
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Test
        run: echo "Running tests for ${{ matrix.configuration }}"
```          
we use the strategy key within the test job to define a matrix of configurations. Each configuration value is represented as a separate job within the workflow. While it's not the exact matrix build syntax as in GitLab CI/CD, this approach achieves a similar outcome by dynamically creating jobs based on the configurations specified.

## **Gitlab Secrets Management**

Gitlab Pipeline example:

```javascript
stages:
  - build

build:
  stage: build
  script:
    - echo "Building..."
  variables:
    SECRET_KEY: $SECRET_KEY
```  

GitHub Actions Workflow equivalent:

```javascript
name: Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Build
        run: echo "Building..."
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
```          
In GitLab CI/CD, you can define variables, including secret variables, using the variables keyword. Secret values can be stored and referenced using predefined variables. In GitHub Actions, secrets are managed at the repository or organization level and can be accessed using the ${{ secrets.SECRET_NAME }} syntax within the workflow file.

## **Gitlab specific Environment Variables**

Gitlab Pipeline example:

```javascript
stages:
  - deploy

deploy:
  stage: deploy
  script:
    - echo "Deploying to $ENVIRONMENT"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - master
``` 

GitHub Actions Workflow equivalent:

```javascript
name: Deploy

on:
  push:
    branches:
      - main

env:
  ENVIRONMENT: staging
  URL: https://staging.example.com

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Deploy
        run: |
          echo "Deploying to $ENVIRONMENT"
          # Use the environment variable URL in your deployment steps
```
In this example, the GitLab CI/CD YAML file defines a deployment stage where it deploys to a staging environment. It utilizes the environment keyword to specify the environment name and URL.

The equivalent GitHub Actions workflow uses the env key to define environment variables ENVIRONMENT and URL. These variables can be accessed within the deploy job or any subsequent steps by referencing $ENVIRONMENT and $URL respectively.

You can then use these environment variables in your deployment steps or any other actions that require them within the workflow.

## **Conditional Execution**

GitLab CI/CD YAML:

```javascript
test:
  script:
    - echo "Testing..."
  rules:
    - exists("$CI_COMMIT_TAG")

deploy:
  script:
    - echo "Deploying..."
  rules:
    - exists("$CI_COMMIT_TAG")
```

GitHub Actions Workflow:

```javascript
name: Test and Deploy

on:
  push:
    branches:
      - main
  release:
    types:
      - created

jobs:
  test:
    runs-on: ubuntu-latest
    if: github.ref_type == 'tag'
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Test
        run: |
          echo "Testing..."

  deploy:
    runs-on: ubuntu-latest
    if: github.ref_type == 'tag'
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Deploy
        run: |
          echo "Deploying..."
```

In GitLab CI/CD YAML, the rules keyword allows you to define conditions for job execution. In GitHub Actions, you can use the if keyword within the job definition to specify conditional execution based on GitHub context variables.

## **Artifacts**

GitLab CI/CD YAML:

```javascript
build:
  script:
    - echo "Building..."
  artifacts:
    paths:
      - compiled-app/

test:
  script:
    - echo "Testing..."
  artifacts:
    paths:
      - test-results/

deploy:
  script:
    - echo "Deploying..."
  needs:
    - test
  environment:
    name: production
    url: https://example.com
  artifacts:
    paths:
      - logs/
```

GitHub Actions Workflow:

```javascript
name: Build, Test, and Deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Build
        run: |
          echo "Building..."
      - name: Archive build artifacts
        uses: actions/upload-artifact@v2
        with:
          name: compiled-app
          path: compiled-app/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Test
        run: |
          echo "Testing..."
      - name: Archive test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test-results/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Deploy
        run: |
          echo "Deploying..."
      - name: Archive deployment logs
        uses: actions/upload-artifact@v2
        with:
          name: logs
          path: logs/
```
In GitLab CI/CD YAML, you can specify artifacts using the artifacts keyword and define the paths to be saved. In GitHub Actions, you can achieve a similar behavior by using the outputs keyword within the job definition to define the paths of the artifacts to be saved.

## **Parallel Jobs**

GitLab CI/CD YAML:

```javascript
build:
  script:
    - echo "Building..."

test:
  script:
    - echo "Testing..."

deploy:
  script:
    - echo "Deploying..."
  needs:
    - test
```
GitHub Actions Workflow:

```javascript
name: Build, Test, and Deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Build
        run: |
          echo "Building..."

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Test
        run: |
          echo "Testing..."

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Deploy
        run: |
          echo "Deploying..."
```
In both GitLab CI/CD YAML and GitHub Actions workflows, you can define job dependencies using the needs keyword. This ensures that jobs run sequentially, with each job depending on the successful completion of its dependencies.

## **Slack Notification**

GitLab CI/CD YAML:

```javascript
deploy:
  script:
    - echo "Deploying..."
  needs:
    - test
  environment:
    name: production
    url: https://example.com
  rules:
    - exists("$CI_COMMIT_TAG")
  variables:
    SLACK_WEBHOOK: $SLACK_WEBHOOK

after_script:
  - |
    if [[ "$SLACK_WEBHOOK" ]]; then
      curl -X POST -H 'Content-type: application/json' \
        --data '{"text": "Deployment completed successfully!"}' \
        "$SLACK_WEBHOOK"
    fi
```
In GitLab CI/CD YAML, you can define the Slack webhook URL as a variable (SLACK_WEBHOOK) and then use it in the after_script section. In this example, if the SLACK_WEBHOOK variable is defined, a Slack notification is sent using the curl command.

GitHub Actions Workflow:

```javascript
name: Deploy

on:
  push:
    tags:
      - '*'

jobs:
  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Deploy
        run: |
          echo "Deploying..."
    env:
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}

  slack-notification:
    needs: [deploy]
    runs-on: ubuntu-latest
    if: ${{ success() }}
    steps:
      - name: Slack Notification
        uses: rtCamp/action-slack-notify@v4
        with:
          status: "Deployment completed successfully!"
          channel: "#general"
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```
In GitHub Actions workflows, you can use a separate job (slack-notification) to send a Slack notification. The job is triggered after the deploy job and only if the deployment is successful (success() condition). The rtCamp/action-slack-notify action is used to send the notification to the specified Slack channel using the SLACK_WEBHOOK secret.

Please note that for GitHub Actions, you would need to install the rtCamp/action-slack-notify action by adding it to your workflow's action or actioncomposite directory.
