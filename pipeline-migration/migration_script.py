
from github import Github
from base64 import b64encode
from nacl import public, encoding
import json
import requests
import os
import time

step_name = os.environ.get('STEP_NAME')

issue_ops_token = os.environ.get('ISSUE_OPS_TOKEN')
issue_ops_repo = os.environ.get('ISSUE_OPS_REPO')
issue_id = os.environ.get('ISSUE_ID')

jenkins_access_token = os.environ.get('JENKINS_ACCESS_TOKEN')
gitlab_access_token = os.environ.get('GITLAB_ACCESS_TOKEN')
circleci_access_token = os.environ.get('CIRCLECI_ACCESS_TOKEN')
travisci_access_token = os.environ.get('TRAVISCI_ACCESS_TOKEN')

# Authenticate to Issue-ops Repo
github = Github(issue_ops_token)
repo = github.get_repo(issue_ops_repo)
#issue = repo.get_issue(number=int(issue_id))

# Load configuration from config.json
with open('pipeline-migration/config/config.json', 'r') as configuration:
    config_data = json.load(configuration)

# Common headers for API requests
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {issue_ops_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_public_key():
    url = f"https://api.github.com/repos/{issue_ops_repo}/actions/secrets/public-key"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["key_id"], data["key"]

def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def update_or_create_secret(secret_name, secret_value):
    key_id, public_key = get_public_key()
    encrypted_value = encrypt(public_key, secret_value)

    url = f"https://api.github.com/repos/{issue_ops_repo}/actions/secrets/{secret_name}"
    #response = requests.get(url, headers=headers)

    payload = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    response = requests.put(url, headers=headers, json=payload)
        
def update_or_create_variable(variable_name, variable_value):
    get_url = f"https://api.github.com/repos/{issue_ops_repo}/actions/variables/{variable_name}"
    post_url = f"https://api.github.com/repos/{issue_ops_repo}/actions/variables"
    
    response = requests.get(get_url, headers=headers)
    if response.status_code == 200:
        payload = {"value": variable_value}
        response = requests.patch(get_url, headers=headers, json=payload)

    elif response.status_code == 404:
        payload = {"name": variable_name, "value": variable_value}
        response = requests.post(post_url, headers=headers, json=payload)

def process_data(data):
    for source in data['sources']:
        #if source['type'].lower() == ci_tool.lower():
        if step_name == 'migration':
            if source['type'].lower() == 'jenkins':
                issue_id = os.environ.get('JENKINS_ISSUE_ID')
                issue = repo.get_issue(number=int(issue_id))
                update_or_create_secret("JENKINS_ACCESS_TOKEN", jenkins_access_token)
                update_or_create_secret("JENKINS_USERNAME", data['jenkins_username'])
                update_or_create_variable("JENKINS_INSTANCE_URL", data['jenkins_instance_url'])
                issue.create_comment(f"/migrate --source-url {source['source_url']} --target-url {data['target_url']}")

            elif source['type'].lower() == 'gitlab':
                issue_id = os.environ.get('GITLAB_ISSUE_ID')
                issue = repo.get_issue(number=int(issue_id))
                update_or_create_secret("GITLAB_ACCESS_TOKEN", gitlab_access_token)
                update_or_create_secret("GITLAB_INSTANCE_URL", data['gitlab_instance_url'])
                source_url = source['source_url'].split(",")
                issue.create_comment(f"/migrate --project {source_url[0]} --namespace {source_url[1]} --target-url {data['target_url']}")

        elif step_name == 'audit':
            if source['type'].lower() == 'jenkins':
                issue_id = os.environ.get('JENKINS_ISSUE_ID')
                issue = repo.get_issue(number=int(issue_id))
                update_or_create_secret("JENKINS_ACCESS_TOKEN", jenkins_access_token)
                update_or_create_secret("JENKINS_USERNAME", data['jenkins_username'])
                update_or_create_variable("JENKINS_INSTANCE_URL", data['jenkins_instance_url'])
                issue.create_comment('/audit')

            elif source['type'].lower() == 'gitlab':
                issue_id = os.environ.get('GITLAB_ISSUE_ID')
                issue = repo.get_issue(number=int(issue_id))
                update_or_create_secret("GITLAB_ACCESS_TOKEN", gitlab_access_token)
                update_or_create_secret("GITLAB_INSTANCE_URL", data['gitlab_instance_url'])
                issue.create_comment(f"/audit --namespace {source['source_url']}")

        elif step_name == 'dry-run':
            if source['type'].lower() == 'jenkins':
                issue_id = os.environ.get('JENKINS_ISSUE_ID')
                issue = repo.get_issue(number=int(issue_id))
                update_or_create_secret("JENKINS_ACCESS_TOKEN", jenkins_access_token)
                update_or_create_secret("JENKINS_USERNAME", data['jenkins_username'])
                update_or_create_variable("JENKINS_INSTANCE_URL", data['jenkins_instance_url'])
                issue.create_comment(f"/dry-run --source-url {source['source_url']}")

            elif source['type'].lower() == 'gitlab':
                issue_id = os.environ.get('GITLAB_ISSUE_ID')
                issue = repo.get_issue(number=int(issue_id))
                update_or_create_secret("GITLAB_ACCESS_TOKEN", gitlab_access_token)
                update_or_create_secret("GITLAB_INSTANCE_URL", data['gitlab_instance_url'])
                source_url = source['source_url'].split(",")
                issue.create_comment(f"/dry-run --project {source_url[0]} --namespace {source_url[1]}")


# Process the relevant data based on the step name
if step_name in config_data:
    for data in config_data[step_name]:
        process_data(data)
