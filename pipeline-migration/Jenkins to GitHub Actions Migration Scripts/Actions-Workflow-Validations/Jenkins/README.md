# Examples - Items Not Imported from Jenkins Pipelines to GitHub Actions Workflow

Jenkins and GitHub Actions have some differences in their syntax and functionality, so it's not always straightforward to convert a Jenkins pipeline to a GitHub Actions workflow using actions importer. However, Below are some examples of Jenkinsfiles and their equivalent GitHub Actions workflows to give you an idea of the differences.

This repository also includes examples of actions that have been migrated from Jenkins jobs, along with custom transforms that have been written for the steps that cannot be imported from Jenkins.

## Note

"Currently, the actions importer does not support Jenkins scripted pipelines. If you encounter any errors like the one shown below while running the actions importer, it may be necessary to manually write the actions workflow. This repository also includes a manually written scripted pipeline."

```javascript
# Unable to parse Jenkins pipeline. Scripted pipelines are not currently supported.
# Pipeline type: flow-definition
#Error: Process completed with exit code 1.
```

## Table of Contents

<!-- !toc (minlevel=2 omit="Table of Contents") -->

* [Jenkins specific plugins](#jenkins-specific-plugins)
* [Jenkins specific syntax](#jenkins-specific-syntax)
* [Jenkins specific environment variables](#jenkins-specific-environment-variables)
* [Jenkins specific agents](#jenkins-specific-agents)
* [Jenkins specific credentials](#jenkins-specific-credentials)
* [Jenkins specific notifications](#jenkins-specific-notifications)
* [Jenkins specific tools](#jenkins-specific-tools)
<!-- toc! -->

While Jenkins pipelines and GitHub Actions share many similarities, there are some items that are not imported from Jenkins pipelines to GitHub Actions workflows. These items include:

## **Jenkins specific plugins**

 Jenkins has a vast array of plugins that are not available in GitHub Actions. These plugins provide additional functionality for Jenkins pipelines, such as automated testing and deployment. Since these plugins are specific to Jenkins, they cannot be imported into GitHub Actions workflows.

For example, the Pipeline Maven plugin used in the Jenkinsfile cannot be used in GitHub Actions Workflow.

Jenkins Pipeline example:

```javascript
 pipeline {
  agent any
  stages {
    stage('Build') {
      agent {
        docker {
          image 'maven:3.5.0-jdk-8'
        }
      }
      steps {
        withMaven(options: [findbugsPublisher(), junitPublisher(ignoreAttachments: false)]) {
          sh 'mvn clean findbugs:findbugs package'
        }
      }
    }
  }
}
```

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Build and Test
        run: |
          sudo apt-get update && sudo apt-get install -y maven
          mvn clean findbugs:findbugs package
      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v1.1
        with:
          files: '**/surefire-reports/TEST-*.xml'
```          

In this example, we use the actions/checkout action to checkout the code, install Maven, and run the build and test steps. We also use the EnricoMi/publish-unit-test-result-action action to publish the test results.          

In this example, the withMaven step uses the Pipeline Maven plugin to publish test results and annotate the console. This plugin is not available in GitHub Actions Workflow.

## **Jenkins specific syntax**

Jenkins Pipeline has its own syntax, which is different from the YAML syntax used in GitHub Actions Workflow. Some of the syntax used in the Jenkinsfile, such as the readMavenPom() function or the success() function in the post-build step, cannot be used in GitHub Actions Workflow.

Jenkins Pipeline example:

```javascript
pipeline {
  agent any
  post {
    success {
      // notify users when the Pipeline succeeds
      mail to: 'team@example.com',
          subject: "Successful Pipeline: ${currentBuild.fullDisplayName}",
          body: "The Pipeline at ${env.BUILD_URL} has succeeded."
    }
  }
}
```  

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: |
          # Build and test steps
      - name: Send Email Notification
        if: ${{ job.status == 'success' }}
        run: |
          echo "The Workflow has succeeded." | mail -s "Successful Workflow" team@example.com
```          
In this example, we use the mail command to send an email notification when the workflow succeeds. We use an if statement to only run the notification step when the workflow succeeds.

In this example, the currentBuild and env.BUILD_URL variables are specific to Jenkins Pipeline and cannot be used in GitHub Actions Workflow.



## **Jenkins specific environment variables**

Jenkins pipelines use their own environment variables, which are specific to Jenkins. These variables are not available in GitHub Actions workflows, and they cannot be imported.

Jenkins provides a wide variety of environment variables that can be used in a Pipeline. Here are some examples of Jenkins-specific environment variables and their potential GitHub Actions equivalents:

1. `currentBuild`: This variable provides information about the current build, such as the build number or the URL of the build. In GitHub Actions, you can use the `github` context to access similar information. For example, `github.run_id` provides the ID of the current workflow run, and `github.run_number` provides the run number.

Jenkins Pipeline example:

```javascript
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'echo "Build Number: ${currentBuild.number}"'
        sh 'echo "Build URL: ${env.BUILD_URL}"'
      }
    }
  }
}
``` 

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Print Build Info
        run: |
          echo "Run Number: ${{ github.run_number }}"
          echo "Workflow URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

2. `env.GIT_COMMIT`: This variable provides the SHA-1 hash of the commit being built. In GitHub Actions, you can use the `github` context to access similar information. For example, `github.sha` provides the SHA-1 hash of the commit being built, and `github.event.head_commit.id` provides the SHA-1 hash of the latest commit in the push event.

Jenkins Pipeline example:

```javascript
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'echo "Commit Hash: ${env.GIT_COMMIT}"'
      }
    }
  }
}
```

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Print Commit Hash
        run: echo "Commit Hash: ${{ github.sha }}"
```

3. `env.GIT_BRANCH`: This variable provides the name of the branch being built. In GitHub Actions, you can use the `github` context to access similar information. For example, `github.ref` provides the full reference name of the branch being built, and `${{ github.ref_path }}` provides the name of the branch being built.

Jenkins Pipeline example:

```javascript
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'echo "Branch Name: ${env.GIT_BRANCH}"'
      }
    }
  }
}
```

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Print Branch Name
        run: echo "Branch Name: ${{ github.ref_path }}"
```
4. 'environment': In Jenkins, you can define environment variables in a pipeline using the environment directive. For example:

Jenkins Pipeline example:

```javascript
pipeline {
    agent any
    environment {
        NAME = "Jenkins"
        VERSION = "2.289.1"
    }
    stages {
        stage('Build') {
            steps {
                sh 'echo "Building ${NAME} version ${VERSION}"'
            }
        }
    }
}
```

In this example, we have defined two environment variables NAME and VERSION using the environment directive. These variables can be accessed and used within the pipeline using the ${NAME} and ${VERSION} syntax.

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: push
env:
  NAME: "GitHub Actions"
  VERSION: "2.0"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Build
      run: |
        echo "Building $NAME version $VERSION"
```        

In this example, we have defined two environment variables NAME and VERSION using the env keyword. These variables can be accessed and used within the workflow using the $NAME and $VERSION syntax.

## **Jenkins specific agents**

Jenkins Pipeline allows you to specify agents to run the different stages of the Pipeline. These agents can be configured with specific labels or requirements, such as Docker or Kubernetes. GitHub Actions does not have the concept of agents, but instead provides runners that can run the workflow on different platforms, such as Linux, Windows, or macOS.

```javascript
pipeline {
  agent {
    node {
      label 'docker'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build . -t my-image'
      }
    }
  }
}
```

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: docker:latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Build Docker Image
        run: docker build . -t my-image
```

In this example, we use the docker:latest container to run the workflow on a Docker environment. We also use the actions/checkout action to checkout the code and run the build step.

In this example, the node block is used to specify an agent with the docker label. This is not directly transferable to GitHub Actions Workflow.

## **Jenkins specific credentials**

Jenkins allows you to store and manage credentials that can be used in your Pipeline. These credentials can be accessed using the withCredentials block in the Jenkinsfile. GitHub Actions provides a similar feature called secrets, which allows you to store and manage secrets that can be used in your workflow.

```javascript
pipeline {
  agent any
  environment {
    NEXUS_CREDENTIALS = credentials('nexus')
  }
  stages {
    stage('Build') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${NEXUS_CREDENTIALS}", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
          sh 'mvn deploy -Dmaven.test.skip=true -DaltDeploymentRepository=nexus::default::${NEXUS_URL} -DaltDeploymentRepositoryId=nexus -DaltDeploymentRepositorySnapshots=${NEXUS_SNAPSHOTS} -DaltDeploymentRepositoryReleases=${NEXUS_RELEASES}'
        }
      }
    }
  }
}
```
GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Deploy to Nexus
        env:
          NEXUS_USER: ${{ secrets.NEXUS_USERNAME }}
          NEXUS_PASS: ${{ secrets.NEXUS_PASSWORD }}
        run: |
          mvn deploy -Dmaven.test.skip=true -DaltDeploymentRepository=nexus::default::${NEXUS_URL} -DaltDeploymentRepositoryId=nexus -DaltDeploymentRepositorySnapshots=${NEXUS_SNAPSHOTS} -DaltDeploymentRepositoryReleases=${NEXUS_RELEASES}
```

In this example, we use the secrets feature to store and manage the Nexus username and password, and use the env syntax to access these secrets in the workflow.

## **Jenkins specific notifications**

Jenkins allows you to configure email or chat notifications to be sent when a Pipeline completes. GitHub Actions provides similar notification features, but the syntax and tools used may differ.

Jenkins Pipeline example:

```javascript
pipeline {
  agent any
  post {
    success {
      // notify users when the Pipeline succeeds
      mail to: 'team@example.com',
          subject: "Successful Pipeline: ${currentBuild.fullDisplayName}",
          body: "The Pipeline at ${env.BUILD_URL} has succeeded."
    }
    failure {
      // notify users when the Pipeline fails
      mail to: 'team@example.com',
          subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
          body: "The Pipeline at ${env.BUILD_URL} has failed."
    }
  }
}
```

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Build and Test
        run: |
          # Build and test steps
      - name: Send Email Notification on Success
        if: ${{ job.status == 'success' }}
        run: |
          echo "The Workflow has succeeded." | mail -s "Successful Workflow" team@example.com
      - name: Send Email Notification on Failure
        if: ${{ job.status == 'failure' }}
        run: |
          echo "The Workflow has failed." | mail -s "Failed Workflow" team@example.com
```


we use the mail command to send email notifications when the workflow succeeds or fails. We use an if statement to run the notification steps only when the workflow status matches the condition.

## **Jenkins specific tools**

Jenkins Pipeline supports a wide range of tools and technologies that can be used in your Pipeline. While some of these tools may not have a direct equivalent in GitHub Actions, you can usually achieve similar results using other tools or workflows.

Jenkins Pipeline example:

```javascript
pipeline {
  agent any
  stages {
    stage('Deploy to Kubernetes') {
      environment {
        KUBECONFIG = credentials('kubeconfig')
      }
      steps {
        sh 'kubectl --kubeconfig=$KUBECONFIG apply -f deployment.yaml'
      }
    }
  }
}
```

GitHub Actions Workflow equivalent:

```javascript
name: My Workflow
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Configure Kubernetes CLI
        uses: steebchen/kubectl-setup@v1
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}
      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f deployment.yaml
```

In this example, we use the steebchen/kubectl-setup action to configure the Kubernetes CLI with the KUBECONFIG secret. We then use the kubectl command to deploy the application to Kubernetes.
