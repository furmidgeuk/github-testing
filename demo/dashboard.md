## DASHBOARD TAB REFERENCE GUIDE

Use this section to prepare for questions about what each dashboard tab shows.

### Tab 1: Yearly Cost Overview
**Audience**: Executives, finance teams, annual planning
**Number of Panels**: 3

**What It Shows**:
- **Panel 1 - Yearly Tagged and Untagged Costs**: Stacked bar chart showing monthly costs broken into two categories:
  - **Tagged Costs** (blue): Costs successfully attributed to business applications (70-90% coverage)
  - **Unstructured Costs** (orange): Costs that couldn't be mapped to business applications (10-30% gap)
- **Panel 2 - Attribution Coverage Percentage**: Shows the percentage breakdown between tagged and unstructured costs
- **Panel 3 - Additional metrics**: May show total costs or other summary statistics

**Key Terminology**:
- **"Tagged costs"** = Costs mapped to business applications (WHERE business_application_ids has values)
- **"Unstructured costs"** = Unmapped/untagged costs (WHERE business_application_ids is NULL or empty)
- Better terms would be "mapped" vs "unmapped" - the data is structured, just not attributed

**Use Cases**:
- Tracking attribution coverage trends over time
- Quarterly business reviews showing total Databricks spend
- Monitoring data quality improvements as teams register service principals
- Executive reporting on cost visibility improvements

**Sample Question**: "Why do we have 'unstructured costs'?"   
**Answer**: "Unstructured costs are workloads we haven't mapped to business applications yet - either because the identity isn't in dc-managed-services, or the Databricks resource type doesn't provide identity metadata. Use Query 3 to see exactly what needs to be registered to improve coverage."

---

### Tab 2: Costs by PRD Workspace (EVP Area)
**Audience**: Finance teams, organizational cost allocation
**Number of Panels**: 12 (most detailed tab)

**What It Shows**:
- **EVP Area Cost Breakdown**: Pie or bar chart showing costs by organizational unit (PSQ, RDCL, etc.)
- **Workspace-Level Summaries**: Individual workspace costs
- **EVP Area Trends**: Month-over-month cost changes by EVP area
- **Workspace Utilization Metrics**: DBUs consumed per workspace
- **Top Workspaces Ranking**: Most expensive workspaces
- **Additional drill-down panels**: Detailed workspace analysis, SKU breakdown by workspace

**Use Cases**:
- Organizational chargeback (charging costs to business units)
- Workspace cost allocation when business apps aren't tagged
- Identifying which business units have highest cloud spend
- Budget allocation by organizational unit

**Sample Question**: "How do we allocate costs to EVP areas for untagged workloads?"   
**Answer**: "Tab 2 shows this. Every workspace maps to an EVP area in dc-managed-services. Untagged costs automatically roll up to the workspace's EVP area for chargeback."

---

### Tab 3: Costs by Business Applications in PRD
**Audience**: Application owners, product teams
**Number of Panels**: 1 visualization panel

**What It Shows**:
- **Yearly Cost Overview by Business Application**: Stacked bar chart showing all business application costs across 12 months
- **Business Application Names**: Retrieved from ServiceNow CMDB for human-readable names
- **Monthly Trends**: See how each application's costs change month-to-month
- **No Interactive Filters**: Chart shows all months and all applications (use SQL queries for filtering)

**Use Cases**:
- Answering "How much does [my app] spend on Databricks?"
- Application-level budget tracking
- Identifying applications with cost spikes across the year
- Cost accountability for product teams

**Sample Question**: "My application costs seem high this month - why?"   
**Answer**: "Tab 3 shows your app's costs across the full year visually. For detailed filtering and drill-down, use Query 1 (total costs by business application) to see specific numbers, then Query 3 to identify unmapped costs."

---

### Tab 4: Business Apps Costs by Product
**Audience**: Architects, platform teams, optimization teams
**Number of Panels**: 3

**What It Shows**:
- **Panel 1**: Cost breakdown by Databricks SKU type
  - JOBS_LIGHT_COMPUTE (serverless jobs)
  - ALL_PURPOSE_COMPUTE (classic interactive clusters)
  - SQL_COMPUTE (SQL warehouses)
  - DLT_CORE_COMPUTE (Delta Live Tables)
  - SERVERLESS_SQL_COMPUTE (serverless SQL)
- **Panel 2**: Business Application × SKU Matrix (which apps use which products)
- **Panel 3**: Resource efficiency metrics (cost per DBU by SKU type)

**Use Cases**:
- Understanding WHAT business applications are consuming (jobs vs interactive vs SQL)
- Optimization opportunities (e.g., migrate from classic compute to serverless)
- Identifying inefficient resource usage patterns
- Architectural decisions (should we use serverless or classic?)

**Sample Question**: "Why did our costs spike last month?"   
**Answer**: "Tab 4 can help diagnose this. If you see a spike in DLT_CORE_COMPUTE, it means you started running Delta Live Tables pipelines. If it's ALL_PURPOSE_COMPUTE, it might be developers running interactive clusters that weren't shut down."

---

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
