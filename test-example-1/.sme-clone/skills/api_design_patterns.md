---
skill: api_design_patterns
sme: Jane Doe
domains: [API design, versioning, routing, gateway architecture]
generated: 2025-03-01
---

# SKILL: API Design Patterns

> This skill captures Jane Doe's decision-making logic for API design, versioning, and gateway architecture.

## Triggers

Consult this skill when someone asks about:

- How to version an API (breaking changes, deprecation)
- API gateway routing architecture
- Middleware composition patterns
- Migration strategies for API infrastructure changes
- Performance optimization of request routing

## Decision Trees

### When to version an API endpoint

```
Is the change breaking? (removes fields, changes types, alters behavior)
├── YES → Use URL-based versioning (/v2/resource)
│         Add sunset headers to old version
│         Enforce 90-day deprecation window
│         Send personal emails to top consumers
│
└── NO → Is the change additive? (new fields, new optional params)
    ├── YES → Ship without versioning. Schema tolerates unknown fields.
    └── NO → Evaluate case-by-case. Likely not a real change.
```

### How to migrate API infrastructure safely

```
1. Build new component with 100% test coverage
2. Deploy in shadow mode alongside existing component
3. Compare outputs for divergence (any divergence = bug)
4. Run shadow mode for minimum 7 days with zero divergence
5. Cut over to new component
6. Keep old component available for 48-hour rollback window
```

## Evidence

| Claim | Source |
| :---- | :----- |
| URL-based versioning preferred over header-based | [thread_api_redesign.md](../parsed/email/thread_api_redesign.md) — "clients struggle with custom headers" |
| 90-day sunset window with direct emails | [thread_api_redesign.md](../parsed/email/thread_api_redesign.md) — "automated deprecation notices get ignored" |
| Radix trie for route matching | [sample_design_doc.md](../parsed/docs/sample_design_doc.md) — O(k) vs O(n) lookup |
| Shadow-mode validation pattern | [sample_design_doc.md](../parsed/docs/sample_design_doc.md) — "zero divergence for 7 consecutive days" |
| 33% p99 latency improvement from routing refactor | [general.md](../parsed/slack/general.md) and [sample_design_doc.md](../parsed/docs/sample_design_doc.md) |
