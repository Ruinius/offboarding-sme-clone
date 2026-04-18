# Thread: API Redesign Discussion

> Parsed from: `sample_emails.mbox`
> Thread participants: Jane Doe, Alex Kim, Priya Patel
> Date range: 2025-02-03 to 2025-02-05

---

**From:** Jane Doe (jane@example.com)
**To:** Alex Kim, Priya Patel
**Date:** 2025-02-03 11:15
**Subject:** RE: API Redesign — my take on versioning

Alex, Priya —

I've been thinking about the versioning question. Here's my recommendation:

1. **URL-based versioning** (`/v2/resource`) for breaking changes. I know header-based versioning is "cleaner" in theory, but in practice our clients struggle with custom headers and our API gateway handles URL routing natively.

2. **Sunset headers** on deprecated endpoints. Give clients 90 days notice, enforce it. We tried "soft deprecation" last year and it just meant we maintained two versions forever.

3. **No versioning for additive changes.** New fields, new optional parameters — just ship them. Our schema is designed to tolerate unknown fields.

The key principle: make the easy thing correct and the wrong thing hard. If a client is on v1, they should get v1 behavior forever until they explicitly opt into v2.

— Jane

---

**From:** Jane Doe (jane@example.com)
**To:** Alex Kim, Priya Patel
**Date:** 2025-02-05 09:30
**Subject:** RE: RE: API Redesign — my take on versioning

To answer your question about the migration path — I'd do it in three phases:

**Phase 1:** Ship v2 endpoints alongside v1. Both live. No client changes required.
**Phase 2:** Add sunset headers to v1. Start the 90-day clock. Send direct emails to top 10 consumers.
**Phase 3:** After 90 days, v1 returns 410 Gone with a redirect hint to v2.

We did this exact pattern for the billing API last year and it went smoothly. The trick is the direct emails — automated deprecation notices get ignored, but a personal "hey, you need to migrate by March 1st" email gets action.

— Jane
