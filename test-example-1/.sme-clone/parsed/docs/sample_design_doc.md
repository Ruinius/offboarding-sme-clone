# Sample Design Doc

> Parsed from `sample_design_doc.pdf`

---

## Page 1

API Gateway Routing Refactor - Design Document
Author: Jane Doe
Date: 2025-01-16
Problem Statement
The current routing uses a nested if/else chain.
This is O(n) and causes p99 latency spikes during deploys.
