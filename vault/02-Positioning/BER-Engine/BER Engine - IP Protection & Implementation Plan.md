## Purpose & Scope

This is a personal working note, separate from the pitch document (_Executive Strategy Brief: Facade Physical-Risk Advisory_). That document makes the case to a target firm; this one covers how to protect the underlying IP and sequence the build so the pitch's "near-zero Director time" claim holds up in practice, not just on paper.

## IP Ownership Structure

- **Vehicle:** Shim Systems — an existing, dormant company, sole director, no trading history. A clean shell for this purpose, with no other liabilities or activity to mix with.
- **Mechanics:** assign the existing PoC code, design brief, and architecture decisions to Shim Systems with a dated record (director's resolution or IP assignment deed), timestamped before any employment discussion advances. This is what gives the "pre-existing platform IP" framing real evidentiary weight later.
- **Ongoing record-keeping:** commit to a private repo under a consistent, dedicated identity, with descriptive commit messages (not "wip"/"fix"), unsquashed history, and a server-side timestamp rather than local-only commits. This is what keeps the dated record credible as it grows, not just the initial assignment.
- **Licence to the employing firm:** covers the deployed, configured instance; perpetual and irrevocable; explicitly survives departure or Shim Systems ceasing to operate.
- **Continuity safeguard:** source-code escrow with a neutral third party, released to the firm automatically on specified trigger events (departure, insolvency, support lapse). Standard practice in enterprise software procurement, not a novel ask.
- **Competitive safeguard (if needed):** an exclusive licence within the firm's sector and geography for a fixed term, rather than broader ownership.
- **Boundary that stays constant:** firm-specific integration work, workflow customisation, and anything built against the firm's own project data during the engagement sit with the firm as ordinary work product. Only the underlying platform is licensed, not assigned.

## Build Plan

- **Current state:** the feasibility approach (extrude + boolean-subtract) is validated via a working PoC. Studio (footprint authoring) and Engine (downstream: floor-plate extraction, adjacency, JV3/daylight/WUFI/carbon) are architecture decisions, not built software yet.
- **Phase 1 — narrow vertical slice (solo, pre-role):** one real, credible worked example, end to end — a single representative building, simple massing, skipping complex roofs, skylights, daylight and carbon for now — geometry in, JV3-grade thermal-bound output out. Scoped to roughly 2–3 weeks; proves the core claim without committing to the full general tool.
- **Phase 2 — expansion (contractor-funded, post-role):** once in the role and on salary, engage a contractor for a roughly 3-week sprint to broaden coverage (roof types, building typologies, remaining modules). Lower risk once Phase 1 has retired the open technical question of whether the approach works at all.
- **Contractor IP:** the engagement agreement must assign work product to Shim Systems explicitly — a contractor's default rights aren't automatic.
- **Bandwidth:** directing a contractor sprint well needs real attention (domain calls, review). Time it to land just before the role's start date, or expect it to run slower if it overlaps the first weeks of ramping in.

## Negotiation Sequencing & Timing

- Use the gap between "serious interest" and "signed and started" as build time — realistically several weeks for a Director-level role that's being created rather than posted, not a fixed date to beat.
- The build doesn't need to be finished by signature; it needs to be visibly progressing by the point real terms are discussed.
- Consider raising the ownership structure early (the first real conversation, not the first coffee) to gauge reaction before committing to a build timeline — a quick negative reaction there saves weeks of building toward a structure that was never going to land.
- If the process moves faster than the narrow-slice build: show the validated PoC and architecture as proof of trajectory, with the working slice as a scheduled deliverable rather than a precondition.
- **Present the engine as a vendor-style deliverable, not a hedge.** The employment structure itself doesn't change — this is about how the IP/engine is described in conversation: definitively, as something already built and licensed through Shim Systems, not as "I could build this once I'm in the role." Confidence here should track the actual build state: the ownership terms are solid now and can be stated boldly; claims about the engine itself being finished should track the Build Plan's actual progress, not run ahead of it.

## Talking Points: The Ownership Conversation

Reframe: not "Jon owns some IP," but "you get an embedded specialist plus a piece of vendor software that happens to travel with him — the same as buying IES or DesignBuilder and hiring someone who knows it cold, except this one's built specifically for how you work, with an escrow so you're never dependent on Jon personally to keep using it."

Analogies, roughly in order of use:

1. **Wind engineering subconsultant model** (open with this) — facade firms already send wind-loading work to specialists who own their own methodology and deliver findings, not source code. Same principle, brought in-house.
2. **The senior engineer's personal toolkit** (if they push on employee vs. subcontractor) — every firm already carries this risk informally, today, with zero protection. This is that same normal arrangement, just formalised and actually protected.
3. **Plant hire with a dedicated operator** (for the exclusivity question) — you don't own the crane, but for something schedule-critical you negotiate exclusive use for the job.
4. **Enterprise software escrow** (close with this) — source escrow is standard practice any time a business licenses vendor software that matters to them. Not exotic, just applied carefully here.

## Open Questions

- How early to raise the IP/licensing structure — the first real conversation, or only once genuine interest is established?
- Remuneration structure (base + variable, staged title/review points) — benchmarked separately, not yet reconciled with the IP/licensing terms above.
- How assertively to describe the engine's readiness before the narrow-slice build is actually finished — overselling maturity risks a credibility problem if pressed for a demo early.
- Personal weakness: originating top-of-funnel leads solo (historically handled by a co-director or a dedicated salesperson) — not addressed in this note.