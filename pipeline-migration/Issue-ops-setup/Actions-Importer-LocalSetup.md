## Table of Contents
<!--

Generated with [markedpp](#markedpp). Get [nodejs](https://nodejs.org) first

1. $ npm i -g markedpp
2. $ markedpp --github -o README.md README.md

-->

<!-- !toc (minlevel=2 omit="Table of Contents") -->

<a id="readme-top"></a>

* [About GitHub Actions Importer](#about-gitHub-actions-importer)
* [Prerequisites](#Prerequisites)
  * [Install Docker Desktop on Windows](#Install-Docker-Desktop-on-Windows)
  * [Install Github CLI on Windows](#Install-Github-CLI-on-Windows)
  * [Steps For Installing Git for Windows](#Steps-For-Installing-Git-for-Windows)
    * [Login to GHCR](#Login-to-GHCR)
* [Steps For Connecting Github from CLI](#Steps-For-Connecting-Github-from-CLI)
* [Installing the GitHub Actions Importer CLI extension](#Installing-the-GitHub-Actions-Importer-CLI-extension)
  * [Authenticating at the command line](#Authenticating-at-the-command-line)
* [PAT for GitHub](#PAT-for-GitHub)
* [PAT for Jenkins](#PAT-for-Jenkins)
* [Using the GitHub Actions Importer CLI to migrate Jenkins Pipelines to GitHub Actions](#Using-the-GitHub-Actions-Importer-CLI-to-migrate-Jenkins-Pipelines-to-GitHub-Actions)
* [Trouble-shoot Steps](#Trouble-shoot-Steps)
<!-- toc! -->

## Article Referred 
<https://docs.github.com/en/actions/migrating-to-github-actions/automating-migration-with-github-actions-importer#installing-the-github-actions-importer-cli-extension>
## **About GitHub Actions Importer**
GitHub Actions Importer can be used to plan and automatically migrate CI/CD pipelines to GitHub Actions from Azure DevOps, CircleCI, GitLab, Jenkins, and Travis CI.

GitHub Actions Importer is distributed as a Docker container and uses a [GitHub CLI](https://cli.github.com/) extension to interact with the container

Any workflow that is converted by the GitHub Actions Importer should be inspected for correctness before using it as a production workload. The goal is to achieve an 80% conversion rate for every workflow; however, the actual conversion rate will depend on the makeup of each individual pipeline that is converted

## **Supported CI platforms**
GitHub Actions Importer to migrate from the following platforms:

- Azure DevOps
- CircleCI
- GitLab
- Jenkins
- Travis CI

Once a user is granted access to the preview, they will be able to access further reference documentation for each of the supported platforms.
## **Prerequisites**
GitHub Actions Importer has the following requirements:

- The user who is migrating pipelines and/or jobs must have been granted access to the public preview for the GitHub Actions Importer.
- A Jenkins account or organization with pipelines and jobs that must be convert to GitHub Actions workflows
- The user must have credentials to authenticate to the GitHub Packages Container registry. For more information, see "[Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry)."
- An environment where Linux-based containers can be run and the necessary tools can be installed. 
- Docker is [installed](https://docs.docker.com/get-docker/) and running.

## **Install Docker Desktop on Windows**

**System requirements**

- Windows 11 64-bit or Windows 10 64-bit
- Enable the WSL 2 feature on Windows (https://learn.microsoft.com/en-us/windows/wsl/install)
- A 64-bit processor with Second Level Address Translation (SLAT)
- A minimum of 4 GB of RAM
- BIOS-level hardware virtualization support

**Step 1:** Downloading Docker, Copy the below click and browse on chrome

https://docs.docker.com/desktop/install/windows-install/

![](./issue-local-setuplocal-png/Images/001.png)

**Step 2:**  Open the downloaded installer and begin the installation.

![](./issue-local-setuplocal-png/Images/002.png)

**Step 3:** Configuration

To run Linux on Windows, Docker requires a virtualization engine. Docker recommends using WSL 2.

![](./issue-local-setuplocal-png/Images/003.png)

**Step 4:** Running the installation, Click Ok, and wait a bit…

![](./issue-local-setuplocal-png/Images/004.png)









**Step 5:**  For Docker to be able to properly register with Windows, a restart is required at this point.

![](./issue-local-setuplocal-png/Images/005.png)









**Step 6:** License agreement

After the restart, Docker will start automatically and you should see the window below

![](./issue-local-setuplocal-png/Images/006.png)

Essentially, if you are a small business or use Docker for personal use, Docker contains to remain free. However, if you are in a large organization, please get in touch with your IT department to clarify the license agreement.

**Step 7:** WSL 2 installation

After you accept the license terms, the Docker Desktop window will open. However, we are not done yet. Since we have selected WSL 2 as our virtualization engine, we also need to install it. Don’t click Restart just yet!

![](./issue-local-setuplocal-png/Images/007.png)

**Step 8:** Follow the link in the dialog window and download WSL 2.

<https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi>

![](./issue-local-setuplocal-png/Images/008.png)

**Step 9 :** Open the installer.

![](./issue-local-setuplocal-png/Images/009.png)

**Step 10:**  Click on Next to begin installing the Windows Subsystem for Linux (WSL).

![](./issue-local-setuplocal-png/Images/010.png)

**Step 11:** After a few seconds, the installation should complete. So you may click on Finish.

![](./issue-local-setuplocal-png/Images/011.png)

**Step 12 :** If you still have the Docker Desktop dialog window still lurking in the background, click on Restart. Otherwise, just restart your computer as you normally do.

![](./issue-local-setuplocal-png/Images/012.png)

**Step 13:** If Docker Desktop did not start on its own, simply open it from the shortcut on your Desktop.

If you wish, you can do the initial orientation by clicking Start.

![](./issue-local-setuplocal-png/Images/013.png)

**Step 14:** After this, your Docker Desktop screen should look like this.

![](./issue-local-setuplocal-png/Images/014.png)

**Step 15:** Testing Docker

Open your favorite command line tool(Windows PowerShell or Command Prompt) and type in the following command

```javascript
docker run hello-world
```

This will download the hello-world Docker image and run it. This is just a quick test to ensure everything is working fine.


![](./issue-local-setuplocal-png/Images/015.png)

**Step 16:** Automatically start Docker

![](./issue-local-setuplocal-png/Images/016.png)

**Troubleshooting** — Issues installing WSL 2

When opening Docker Desktop for the first time, you may get an error like this one:

Failed to deploy distro docker-desktop to C:\Users\valentin\AppData\Local\Docker\wsl\distro: : Please enable the Virtual Machine Platform Windows feature and ensure virtualization is enabled in the BIOS.

For information please visit https://aka.ms/wsl2-install

Some WSL system related access rights are not set correctly. This sometimes happens after waking the computer or not being connected to your domain/active directory. Please try to reboot the computer. If not sufficient, WSL may need to be reinstalled fully. As a last resort, try to uninstall/reinstall Docker Desktop.

**Option 1:** Enable Virtual Machine Platform

Make sure that Virtual Machine Platform is enabled on your Windows installation. You can easily check this by opening the Turn Windows features on or off from your Control panel.

![](./issue-local-setuplocal-png/Images/017.png)

On your list of features, check that Virtual Machine Platform is enabled.

![](./issue-local-setuplocal-png/Images/018.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Install Github CLI on Windows**

**Step 1:** Installing GitHub CLI

GitHub CLI has releases for major operating systems. For example, if you’re using a Windows you can follow the below steps:

Click on Download for Windows and download the installer.

[GitHub CLI](https://cli.github.com/)

![](./issue-local-setuplocal-png/Images/019.png)

**Step 2:**  Open the downloaded installer and double click on gh\_\* installer.

![](./issue-local-setuplocal-png/Images/020.png)



**Step 3:**  Click on Next

![](./issue-local-setuplocal-png/Images/021.png)

**Step 4:** Click on Next

![](./issue-local-setuplocal-png/Images/022.png)

**Step 5:** Click on Install

![](./issue-local-setuplocal-png/Images/023.png)

**Step 6:** Click on Yes once it promoted and click on install and finish the setup.

![](./issue-local-setuplocal-png/Images/024.png)

**Step 7:** Verify the Installation

Open your favorite command line tool(Windows PowerShell or Command Prompt) and type in the following command

```javascript
gh --version
```

![](./issue-local-setuplocal-png/Images/025.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Steps For Installing Git for Windows**

**Step 1:** Browse to the official Git website: <https://git-scm.com/downloads>

![](./issue-local-setuplocal-png/Images/026.png)

**Step 2:**  Click on download

![](./issue-local-setuplocal-png/Images/027.png)

**Step 3:**  Browse to the download location (or use the download shortcut in your browser). Double-click the file to extract and launch the installer.

![](./issue-local-setuplocal-png/Images/028.png)









**Step 4:** Check the **only show new options** and click on install

![](./issue-local-setuplocal-png/Images/029.png)

**Step 5:** Check on launch Git bash and click on finish

![](./issue-local-setuplocal-png/Images/030.png)

**Step 6:** Terminal would like as below** 

![](./issue-local-setuplocal-png/Images/031.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Login to GHCR**
Follow the below steps for connecting to github container registry.

New versions of GitHub Actions Importer are released on a regular basis. To ensure you're always up to date, we need to connect to GHCR for downloading latest images.

**Step 1:** Open git bash 

![](./issue-local-setuplocal-png/Images/032.png)

**Step 2:**  Run the following command
```javascript
export CR_PAT=<pat token>
```
PAT(Personal access token)- we need to have pat token with workflow scope that can be created in github.com.please follow the steps [here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) if you don’t have a token.

Once created copy and paste the token as below

![](./issue-local-setuplocal-png/Images/033.png)

**Step 3:** 

Copy and paste your github handler name after -u ,you can login into github and get the handler name as below

![](./issue-local-setuplocal-png/Images/034.png)

```javascript
echo $CR_PAT | docker login ghcr.io -u <username> --password-stdin
```

![](./issue-local-setuplocal-png/Images/035.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Steps For Connecting Github from CLI**

**Step 1:** Open powershell from windows search

![](./issue-local-setuplocal-png/Images/036.png)

**Step 2:** Follow the below steps and provide the values exactly as below, we need to authenticate via PAT(Personal Access Token) which was created in above steps


Once powershell is opened execute the following command as mentioned in screenshot
```javascript
gh auth login
```

### ![](./issue-local-setuplocal-png/Images/037.png)
### Select Github.com and click enter
### ![](./issue-local-setuplocal-png/Images/038.png)
### Type Y and click enter
### ![](./issue-local-setuplocal-png/Images/039.png)
### Select HTTPS and click enter
### ![](./issue-local-setuplocal-png/Images/040.png)
### Type Y and click enter
### ![](./issue-local-setuplocal-png/Images/041.png)
###
###
###
###
### Here select Paste an authentication token and click enter
### ![](./issue-local-setuplocal-png/Images/042.png)
### Paste the authentication token and enter
###

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Installing the GitHub Actions Importer CLI extension**
Open powershell from windows search

![](./issue-local-setuplocal-png/Images/043.png)

1. Run the below command and Install the GitHub Actions Importer CLI extension:

```javascript 
 gh extension install github/gh-actions-importer
 ```

![](./issue-local-setuplocal-png/Images/044.png)

2. Verify that the extension is installed:

```javascript 
 gh extension list 
 ```

![](./issue-local-setuplocal-png/Images/045.png)
## Updating the GitHub Actions Importer CLI

```javascript 
 gh actions-importer update 
 ```

![](./issue-local-setuplocal-png/Images/046.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Authenticating at the command line**
You must configure credentials that allow GitHub Actions Importer to communicate with GitHub and your current CI server(Jenkins). You can configure these credentials using environment variables or a .env.local file. The environment variables can be configured in an interactive prompt, by running the following command:

```javascript 
 gh actions-importer configure 
 ```

Once you are granted access to the preview, you will be able to access further reference documentation about using environment variables.

![](./issue-local-setuplocal-png/Images/047.png)

## **PAT for Github**
After selecting Jenkins provide the PAT for github by following [here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) and select scope as repo and workflow as below 

![](./issue-local-setuplocal-png/Images/048.png)

## **PAT for Jenkins**

For creating Jenkins personal access token, please follow the below steps

**Step 1:** Login into Jenkins

![](./issue-local-setuplocal-png/Images/049.png)





**Step 2:** Click on configure

![](./issue-local-setuplocal-png/Images/050.png)

**Step 3:** Click on Add new Token

![](./issue-local-setuplocal-png/Images/051.png)

**Step 4:** Provide the name and click on Generate

![](./issue-local-setuplocal-png/Images/052.png)

**Step 5:** Copy the token and save it locally because it cannot be recovered in future.

![](./issue-local-setuplocal-png/Images/053.png)

**Provide all the values like PAT for github,base url of github,PAT for Jenkins,Jenkins Username and Jenkins Instance Url**

![](./issue-local-setuplocal-png/Images/054.png)

**Note:** Configure will create a .env.local file locally

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 
## **Using the GitHub Actions Importer CLI to migrate Jenkins Pipelines to GitHub Actions**
**Step 1:** Use the subcommands of gh actions-importer to begin your migration to GitHub Actions, including audit, forecast, dry-run, and migrate

 ```javascript
gh actions-importer audit jenkins --output-dir .
```

![](./issue-local-setuplocal-png/Images/055.png)

In File Explorer it would look like as below

![](./issue-local-setuplocal-png/Images/056.png)

**Step 2:** This command converts a Jenkins Job to a GitHub Action Workfow and output its yaml file.

```javascript
gh actions-importer dry-run jenkins -h
```

![](./issue-local-setuplocal-png/Images/057.png)


**Step 3:** Run the below command by passing the job name as below,in my case the Jenkins job name is “IM-Jenkins-ActionsImported”

```javascript
gh actions-importer dry-run jenkins -s http://20.51.238.66:8080/job/IM-Jenkins-ActionsImported -o .
```

![](./issue-local-setuplocal-png/Images/058.png)

**Step 4:** Run the below command by passing source and destination url
  
```javascript
gh actions-importer migrate jenkins -s http://20.51.238.66:8080/job/IM-Jenkins-ActionsImported/ --target-url https://github.com/im-sandbox-suryaraghava80/test.git -o .
```

Source would be Jenkins job url : [**http://20.51.238.66:8080/job/IM-Jenkins-ActionsImported/**](http://20.51.238.66:8080/job/IM-Jenkins-ActionsImported/)

![](./issue-local-setuplocal-png/Images/059.png)

Destination would be github repository : [**https://github.com/customer-sandbox/Jenkins-githubactions.git**](https://github.com/customer-sandbox/Jenkins-githubactions.git)

If you don’t have destination repository please follow the steps [here](https://docs.github.com/en/get-started/quickstart/create-a-repo)


![](./issue-local-setuplocal-png/Images/060.png)

**Step 5:** Login into github and approve the pull request and merge to main branch

![](./issue-local-setuplocal-png/Images/061.png)









Click on merge pull request and confirm merge

![](./issue-local-setuplocal-png/Images/062.png)



Now go to workflow folder and we would see the pipeline was migrated successfully.

![](./issue-local-setuplocal-png/Images/063.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 
## **Trouble-shoot Steps:**

- Base url of the Jenkins Instance: http://20.51.238.66:8080/
- Base url of the GitHub instance: <https://github.com>
- Jenkins PAT: name: IM-Actions-Importer , value: "Api-Token"
- Make sure the Repo at GitHub has branches
