# Copy issues and pull requests from one organisation to another
## Python setup
Create a virtual environment
```
python3 -m venv <env name>
```
e.g.
```
python3 -m venv venv
```

Activate the environment on linux/macos
```
source venv/bin/activate
```
Activate the environment on Windows
```
.\venv\Scripts\activate.bat
```

## Install dependencies
```
pip install requests python-dotenv
```
## Created a .env file with your GitHub token:
```
GITHUB_TOKEN=your_github_token
```

## Python Script
```
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API URL
GITHUB_API_URL = "https://api.github.com"

# Set source and destination repositories
SOURCE_OWNER = "source-org"
SOURCE_REPO = "source-repo"
DEST_OWNER = "destination-org"
DEST_REPO = "destination-repo"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_issues_and_prs(owner, repo):
    """Fetch all open and closed issues, including PRs, from the source repository."""
    issues = []
    page = 1
    while True:
        issues_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
        response = requests.get(issues_url, headers=HEADERS, params={"state": "all", "per_page": 100, "page": page})

        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # No more issues to fetch
            issues.extend(batch)
            page += 1
        else:
            print(f"Error fetching issues: {response.status_code}, {response.text}")
            break
    
    return issues

def create_issue(owner, repo, issue):
    """Create an issue in the destination repository."""
    issue_data = {
        "title": issue["title"],
        "body": issue.get("body", ""),
        "labels": [label["name"] for label in issue.get("labels", [])],
        "state": issue["state"],  # Preserve open/closed state
    }

    if "pull_request" in issue:
        issue_data["body"] += f"\n\n**Original PR:** {issue['html_url']}"  # Add reference to original PR

    issues_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    response = requests.post(issues_url, json=issue_data, headers=HEADERS)

    if response.status_code == 201:
        print(f"Issue/PR '{issue['title']}' copied successfully.")
    else:
        print(f"Error creating issue: {response.status_code}, {response.text}")

def copy_issues_and_prs():
    """Copy all issues and PRs from source to destination repository."""
    issues = get_issues_and_prs(SOURCE_OWNER, SOURCE_REPO)
    
    if not issues:
        print("No issues or PRs found.")
        return

    for issue in issues:
        create_issue(DEST_OWNER, DEST_REPO, issue)

if __name__ == "__main__":
    copy_issues_and_prs()

```
