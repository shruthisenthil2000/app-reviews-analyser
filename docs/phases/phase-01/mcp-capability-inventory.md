# MCP capability inventory (Phase 1)

Complete this after Gmail and Google Docs MCP servers (or one combined **Google Workspace** MCP) are configured in Cursor.

**Do not paste tokens, client secrets, refresh tokens, or full OAuth payloads here.**

## Environment

| Field | Value (non-secret) |
|-------|---------------------|
| Cursor / host version | |
| Date inventory completed | |
| Operator Google account (label only, e.g. `team-lab-alias`) | |

## Server registration

| Server display name (as shown in MCP UI) | Purpose (Gmail / Docs / combined) | Package or repo URL (if applicable) |
|------------------------------------------|-----------------------------------|-------------------------------------|
| | | |
| | | |

## Capability map (architecture alignment)

Map each important capability to [architecture.md](../../architecture.md) **§5.4 Delivery layer**.

### Gmail MCP

| Tool or operation name | Creates draft? | Sends mail? | Reads threads? | Notes |
|------------------------|----------------|---------------|------------------|-------|
| | Yes / No | Yes / No | Yes / No | |
| | | | | |

**Planned use for this project:** Create **draft** to self or approved alias only (unless [decision.md](../../decision.md) records a change).

### Google Docs MCP

| Tool or operation name | Create doc | Append to doc | Update section | Read doc | Notes |
|--------------------------|-------------|---------------|----------------|----------|-------|
| | Yes / No | Yes / No | Yes / No | Yes / No | |
| | | | | |

**Planned use for this project:** Optional running log or weekly doc—record final workflow in [decision.md](../../decision.md) if Docs is waived.

## Gaps and mitigations

| Gap (e.g., no append) | Mitigation (e.g., new doc per week) | Owner |
|-----------------------|-------------------------------------|-------|
| | | |

## Evidence pointers (Phase 1 close)

- Redacted screenshot or note: MCP panel shows servers **without load errors** (T1.1).
- Paste: **non-sensitive** tool list summary (T1.2) or link to internal doc.
