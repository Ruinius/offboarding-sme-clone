# API Gateway Routing Refactor — Design Document

> Parsed from: `sample_design_doc.pdf`
> Author: Jane Doe
> Date: 2025-01-16

## Problem Statement

The current API gateway routes requests using a nested if/else chain that has grown to 200+ conditions. This causes:

- **High latency:** O(n) route matching on every request. P99 is 45ms for routing alone.
- **Fragile deployments:** Adding a new route requires modifying a monolithic function. Merge conflicts are frequent.
- **No middleware hooks:** Auth, rate limiting, and logging are scattered across individual route handlers instead of being composable.

## Proposed Solution

Replace the if/else chain with a **radix trie** (compressed prefix tree) for route matching.

### Why a radix trie?

- O(k) lookup where k = length of the URL path (not the number of routes).
- Naturally supports parameterized routes (`/users/:id/orders`).
- Middleware can be attached at any node in the trie, enabling route-level composition.

### Architecture

```
Request → Trie Lookup → Middleware Chain → Handler → Response
              │
              ├── /api/v1/users/*  → [auth, rateLimit] → usersHandler
              ├── /api/v1/orders/* → [auth, audit]     → ordersHandler
              └── /health          → []                 → healthHandler
```

### Migration Plan

1. Build the trie router as a standalone module with 100% test coverage.
2. Run it in shadow mode alongside the existing router for 2 weeks.
3. Compare routing decisions — any divergence is a bug.
4. Cut over once shadow mode shows zero divergence for 7 consecutive days.

## Expected Impact

- P99 routing latency: 45ms → ~30ms (33% reduction)
- New route deployment: 30 min → 5 min
- Middleware composition: manual → declarative
