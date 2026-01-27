### Q: "Why do you attribute the full cost to each app instead of dividing by 3? Won't that inflate the numbers?"

**A:** "Great question - this is a deliberate design choice. We use **full attribution** rather than cost division for three key reasons:

**1. Accountability and Optimization Incentives:**
If your service principal or user is on a $300 resource, you have the ability to optimize it. Showing you the full $300 creates a strong incentive to act. If we showed you $100, you might think 'it's only $100, not worth optimizing' - but you could potentially save the full $300 by optimizing or removing your access.

**2. You Can't Fairly Divide Without Usage Data:**
How do you split a shared warehouse cost fairly? Equal thirds? What if App A runs 90% of the queries and Apps B and C barely use it? We don't have reliable usage percentage data at the business application level, so any division would be arbitrary and potentially unfair.

**3. Transparency About What You're Using:**
Full attribution shows you every resource your identities touch. This helps with cost accountability - if your service principal is on something, you should know about it, investigate it, and decide if you need to be there.

**The Trade-off:**
Yes, this means if you sum all business application costs, the total will exceed the actual invoice due to shared resource duplication. For exact invoice reconciliation, use the EVP area view (Tab 2), which doesn't have this duplication. But for driving optimization behavior, full attribution works better."

**FOLLOW-UP IF ASKED:** "If there's strong demand for a divided cost view, we could add an alternative query that divides by the count of business applications. But so far, teams prefer seeing the full cost for accountability."

---

### Q: "What if my application's costs show up as untagged?"

**A:** "That means the identity running your workload isn't mapped in dc-managed-services. You should check that your service principals and user groups are properly defined in your service request. The NNDCP team can help with that."

### Q: "How accurate are the costs?"

**A:** "We use Databricks list prices from their official system tables. These are pre-discount prices, so actual invoiced amounts may differ due to enterprise agreements.

### Q: "Can I get more granular attribution - like by team within a business app?"

**A:** "Currently we attribute to the business application level. More granular attribution would require additional tagging in dc-managed-services. Let us know if there's demand for this."

### Q: "What are 'unstructured costs'? Is the data missing structure?"

**A:** "The term 'unstructured costs' is a bit misleading - it just means 'unmapped to business applications'. The data is fully structured. These are costs where the identity fields (run_as, created_by, etc.) either don't exist or weren't found in dc-managed-services. Query 3 shows you exactly what needs to be registered to convert these into tagged costs."

### Q: "Why is attribution coverage not 100%?"

**A:** "Some Databricks products don't provide identity metadata - like certain ML endpoints. Also, some older resources may have been created before proper tagging was in place. Additionally, some identities just haven't been registered in dc-managed-services yet. We're working to improve coverage over time."

### Q: "How do I add a new business application?"

**A:** "Submit a service request to dc-managed-services with your workspace requirements, service principals, and user groups. Once deployed, costs will automatically start attributing to your application."
