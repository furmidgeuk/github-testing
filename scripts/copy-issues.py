import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API URLs
GITHUB_API_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Set source and destination repositories
SOURCE_OWNER = "furmidgeuk"
SOURCE_REPO = "nn-databricks"
DEST_OWNER = "furmidgeuk"
DEST_REPO = "nndcp-docs"

# GitHub Project ID
PROJECT_ID = "PVT_kwDOCaCuvc4Azlr2"
ITERATION_ID_MAP = {
    "ea0f6749": "7f367449",  # Source ID → Target ID
    "792d2d4e": "2e7ffa25",
    "f0652ad5": "df921a35"
}
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_issues(owner, repo):
    """Fetch all open and closed issues (excluding PRs)."""
    issues = []
    page = 1
    while True:
        issues_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
        response = requests.get(issues_url, headers=HEADERS, params={"state": "all", "per_page": 100, "page": page})

        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # No more issues to fetch
            issues.extend([issue for issue in batch if "pull_request" not in issue])  # Exclude PRs
            page += 1
        else:
            print(f"❌ Error fetching issues: {response.status_code}, {response.text}")
            break
    
    return issues

def get_custom_fields():
    """Fetch all custom fields for a GitHub ProjectV2."""
    query = {
        "query": """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 50) {
                nodes {
                  __typename
                  ... on ProjectV2Field {
                    id
                    name
                    dataType
                  }
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    dataType
                    options {
                      id
                      name
                    }
                  }
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

    fields = response_json["data"]["node"]["fields"]["nodes"]
    
    field_dict = {}
    for field in fields:
        # Skip empty or malformed fields
        if not field or "id" not in field or "name" not in field or "dataType" not in field:
            print(f"⚠️ Skipping invalid field: {field}")
            continue
        
        field_data = {
            "id": field["id"],
            "type": field["__typename"],
            "dataType": field["dataType"],
        }
        
        # Handle single select fields
        if field["__typename"] == "ProjectV2SingleSelectField":
            field_data["options"] = {opt["name"]: opt["id"] for opt in field.get("options", [])}
        
        # Handle iteration fields
        elif field["__typename"] == "ProjectV2IterationField":
            iterations = {}
            
            for iteration in field.get("configuration", {}).get("iterations", []):
                iterations[iteration["title"]] = {
                    "id": iteration["id"],
                    "startDate": iteration["startDate"]
                }
            
            field_data["iterations"] = iterations
        
        field_dict[field["name"]] = field_data

    print(f"✅ Retrieved Custom Fields: {json.dumps(field_dict, indent=2)}")

    return field_dict


def update_issue_field(item_id, field_id, value_id, field_type="singleSelect"):
    """Update a custom field of an issue in the GitHub Project."""
    time.sleep(2)  # Delay to prevent API rate limits

    # First, check the current value of the field before updating
    existing_value = check_issue_status(item_id, field_id)
    if existing_value == value_id:
        print(f"🔄 Skipping update: Field (ID: {field_id}) already has value (ID: {value_id})")
        return

    value_dict = {}
    if field_type == "singleSelect":
        value_dict["singleSelectOptionId"] = value_id
    elif field_type == "iteration":
        value_dict["iterationId"] = value_id  # ✅ Correct handling for Iteration fields
    else:
        value_dict["text"] = value_id  # Use text value for other fields

    mutation = {
        "query": """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $projectId,
            itemId: $itemId,
            fieldId: $fieldId,
            value: $value
          }) {
            projectV2Item {
              id
            }
          }
        }
        """,
        "variables": {
            "projectId": PROJECT_ID,
            "itemId": item_id,
            "fieldId": field_id,
            "value": value_dict
        }
    }

    response = requests.post(GITHUB_GRAPHQL_URL, json=mutation, headers=HEADERS)

    if response.status_code == 200:
        print(f"✅ Updated {field_type} field (ID: {field_id}) with value (ID: {value_id}) successfully!")
    else:
        print(f"❌ Error updating field: {response.status_code}, {response.text}")

    # Re-check if status is updated
    check_issue_status(item_id, field_id)


def check_issue_status(item_id, field_id):
    """Check if a specific field (e.g., Status, Priority) was successfully updated."""
    check_query = {
        "query": """
        query($itemId: ID!) {
          node(id: $itemId) {
            ... on ProjectV2Item {
              fieldValues(first: 10) {
                nodes {
                  __typename
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    id
                    optionId
                    field {
                      ... on ProjectV2FieldCommon {
                        id
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldTextValue {
                    id
                    text
                    field {
                      ... on ProjectV2FieldCommon {
                        id
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldNumberValue {
                    id
                    number
                    field {
                      ... on ProjectV2FieldCommon {
                        id
                        name
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
            "itemId": item_id
        }
    }

    response = requests.post(GITHUB_GRAPHQL_URL, json=check_query, headers=HEADERS)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Error decoding JSON response: {response.text}")
        return None

    # ✅ Handle API errors
    if response.status_code != 200:
        print(f"❌ GitHub API error: {response.status_code}, {response.text}")
        return None

    if "errors" in data:
        print(f"❌ GraphQL query error: {json.dumps(data['errors'], indent=2)}")
        return None

    if "data" not in data or "node" not in data["data"]:
        print(f"❌ Unexpected API response: {json.dumps(data, indent=2)}")
        return None

    # ✅ Extract field values
    for node in data["data"]["node"]["fieldValues"]["nodes"]:
        if "field" in node and node["field"] is not None:
            if node["field"].get("id") == field_id:
                return node.get("optionId") or node.get("text") or node.get("number")

    return None  # Field not found

def create_issue(owner, repo, issue):
    """Create an issue in the destination repository and return its node_id."""
    issue_body = issue.get("body", "") or ""
    assignees = [user["login"] for user in issue.get("assignees", [])]  # Extract assignees
    labels = [label["name"] for label in issue.get("labels", [])]  # Extract labels


    issue_data = {
        "title": issue["title"],
        "body": issue_body,
        "labels": labels,  # Include labels in the new issue
        "assignees": assignees  # Include assignees in the new issue
    }

    issues_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    response = requests.post(issues_url, json=issue_data, headers=HEADERS)

    if response.status_code == 201:
        created_issue = response.json()
        issue_node_id = created_issue["node_id"]
        print(f"✅ Issue '{issue['title']}' copied successfully. Issue Node ID: {issue_node_id}")
        return issue_node_id
    else:
        print(f"❌ Error creating issue: {response.status_code}, {response.text}")
        return None

def add_issue_to_project(issue_node_id):
    """Adds the created issue to a GitHub Project using GraphQL API and returns the item ID."""
    if not issue_node_id:
        return None

    graphql_query = {
        "query": """
        mutation($projectId: ID!, $contentId: ID!) {
            addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                item {
                    id
                }
            }
        }
        """,
        "variables": {
            "projectId": PROJECT_ID,
            "contentId": issue_node_id
        }
    }

    response = requests.post(GITHUB_GRAPHQL_URL, json=graphql_query, headers=HEADERS)

    if response.status_code == 200:
        item_id = response.json()["data"]["addProjectV2ItemById"]["item"]["id"]
        print(f"✅ Issue added to project successfully! Item ID: {item_id}")
        return item_id
    else:
        print(f"❌ Error adding issue to project: {response.status_code}, {response.text}")
        return None
    
def get_issue_project_fields(owner, repo, issue_number):
    """Fetch project-specific fields for a given issue."""
    query = {
        "query": """
        query($owner: String!, $repo: String!, $issueNumber: Int!) {
          repository(owner: $owner, name: $repo) {
            issue(number: $issueNumber) {
              id
              title
              projectItems(first: 10) {
                nodes {
                  project {
                    id
                    title
                  }
                  fieldValues(first: 20) {
                    nodes {
                      __typename
                      ... on ProjectV2ItemFieldSingleSelectValue {
                        field {
                          ... on ProjectV2FieldCommon {
                            name
                          }
                        }
                        optionId
                        name
                      }
                      ... on ProjectV2ItemFieldTextValue {
                        field {
                          ... on ProjectV2FieldCommon {
                            name
                          }
                        }
                        text
                      }
                      ... on ProjectV2ItemFieldNumberValue {
                        field {
                          ... on ProjectV2FieldCommon {
                            name
                          }
                        }
                        number
                      }
                      ... on ProjectV2ItemFieldIterationValue {
                        field {
                          ... on ProjectV2FieldCommon {
                            name
                          }
                        }
                        iterationId
                        startDate
                        title
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
            "owner": owner,
            "repo": repo,
            "issueNumber": issue_number
        }
    }

    response = requests.post(GITHUB_GRAPHQL_URL, json=query, headers=HEADERS)

    try:
        response_json = response.json()
        
        # Check for GraphQL errors
        if "errors" in response_json:
            print(f"❌ GraphQL Errors: {json.dumps(response_json['errors'], indent=2)}")
            return {}

        issue_data = response_json.get("data", {}).get("repository", {}).get("issue")

        if not issue_data:
            print(f"❌ No issue data found in the response: {json.dumps(response_json, indent=2)}")
            return {}

        project_items = issue_data.get("projectItems", {}).get("nodes", [])

        if not project_items:
            print("❌ No project items found for the issue")
            return {}

        field_values = {}
        for project_item in project_items:
            for field_value in project_item.get("fieldValues", {}).get("nodes", []):
                field_name = field_value.get("field", {}).get("name")

                if not field_name:
                    continue

                if field_value["__typename"] == "ProjectV2ItemFieldSingleSelectValue":
                    # For single select, use the option name
                    field_values[field_name] = field_value.get("name")
                elif field_value["__typename"] == "ProjectV2ItemFieldTextValue":
                    field_values[field_name] = field_value.get("text")
                elif field_value["__typename"] == "ProjectV2ItemFieldNumberValue":
                    field_values[field_name] = field_value.get("number")
                elif field_value["__typename"] == "ProjectV2ItemFieldIterationValue":
                   field_values[field_name] = field_value.get("iterationId")

        print(f"🔍 Extracted Source Issue Fields: {json.dumps(field_values, indent=2)}")
        return field_values

    except Exception as e:
        print(f"❌ Error processing issue project fields: {e}")
        return {}
    
def copy_issues():
    """Copy all issues and preserve all custom fields from the source project."""
    issues = get_issues(SOURCE_OWNER, SOURCE_REPO)

    if not issues:
        print("No issues found.")
        return

    # Fetch project custom fields for both source and destination
    source_custom_fields = get_custom_fields()  # Source project fields
    target_custom_fields = get_custom_fields()  # Destination project fields

    for issue in issues:
        # Extract source issue project fields
        source_project_fields = get_issue_project_fields(SOURCE_OWNER, SOURCE_REPO, issue["number"])
        print(f"🔍 Source Issue Fields: {json.dumps(source_project_fields, indent=2)}")

        # Create issue in destination repo
        issue_node_id = create_issue(DEST_OWNER, DEST_REPO, issue)
        if issue_node_id:
            # Add issue to project
            item_id = add_issue_to_project(issue_node_id)

            if item_id:
                time.sleep(2)  # Ensure GitHub API processes the issue addition

                for field_name, field_data in target_custom_fields.items():
                    if field_name in source_project_fields:
                        source_value = source_project_fields[field_name]

                        # Determine the field type
                        field_id = field_data["id"]
                        field_type = field_data["type"]
                        field_options = field_data.get("options", {})

                        # Handle Type Field
                        if field_name == "Type" and field_type == "ProjectV2SingleSelectField":
                            type_value_id = field_options.get(source_value)
                            if type_value_id:
                                update_issue_field(item_id, field_id, type_value_id, field_type="singleSelect")
                                print(f"✅ Type '{source_value}' applied to issue '{issue['title']}'")
                            else:
                                print(f"⚠️ Could not find matching Type '{source_value}' in the destination project")

                        # Handle Single Select Fields (e.g., Status, Priority, Size)
                        elif field_type == "ProjectV2SingleSelectField":
                            value_id = field_options.get(source_value)
                            if value_id:
                                update_issue_field(item_id, field_id, value_id, field_type="singleSelect")
                                print(f"✅ {field_name} '{source_value}' applied to issue '{issue['title']}'")
                            else:
                                print(f"⚠️ Could not find {field_name} '{source_value}' in destination project")
                                
                        # Handle Iteration Fields
                        elif field_type == "ProjectV2IterationField":
                            source_iteration_id = source_value  # This should be the source iteration ID

                            # Map to the target iteration ID
                            target_iteration_id = ITERATION_ID_MAP.get(source_iteration_id)

                            if target_iteration_id:
                                update_issue_field(item_id, field_id, target_iteration_id, field_type="iteration")
                                print(f"✅ Iteration mapped: '{source_iteration_id}' → '{target_iteration_id}' for issue '{issue['title']}'")
                            else:
                                print(f"⚠️ No mapping found for iteration ID: {source_iteration_id}, skipping iteration update.")
        



if __name__ == "__main__":
    copy_issues()
