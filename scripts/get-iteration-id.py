import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API URL
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Target GitHub Project ID
PROJECT_ID = "PVT_kwDOCaCuvc4Azlr2"

# Headers for GitHub API authentication
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_target_iterations():
    """Fetch all iterations in the target GitHub ProjectV2."""
    query = {
        "query": """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 50) {
                nodes {
                  __typename
                  ... on ProjectV2IterationField {
                    id
                    name
                    dataType
                    configuration {
                      iterations {
                        id
                        title
                        startDate
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """,
        "variables": {
            "projectId": PROJECT_ID
        }
    }

    response = requests.post(GITHUB_GRAPHQL_URL, json=query, headers=HEADERS)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Error decoding JSON response: {response.text}")
        return {}

    if response.status_code != 200:
        print(f"❌ GitHub API error: {response.status_code}, {response.text}")
        return {}

    if "errors" in response_json:
        print(f"❌ GraphQL query error: {response_json['errors']}")
        return {}

    if "data" not in response_json or "node" not in response_json["data"]:
        print(f"❌ Unexpected API response: {response_json}")
        return {}

    # Extract iteration field and details
    fields = response_json["data"]["node"]["fields"]["nodes"]
    
    iteration_field = next((field for field in fields if field["__typename"] == "ProjectV2IterationField"), None)

    if not iteration_field:
        print("❌ No Iteration Field found in the target project.")
        return {}

    # Extract iterations
    iterations = iteration_field.get("configuration", {}).get("iterations", [])

    iteration_map = {iteration["title"]: iteration["id"] for iteration in iterations}

    print(f"✅ Retrieved Iteration Mapping:\n{json.dumps(iteration_map, indent=2)}")
    return iteration_map


if __name__ == "__main__":
    get_target_iterations()
