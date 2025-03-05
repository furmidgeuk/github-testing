import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API URLs
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# GitHub Organization and Repo
ORG_NAME = "furmidgeuk"  # Update with your org or username
REPO_NAME = "nndcp-docs"  # Update with your repository name

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_project_id():
    """Fetch the project ID for the given repository."""
    query = {
        "query": """
        query {
          repository(owner: "%s", name: "%s") {
            projectsV2(first: 10) {
              nodes {
                id
                title
              }
            }
          }
        }
        """ % (ORG_NAME, REPO_NAME)
    }

    response = requests.post(GITHUB_GRAPHQL_URL, json=query, headers=HEADERS)

    if response.status_code == 200:
        projects = response.json()["data"]["repository"]["projectsV2"]["nodes"]
        if projects:
            project_id = projects[0]["id"]  # Assuming the first project is the target one
            print(f"✅ Found Project ID: {project_id}")
            return project_id
        else:
            print("❌ No projects found in this repository.")
    else:
        print(f"❌ Error fetching project ID: {response.status_code}, {response.text}")

    return None

# Example usage:
if __name__ == "__main__":
    project_id = get_project_id()
