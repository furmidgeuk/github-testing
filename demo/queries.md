## DEMO QUERY REFERENCE

### Query 1: Total Costs by Business Application
**What It Shows**: Total annual costs for all business applications   
**Key Insight**: Uses EXPLODE to attribute shared resource costs to all associated business applications   
**When to Use**: Executive reporting, budget tracking, identifying top cost drivers   
**Talking Point**: "This shows all business application costs for the year - notice how EXPLODE attributes shared resources to each app that uses them."

### Query 2: Costs by EVP Area
**What It Shows**: Costs broken down by organizational unit (EVP area) and month   
**Key Insight**: Shows which business units are driving costs and how many workspaces they operate   
**When to Use**: Organizational chargeback, finance reporting, budget allocation   
**Talking Point**: "This is critical for finance - we can charge back to the right business units even when specific applications aren't tagged."

### Query 3: Unmapped Costs Analysis
**What It Shows**: Costs that couldn't be attributed to business apps (the 10-30% gap)   
**Key Insight**: Root cause column diagnoses why mapping failed - identity/warehouse needs registration, or resource type has no metadata   
**When to Use**: Data quality improvement, increasing attribution coverage, identifying what to add to dc-managed-services   
**Talking Point**: "Full transparency - we're at 70-90% coverage. The root_cause column tells you exactly what action to take for each unmapped cost."

---
