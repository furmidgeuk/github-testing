# FinOps Demo Presenter Script

## Pre-Demo Checklist

- [ ] Databricks workspace open with dashboard loaded
- [ ] SQL editor ready with sample queries
- [ ] Demo slides open in presentation mode
- [ ] Backup screenshots ready (in case of connectivity issues)

## INTRODUCTION 

### Slide 1: Title 

**SAY:**
> "Good morning everyone. Today I'm going to show you our FinOps Cost Attribution Solution - a system that automatically tells us which business applications are driving our Databricks costs.

### Slide 2: The Problem 

**SAY:**
> "Let me start with the problem we were trying to solve.

> Before this solution, if someone asked 'How much is their business application spending on Databricks?' - we couldn't answer that question easily.

> We had usage data from Databricks, but no way to connect it to business applications. 

> And without this visibility, chargeback is essentially impossible - we cannot fairly allocate costs to the right teams."

**PAUSE** for 2 seconds to let this sink in

**SAY:**
> "So the core question we needed to answer was: For any given Databricks cost, which business application should it be attributed to?"

### Slide 3: The Solution 

**SAY:**
> "What we've built is an automated cost attribution system that:
> - Attributes costs to over 100 business applications
> - Refreshes daily - so costs are visible within 24 hours
> - Achieves 70 to 90 percent attribution coverage
> - And provides self-service dashboard and queries for teams to analyze their own costs

> Let me show you how it works."

## DATA FLOW & ATTRIBUTION LOGIC 

### Slide 4: Architecture Overview 

**SAY:**
> "Here's the end-to-end architecture - just the essentials.

> We have two main data sources:
> 1. **dc-managed-services** on GitHub - where teams define their service principals and user groups
> 2. **Databricks System Tables** - raw usage data: who ran what, when, and how many DBUs

**SAY:**
> "Three pipelines run daily:
> - **ingest-github** pulls business application mappings
> - **dc-ingest-system** pulls Databricks system tables 
> - **transform-finops** joins everything together

> From there, teams can access the data through a dashboard and SQL queries."

### Slide 5: The Attribution Logic 

**SAY:**
> "This slide shows our attribution logic - the fallback strategy for determining which business application owns a cost.

> We check identity fields in priority order: run_as → created_by → owned_by → cluster owner → warehouse creator.

> Once we find an identity, we look it up in dc-managed-services to get the business application.

> If no match is found, it becomes 'untagged' and charged to the EVP area."

**KEY POINTS:**
> "We support three identity types:
> - **Service Principals** - most reliable, used by automated jobs
> - **User Groups** - mapped to business applications
> - **Individual Users** - mapped through group membership

> For shared resources, costs are attributed to all associated business applications - meaning each app sees the full cost of resources they have access to through their service principals or user groups."

### Slide 6: Shared Resource Handling 

**SAY:**
> "Let me clarify how we handle shared resources - this is important for understanding the cost numbers you'll see.

> When a resource is shared - for example, a user belongs to multiple user groups, each mapped to different business applications - we use SQL's EXPLODE function to attribute costs.

> Here's the key point: each business application sees the **full cost** of shared resources they have access to.

> For example, if a $300 warehouse is shared by 3 applications, each application shows $300 in their costs - not $100.

> **Why full attribution instead of dividing by 3?**
> We can't fairly divide costs without knowing exact usage percentages - which app runs 90% of the queries vs just 10%?
> Because if your service principal is on that resource, you have the ability to optimize or remove it.
> Showing you the full $300 creates accountability and a strong incentive to act. 

> This means if you sum all business application costs together, the total will be higher than the actual Databricks invoice. But for driving cost optimization behavior, this approach works better than diluting costs across teams."

**KEY POINTS:**
> - Shared resource costs are **attributed** to all associated business applications (not divided)
> - Each app sees the **full cost** of resources they access
> - Can't fairly divide without usage percentages (which app uses 90% vs 10%?)
> - Sum of all business app costs > actual invoice (due to cost duplication on shared resources)

### Slide 7: Self-Service Dashboard & Query Library 

**SAY:**
> "So how do teams actually access all this cost data? We've built two self-service tools.

> First, a **Databricks dashboard** with 4 tabs:
> - Tab 1: Yearly cost overview showing tagged vs untagged costs
> - Tab 2: Costs by EVP area for organizational chargeback
> - Tab 3: Costs by business application - the core use case
> - Tab 4: Costs by product type for optimization insights

> Second, a **library of ready-to-use SQL queries**. Teams can run these directly in Databricks SQL or customize them for their needs. We have queries for:
> - Top business applications by cost
> - Costs by EVP area
> - Unmapped costs analysis
> - And many more for specific use cases

> Let me show you both in action."

**KEY POINTS:**
> - **Self-service**: No waiting for reports - teams query their own costs
> - **Dashboard**: Visual overview for executives and stakeholders
> - **SQL Queries**: Detailed analysis and filtering for power users

## LIVE DEMO 

### DEMO PART 1: Dashboard Walkthrough 

**SAY:**
> "Now let me show you the live dashboard. We have 4 tabs that serve different audiences."

---

#### Tab 1: Yearly Cost Overview

**DO:** Navigate to "Yearly cost overview" tab

**SAY:**
> "Tab 1 is the executive summary - shows our total annual Databricks spend broken down into two categories.

> The green bars show 'tagged costs' - these are costs successfully attributed to business applications. This represents our 70-90% coverage.

> The blue shows 'unstructured costs' - this is the 10-30% that couldn't be mapped to business applications yet. 

> This chart helps us track our attribution coverage over time - ideally we want to see the blue shrinking.

**POINT OUT:**
- Monthly breakdown of tagged vs unstructured (unmapped) costs
- Attribution coverage trends month-over-month
- Total Databricks spend per month

--

#### Tab 2: Costs by PRD Workspace (EVP Area)

**DO:** Navigate to "Costs by PRD workspace (EVP area)" tab

**SAY:**
> "Tab 2 is where finance teams live - this breaks down costs by organizational unit (EVP area) and by individual workspaces.

> This is critical for chargeback - we can allocate costs to the right business unit even if specific business applications aren't tagged.

> [Point to a panel] Here you can see which EVP areas are spending the most, and drill down to specific workspaces."

**POINT OUT:**
- EVP area cost breakdown
- Workspace-level summaries
- Month-over-month trends by EVP area

---

#### Tab 3: Costs by Business Applications in PRD

**DO:** Navigate to "Costs by Business applications in PRD" tab

**SAY:**
> "Tab 3 is the core use case - costs by business application. Before this solution, we couldn't answer 'how much does a particular business application spend on Databricks?' Now it's right here.

> This shows all business application costs across the year. You can see which applications are the biggest spenders and how costs trend month-to-month."

**POINT OUT:**
- Yearly cost overview by business application
- Monthly trend visualization showing all 12 months
- Business application names pulled from ServiceNow

---

#### Tab 4: Business Apps Costs by Product

**DO:** Navigate to "Business apps costs by product" tab

**SAY:**
> "Tab 4 shows WHAT business applications are using - are they running serverless jobs, SQL warehouses, or classic compute clusters?

> This helps with optimization - for example, migrating from classic compute to serverless can reduce costs significantly."

**POINT OUT:**
- Cost breakdown by SKU type (JOBS_LIGHT_COMPUTE, SQL_COMPUTE, etc.)
- Which apps use which products
- Resource efficiency metrics

**TRANSITION:** Switch to SQL editor

---

### DEMO PART 2: SQL Queries 

**SAY:**
> "Now let me show you the self-service SQL queries. We have a number of ready-to-use queries for different analyses. I'll demonstrate the three most popular ones."

---

#### Query 1: Total Costs by Business Application

**DO:** Run the query

**SAY:**
> "Query 1 shows total costs by business application for the year. Notice the EXPLODE function - that's how we attribute shared resource costs to all associated business applications.

> [Point to results] You can see the business application names pulled from ServiceNow, the costs formatted in dollars, and the number of usage records for each application."

---

#### Query 2: Costs by EVP Area

**DO:** Run the query

**SAY:**
> "Query 2 shows costs broken down by organizational unit - our EVP areas - over time.

> [Point to results] This is critical for chargeback. You can see which business units are spending the most, how many workspaces they have, and the monthly trends."

---

#### Query 3: Unmapped Costs Analysis

**DO:** Run the query

**SAY:**
> "Query 3 shows transparency - what's NOT mapped yet. We're at 70-90% coverage.

> [Point to root_cause column] This is the key diagnostic column - it tells us exactly why each cost couldn't be mapped:
> - 'run_as not mapped' or 'created_by not mapped' means that service principal or user exists but isn't registered in dc-managed-services
> - 'warehouse creator not mapped' means we need to add that warehouse's creator to dc-managed-services
> - 'no identity metadata available' means the Databricks resource type doesn't provide identity information - nothing we can do about these

> [Point to identity column] When identity shows an actual ID (not 'NONE'), that's the specific service principal or user that needs to be added to dc-managed-services.

> [Point to warehouse_id column] When identity is 'NONE' but warehouse_id has a value, we need to find who created that warehouse and then register that creator in dc-managed-services."


**TRANSITION:** Open for questions

---

## Q&A [11:00+]

**SAY:**
> "That's the 10-minute tour. Happy to take questions about the solution, dashboard access, or your specific application's costs."

