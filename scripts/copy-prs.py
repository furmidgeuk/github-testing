import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API URL
GITHUB_API_URL = "https://api.github.com"

# Set source and destination repositories
SOURCE_OWNER = "furmidgeuk"
SOURCE_REPO = "github-testing"
DEST_OWNER = "furmidgeuk"
DEST_REPO = "nndcp-docs"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_pull_requests(owner, repo):
    """Fetch all open and closed pull requests."""
    prs = []
    page = 1
    while True:
        prs_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
        response = requests.get(prs_url, headers=HEADERS, params={"state": "all", "per_page": 100, "page": page})

        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # No more PRs to fetch
            prs.extend(batch)
            page += 1
        else:
            print(f"❌ Error fetching PRs: {response.status_code}, {response.text}")
            break
    
    return prs

def get_existing_branches(owner, repo):
    """Fetch all existing branches in the destination repository."""
    branches_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches"
    response = requests.get(branches_url, headers=HEADERS)

    if response.status_code == 200:
        return [branch["name"] for branch in response.json()]
    else:
        print(f"❌ Error fetching branches: {response.status_code}, {response.text}")
        return []

def get_pr_details(owner, repo, pr_number):
    """Fetch additional PR details like head and base branches."""
    pr_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching PR details for #{pr_number}: {response.status_code}, {response.text}")
        return None

def get_pr_labels(owner, repo, pr_number):
    """Fetch labels for a specific PR."""
    labels_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/labels"
    response = requests.get(labels_url, headers=HEADERS)
    
    if response.status_code == 200:
        return [label["name"] for label in response.json()]
    else:
        print(f"❌ Error fetching labels for PR #{pr_number}: {response.status_code}, {response.text}")
        return []

def get_pr_assignees(owner, repo, pr_number):
    """Fetch assignees for a specific PR."""
    # Using the issues endpoint to get assignees since PR is also an issue
    issue_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}"
    response = requests.get(issue_url, headers=HEADERS)
    
    if response.status_code == 200:
        return [assignee["login"] for assignee in response.json().get("assignees", [])]
    else:
        print(f"❌ Error fetching assignees for PR #{pr_number}: {response.status_code}, {response.text}")
        return []

def add_labels_to_pr(owner, repo, pr_number, labels):
    """Add labels to a pull request."""
    if not labels:
        return
        
    labels_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/labels"
    response = requests.post(labels_url, json={"labels": labels}, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"✅ Labels added to PR #{pr_number}: {', '.join(labels)}")
    else:
        print(f"❌ Error adding labels to PR #{pr_number}: {response.status_code}, {response.text}")

def add_assignees_to_pr(owner, repo, pr_number, assignees):
    """Add assignees to a pull request."""
    if not assignees:
        return
        
    assignees_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/assignees"
    response = requests.post(assignees_url, json={"assignees": assignees}, headers=HEADERS)
    
    if response.status_code == 201:
        print(f"✅ Assignees added to PR #{pr_number}: {', '.join(assignees)}")
    else:
        print(f"❌ Error adding assignees to PR #{pr_number}: {response.status_code}, {response.text}")

def create_pull_request(owner, repo, pr):
    """Create a pull request in the destination repository with labels and assignees."""
    pr_number = pr["number"]
    pr_details = get_pr_details(SOURCE_OWNER, SOURCE_REPO, pr_number)

    if not pr_details:
        print(f"⚠️ Skipping PR #{pr_number} - could not retrieve details.")
        return

    # Extract head and base branches
    source_branch = pr_details["head"]["ref"]
    base_branch = pr_details["base"]["ref"]

    # Check if base branch exists in the destination repo
    existing_branches = get_existing_branches(owner, repo)
    if base_branch not in existing_branches:
        print(f"⚠️ Base branch '{base_branch}' not found in {owner}/{repo}. Defaulting to 'main'.")
        base_branch = "main"  # Set default base branch

    # Get labels and assignees from source PR
    labels = get_pr_labels(SOURCE_OWNER, SOURCE_REPO, pr_number)
    assignees = get_pr_assignees(SOURCE_OWNER, SOURCE_REPO, pr_number)

    pr_data = {
        "title": pr["title"],
        "body": pr.get("body", "") or "",  # Ensure body is a string
        "head": source_branch,  # Source branch
        "base": base_branch,  # Target branch
    }

    prs_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    response = requests.post(prs_url, json=pr_data, headers=HEADERS)

    if response.status_code == 201:
        new_pr_number = response.json()["number"]
        print(f"✅ Pull request '{pr['title']}' copied successfully as PR #{new_pr_number}.")
        
        # Add labels and assignees to the new PR
        add_labels_to_pr(owner, repo, new_pr_number, labels)
        add_assignees_to_pr(owner, repo, new_pr_number, assignees)
    else:
        print(f"❌ Error creating PR: {response.status_code}, {response.text}")

def copy_pull_requests():
    """Copy all PRs from source to destination repository with labels and assignees."""
    prs = get_pull_requests(SOURCE_OWNER, SOURCE_REPO)
    
    if not prs:
        print("No PRs found.")
        return

    for pr in prs:
        create_pull_request(DEST_OWNER, DEST_REPO, pr)

if __name__ == "__main__":
    copy_pull_requests()
