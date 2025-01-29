---
name: User Story
about: New User Story
title: '[Story]: '
labels: ['User Story']
---

# Background
**Provide some context to help explain the feature that you are asking for**

...

# User Story

<details>
    <summary>Guidance on how to write user stories</summary>
    <p>Where possible, we prefer to frame each piece of work in terms of the features that it provides to users.</p>
    <p>After reading a user story, the team knows why they are implementing a feature, what they're building, and what value it creates.</p>
    <p>Good user story examples:</p>
    <pre>
As a security officer
I want approvals to be based on user roles (e.g., admin, developer, tester)
So that access to sensitive actions is restricted appropriately
    </pre>
    <pre>
As a DevOps engineer
I want to enforce an approval process for pipelines before they run in production
So that deployment risks are minimized
    </pre>
    <p>Bad user story examples</p>
    <pre>
As a developer
I want the system to be better
So that it works properly
    </pre>
<hr />
</details>

**Describe the feature you would like as one or more user stories** 

```text
As a []
I want to []
So that []
```

# Acceptance Criteria

<details>
    <summary>Guidance on how to write Acceptance Criteria</summary>
    <p>The acceptance criteria (ACs) of a feature are the criteria which must be met to mark a user story complete.</p>
    <p>ACs should be implemented as a numbered list, so that they can be referred to by their number.</p>
    <p>ACs should typically be phrased from the user's point of view, and should not be a list of technical tasks</p>
    <p>Good example of ACs:</p>
    <ol>
        <li>Only users with the appropriate role (e.g., admin or manager) must be able to approve sensitive actions.</li>
        <li>Approval requests must include a clear explanation of the action requiring approval.</li>
        <li>Approvers must have a way to audit their approvals for compliance purposes.</li>
        <li>Users without the required role must see a clear message explaining why they cannot approve the action.</li>
    </ol>
    <p>Bad example of ACs:
    <ol>
       <li>Implement a button for the approval process.</li>
       <li>The database must support indexing for faster queries.</li>
       <li>Write unit tests to ensure feature reliability.</li>
       <li>Use a dropdown menu for user role selection.</li>
    </ol>
<hr />
</details>

**What criteria has to be true for this feature to be considered as implemented?**

1. [...]
2. [...]


# Other Information
**Provide any useful additional information (links, notes etc), if applicable.**
