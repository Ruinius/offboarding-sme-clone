# #general

> **Channel purpose:** General team discussion

> **Date range:** 2025-01-15 16:00 UTC — 2025-01-17 16:00 UTC | **Messages:** 5

---

**Jane Doe** — 2025-01-15 16:00 UTC

TL;DR — I’m going to refactor the API gateway routing. The current nested if/else chain is O(n) and we’re seeing p99 latency spikes during deploys. Plan is to replace it with a radix trie.

**Alex Kim** — 2025-01-15 16:10 UTC

Interesting. What’s the expected improvement?

**Jane Doe** — 2025-01-15 16:20 UTC

Based on the benchmarks I ran yesterday, we should see ~33% p99 reduction. I’ll share the design doc later today.

**Jane Doe** — 2025-01-16 16:00 UTC

Design doc is up: https://docs.example.com/api-gateway-refactor. @Alex Kim can you review the migration plan section?

**Jane Doe** — 2025-01-17 16:00 UTC

Deployed the trie router to staging. Smoke tests passing. Going to let it soak for 48 hours before we push to prod.
