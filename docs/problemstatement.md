# Problem Statement

## Context

App Store and Play Store reviews are a noisy but high-signal stream of user feedback. Product, growth, support, and leadership teams rarely have time to read hundreds of recent reviews, yet those reviews often surface bugs, confusion, and feature gaps before they show up in tickets or analytics.

This project addresses that gap by turning recent public reviews (same product as Milestone 1) into a short, weekly pulse: themes, representative quotes, and concrete action ideas—then delivering that pulse through familiar Google Workspace surfaces so it is easy to share, archive, and act on.

The solution must stay within public review data (exports or feeds that do not require logging in as a user or scraping behind authentication), respect privacy (no PII in generated artifacts), and remain scannable so busy stakeholders can absorb it in under a minute.

## Core Problem

Pick the same product you selected in Milestone 1.

Turn recent App Store + Play Store reviews into a one-page weekly pulse containing:

- Top themes
- Real user quotes
- Three action ideas

Finally, send yourself a draft email containing this weekly note, and optionally maintain a running doc (for example, a Google Doc) for the pulse history—without building or maintaining custom OAuth clients or REST integrations against Google APIs in application code.

## Who This Helps

| Audience | Benefit |
|----------|---------|
| Product / Growth Teams | Understand what to fix or prioritize next |
| Support Teams | Know what users are saying and acknowledge patterns |
| Leadership | A quick weekly health pulse without deep-dive tooling |

## What You Must Build

1. Import reviews from the last 8–12 weeks (rating, title, text, date) from public sources only.
2. Group reviews into 5 themes max (e.g., onboarding, KYC, payments, statements, withdrawals).
3. Generate a weekly one-page note:
   - Top 3 themes
   - 3 user quotes
   - 3 action ideas
4. Deliver the pulse:
   - Draft an email with the note (send to yourself or an alias)
   - Where a written artifact in Docs is required, use the same delivery pattern via the Google Docs integration below
5. Do not include PII (no usernames, emails, or IDs in any artifacts).

## Integration Approach: MCP, Not Raw Google APIs

Google Docs and Gmail capabilities should be exercised through Cursor MCP servers (Model Context Protocol) that expose Docs and Gmail operations to the agent or workflow—not through hand-rolled Google Cloud projects, OAuth flows, and direct REST calls to the Google APIs from your app’s codebase.

Rationale:

- MCP centralizes authentication and tool boundaries in the server the IDE or host runs; your milestone work focuses on analysis and content, not API client maintenance.
- Consistency with how agents are expected to read and write docs and mail in this course: tools are declared and invoked as MCP resources, keeping the problem statement aligned with the prescribed stack.

Implication for the build: the draft email and any write-to-Google-Doc steps are satisfied by configuring and using the appropriate Google Docs MCP server and Gmail MCP server (or a combined Google Workspace MCP offering, if that is what your environment provides), so that composition, sending drafts, and doc updates happen through those tool surfaces rather than embedding `googleapis` SDK calls or custom HTTP clients in your own code.

## Key Constraints

- Use public review exports only — no scraping behind logins.
- Max 5 themes when clustering.
- Keep notes scannable, ≤250 words for the main pulse body.
- No usernames, emails, or IDs in any generated artifacts (quotes should be paraphrased or anonymized where needed to avoid PII).
