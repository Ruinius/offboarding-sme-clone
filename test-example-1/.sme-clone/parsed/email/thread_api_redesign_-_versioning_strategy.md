# API Redesign - versioning strategy

> **Thread:** API Redesign - versioning strategy
> **Participants:** Alex Kim, Jane Doe, Priya Patel
> **Date range:** Mon, 03 Feb 2025 10:00:00 -0800 — Wed, 05 Feb 2025 09:15:00 -0800
> **Messages:** 3

---

**Jane Doe <jane@example.com>** — Mon, 03 Feb 2025 10:00:00 -0800

Hey team,

TL;DR — I think we should go with URL-based versioning for breaking changes. Here’s why:

1. Clients struggle with custom headers. We tried header-based versioning on the billing API last year and adoption was painful.
2. URL-based is explicit — /v1/users vs /v2/users. No ambiguity.
3. For additive, non-breaking changes: no versioning needed. Just ship it.

For deprecation, I propose sunset headers with 90-day enforcement:
- Day 0: Add Sunset header to deprecated endpoints
- Day 30: Start logging warnings for top 10 consumers
- Day 60: Email consumers directly with migration guide
- Day 90: Return 410 Gone

We did this exact pattern for the billing API last year and it worked well.

---

**Alex Kim <alex@example.com>** — Mon, 03 Feb 2025 14:30:00 -0800

Makes sense. What about the migration plan for existing v1 endpoints?

---

**Jane Doe <jane@example.com>** — Wed, 05 Feb 2025 09:15:00 -0800

Three-phase plan:

Phase 1 (Weeks 1-2): Stand up v2 endpoints alongside v1. Shadow-mode routing — v2 handles traffic but we compare responses against v1 before committing.

Phase 2 (Weeks 3-4): Add sunset headers to v1. Start the 90-day clock.

Phase 3 (Week 12): Decommission v1. Ship it.

The key lesson from the billing migration: never skip shadow mode. We caught 3 edge cases that would have been production incidents.

---
