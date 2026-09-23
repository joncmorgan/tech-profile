# Software Design Brief: BER-Engine (Envelope Geometry Engine)

**Project Title:** Building Envelope Rapid Engine (`ber-engine`) **Document Type:** System Architecture & UX Strategy Brief **Target Application:** Fast, reliable envelope authoring for a facade-engineering practice — feeding early-stage design advisory and NCC-methodology (JV3-equivalent) compliance work, plus daylight, hygrothermal, and carbon-takeoff workflows.

## 1. Executive Summary

The **BER-Engine** is an envelope-only geometry authoring tool. It does one thing — turn a building's massing into accurate, valid envelope geometry, fast — and deliberately does nothing else. It does not reinvent building physics: EnergyPlus, Radiance, and other standard tools remain the analytical engines throughout (Section 6). On modern hardware, simulation is effectively instantaneous; the time cost in this workflow has only ever been in authoring geometry and proving its quality. This tool exists to eliminate that cost, not to produce a different or better analytical answer than the incumbent tools (DesignBuilder, IES-VE, Better Building) already give.

The tool exists because geometry authoring, not analysis, has consistently been the highest-risk, hardest-to-debug part of this workflow in practice: vertex mismatches, sliver surfaces, and unreliable adjacency detection are symptoms of building geometry up from 2D floor plates, where nothing in the data model guarantees consistency between levels. BER-Engine avoids that failure mode structurally rather than managing it. At its core, the entire model file is a small, generic structure: a set of 2D polygons (with holes), each carrying a base height, a height, and a collection of attributes — nothing more elaborate is stored. Two properties do the work: every footprint is a constant-cross-section prism, so per-level floor plates are _derived_ by simple interval membership rather than independently redrawn (Section 4.1); and nothing beyond that plain prism — no window, roof, or shading detail — is ever a real 3D solid in the authoring model at all (Section 4.3–4.5). There is no second input to disagree with, and nothing extraneous for a boolean operation to get wrong, because nothing extraneous is ever really there. This is a genuinely different authoring architecture from DesignBuilder, IES-VE, or Better Building, all of which model geometry (including roofs) as real, directly-manipulated solids or surfaces even in their simplified modes.

The tool serves two project stages on an identical authoring workflow, differing in accuracy requirement and downstream output (Section 6):

- **Pre-planning** — architect-led, massing locked but design still evolving, producing a short bounding-advice pack ahead of the client's ESD consultant appointment. This is the intended first offering: a loss-leader service driving work into higher-margin facade consulting.
- **Remedial** — an existing building assessed for facade-upgrade compliance against NCC methodology, where the model must be defensible to a building surveyor. Intended as a second-stage capability once the pre-planning offering is running.

**Immediate purpose of this brief:** to validate that a proof-of-concept geometry tool covering Sections 2–4 is buildable in a short, defined timeframe — establishing the confidence needed to commit to the pre-planning loss-leader offering first, with remedial JV3-equivalent capability following within a following few-month build once the core tool is proven.

## 2. Data Model Hierarchy

The file format is deliberately minimal and holds three nested levels only:

- **Site** — the top-level container. Holds one or more Buildings, and the project-wide reference-angle set (Section 3), shared across every building on the site so neighbouring structures (a podium meeting a tower on an adjacent block, say) can align exactly.
- **Building** — a named collection of footprints that share a common vertical datum. Owns its own **Floor-Level Table** (storey names, relative levels, floor-to-floor heights) — real sites often carry two independent storey rhythms (e.g. a podium and a tower on separate structural grids), so levels belong to the building, not the project, and each building on a site can have its own. Also owns the **declarative rule set** (Section 4.3) governing that building's windows, constructions, and rule-based shading.
- **Footprint** — the base primitive (Section 3): a closed 2D polygon (holes permitted, for an internal courtyard or atrium void), a base height, a height, and a functional-use tag. Every footprint belongs to exactly one Building; the UI enforces this — there is no way to author an orphan footprint.

## 3. The Authoring Primitive

Every mass is an **extruded footprint**: a closed 2D polygon (optionally with holes), a base height, a height, a functional-use tag. A simple polygon extruded straight up is always a valid solid regardless of its shape — this primitive cannot produce non-manifold geometry, because there is no authoring path that can express one. The base height (rather than an implicit ground datum) is what lets a setback tower or a floating canopy be represented directly.

**Entry modes (no other file import is supported):**

- **Typed rectangle** — position, width, depth, height entered directly.
- **PDF-traced footprint** — an architectural drawing or site plan loaded as a background image; scale is calibrated once per page (click two points a known distance apart), then a closed polygon is traced and given a height.
- **Boolean union/difference** between footprints, for merging masses or cutting a courtyard.

### 3.1 Reference Angles & Guided Drawing

Architectural geometry is rarely arbitrary — walls, ridges, and sills overwhelmingly follow a small set of governing angles per building (usually an orthogonal grid, sometimes with one or two secondary angles for a rotated wing or an angled boundary). BER-Engine makes this explicit rather than incidental: every edge, in both typed and PDF-traced entry, must snap to a **defined reference angle** (Site-scoped, Section 2) — no free angle is permitted. This is the same "the tool structurally can't express the mistake" principle as the rest of Section 3, applied to direction instead of shape, and it directly simplifies downstream roof-form authoring (Section 4.4), since a ridge direction becomes a selection from the same angle set the walls already use.

- **Anchored, not averaged:** once a reference angle is defined, its stored value never moves. A new proposed angle within tolerance (0.5°, at 0.1° storage resolution) snaps silently to the existing anchor; it does not nudge the anchor toward itself, preventing drift across a long sequence of merges.
- **Mid-draw angle definition:** adding a new reference angle is a mode within the draw action — a key/button lets the user define a new angle without abandoning the polygon in progress; drawing resumes immediately, and the angle joins the site's permanent set.
- **Guide rendering:** guide rays project from the cursor along every reference angle, and from every existing vertex/edge across _all_ footprints on the site (not just the one being drawn) — enabling exact alignment between neighbouring masses, which materially improves Section 4.2's adjacency detection. The cursor snaps only to intersections between guides — standard 2D line-intersection math, well inside `shapely`'s scope.
- **Guide-overload mitigation:** guides are spatially culled to a bounded radius around the cursor, fade in only as the cursor approaches true alignment, and are capped at the nearest 3–4 candidates at once. At scale, a spatial index (e.g. `rbush`) keeps proximity queries performant.

### 3.2 Authoring Layout: Plan View, Live 3D, and Level Ghosting

Authoring happens in **plan view** — the natural surface for drawing, tracing, and applying the reference-angle guides above — with a **live, docked 3D panel** (not a pop-out) updating continuously alongside it, never a separate step the user has to remember to open. Plan view alone cannot surface a height error (a floating or mis-set-back mass looks identical from directly above), so the 3D panel is the working verification mechanism, not a nice-to-have render.

Overlapping footprints at different heights are visually hard to read in plan view alone. BER-Engine adopts the standard BIM pattern for this — **level-based visibility filtering**: the user selects a current Building level (from that building's Floor-Level Table), and every footprint not active at that level renders as a faded, non-interactive ghost outline beneath it — visible as spatial reference, unselectable, out of the way.

## 4. Geometry Kernel & Real-Time Preview

No general-purpose CAD kernel (FreeCAD/OpenCASCADE) or desktop CAD application (SketchUp) is used — both solve problems this tool doesn't have, at the cost of the fragility (unreliable booleans, healing algorithms) this brief exists to avoid.

**Governing principle:** the boolean solid is authored and composed as pure opaque volumes only. Windows, skylights, and roof forms are never boolean-modelled — they are descriptive attributes attached to a face, realized into real geometry only by whichever consumer downstream actually needs it. Nothing that isn't load-bearing for the solid's validity ever reaches a boolean operation, which is what keeps authoring robust: there is nothing left for a boolean to get wrong.

- **`shapely`** is the day-to-day geometry kernel — 2D polygon creation, boolean union/difference, and the overlap computations that drive adjacency (Section 4.2). Because every footprint stays a constant-cross-section prism, floor-plate extraction (Section 4.1) is interval membership plus a 2D union — never a 3D intersection.
- **`manifold`** is an on-demand, export-time helper only — invoked when a specific downstream consumer needs realized roof or opening geometry (a THERM section, a polished render). It never sits in the live authoring path.
- **`three.js`** (or equivalent WebGL viewer) renders the live 3D preview (Section 3.2) in the same browser process as the authoring canvas.
- **`pdf.js` / `PyMuPDF`** renders PDF backgrounds for the trace-and-calibrate authoring mode.

### 4.1 Floor-Plate Extraction

For each level in a Building's Floor-Level Table, every footprint whose $[base, base+height]$ range contains that $Z$ is collected and **unioned together** (a 2D `shapely` operation, distributing correctly over a horizontal slice of any 3D union) to form that level's floor plate — automatically, regardless of whether the user explicitly merged the relevant footprints while authoring. This is exact — no sliver handling is needed, since no footprint's cross-section is ever modified. The resulting per-level outline is also rendered in the live 3D view as an intersection line, at no extra computational cost — the same slice already being computed for extraction.

### 4.2 Adjacency & Boundary Conditions (first-order — must be exact)

For any two neighbouring footprints — stacked or lateral — the shared boundary's condition (external / internal / adiabatic) is derived from the overlap or shared edge of their footprints, using the same overlap logic in both cases: roof/floor exposure is the vertical case of the identical check used for lateral walls between neighbouring functional blocks. Where two neighbours have different heights, the shared wall is split at the shorter footprint's height.

### 4.3 Tagged Surfaces & the Declarative Rule Engine

Fenestration, construction assignment, and rule-based shading are not stored per-surface — that couples an instruction to specific geometry and breaks it the moment the geometry changes. Instead, every wall (and roof) surface is **automatically tagged**, fresh, whenever geometry is queried or exported:

- **Orientation** — the surface's outward normal, bucketed to the 8-point compass.
- **Floor** — from the owning Building's Floor-Level Table (the same Z-range membership already used for extraction).
- **Exposed / recessed** — a wall is _recessed_ if it sits behind the building's outer line at the level(s) immediately above and/or below by more than a threshold setback (default 300mm, worth validating against real stepped-massing examples before locking); otherwise _exposed_.

A **Building-level rule set** — the natural evolution of the original AI-parsed text brief — holds declarative instructions matched against these tags at query time, e.g. _"floors 1–3, exposed, east: windows 1.8m high, sill 200mm, 1.2m wide, 1.5m spacing"_, or equally _"floors 1–3, exposed, east: U-value 1.4, SHGC 0.35"_, or _"west, exposed: 600mm projecting eave."_ One generic mechanism serves window rules, construction/U-value assignment, rule-based shading, and (in the `remedial` stage) the upgrade-scope flag — rather than four separate ad hoc schemas. A rule is never baked onto a surface; it is matched fresh every time, so if geometry changes, no instruction is ever lost or orphaned. Where more than one rule matches the same surface, **the most specific match wins** (more matching tag constraints beats fewer) — the same resolution principle as CSS specificity, stated explicitly rather than left ambiguous.

Not everything belongs in the rule engine: a _specific_, one-off physical element — a particular existing eave photographed on a `remedial` site, a skylight at a specific position — is an authored **instance** (Section 4.5), not a pattern. The rule engine is for systematic, repeating instructions; instances are for singular, located things. Both can coexist on the same building.

### 4.4 Roof Forms (metadata, not geometry)

Walls stay vertical because roofs are never a boolean operation on the solid at all. A roof form — gable, hip, mono-pitch/skillion, flat-with-parapet — is stored as metadata on a footprint's flat top face (eave height, ridge height/direction, pitch — ridge direction drawn from the same reference-angle set as the walls, Section 3.1). `manifold` realizes an actual sloped mesh from these attributes only when a specific consumer needs one — never as part of the authoritative model.

Skylights are an authored instance record on the roof face (position, dimensions) — geometrically a hole in a sloped surface, kept out of the boolean solid the same way windows are.

### 4.5 Shading, Eaves & Aesthetic Detail — Three Tiers, Kept Structurally Separate

- **Zone-generating:** the constant-cross-section prisms (Section 3) that produce thermal zones, daylight zones, and floor plates. Nothing in the other tiers ever enters this one.
- **Shading-relevant, non-zone geometry:** fins, eaves, and overhangs that can genuinely cast shade or block wind/rain on a real surface — either a rule-engine instruction (Section 4.3, for systematic cases) or an authored instance tied to a specific wall/roof edge (for a particular physical element) — feeding WUFI/THERM/solar-exposure/daylight/resilience consumers (Section 6), never forming a thermal zone. The test for this tier: could it ever block sun, wind, or rain from a real surface?
- **Pure aesthetic:** genuinely decorative detail (cornices, cosmetic massing) with no shading or exposure consequence — kept in a separate data structure so it cannot leak into a zone or a shading calculation by accident. Real value for the pre-planning pack's credibility, but Phase 3+/optional.

For the `remedial` stage, capturing existing shading (tier two) is a **mandatory** checklist step (photograph each facade, note any projecting element with rough dimensions) rather than an opportunistic mention.

## 5. Fidelity Boundary

Where the downstream workflow is comparative (proposed vs. a reference building, as in JV3-methodology runs), a geometric simplification that affects both sides symmetrically has negligible effect on the outcome delta; a simplification changing topology, boundary conditions, or the facade actually carrying the compliance/design argument does not cancel and must be exact. **This cancellation logic does not extend to absolute-metric runs** (heatwave, design-day, free-running overheating checks) — there, geometry fidelity (shading especially) directly affects the result and must be treated as first-order.

**First-order (always exact):** adjacency and boundary condition type; orientation of exterior surfaces; area/boundary accuracy of any facade carrying the compliance or design argument; any tier-two shading element once captured. **Second-order (safe to abstract):** reveal depth; incidental fin/shading geometry nobody specifically raised or photographed; minor setbacks and sub-massing articulation; all tier-three aesthetic detail. **Promotion rule:** any shading device, skylight, or similar element captured through the AI-assisted briefing session (or the mandatory remedial shading checklist) is automatically first-order for that element, regardless of how minor.

## 6. Downstream Layer (out of scope for this brief)

The geometry engine's output — zone/surface geometry, tags, matched rules, orientation, area, boundary conditions, tier-two shading — feeds a separate, more substantial body of domain logic, developed independently:

|Consumer|What it needs from the geometry engine|
|---|---|
|JV3-equivalent thermal simulation|Zone/surface geometry, boundary conditions, orientation, and matched construction/glazing rules (Section 4.3). Reference-building generation and NCC schedule logic are downstream and roughly as substantial as the geometry engine itself — worth keeping close rather than delegating in a build handoff.|
|Daylight assessment|Same window geometry (realized from rule matches), plus tier-two shading — for Radiance or an equivalent daylight engine.|
|WUFI hygrothermal screening|Facade area, orientation, and (if coupled) interior zone conditions as a boundary input. Assembly material stack-up is downstream, not geometric.|
|THERM section analysis|A vertical 2D cross-section at a nominated junction — the same kernel, a cutting plane rotated 90° from the horizontal floor-level cuts.|
|Carbon-accounting takeoffs|Area by construction type and orientation — close to a free byproduct of the matched construction rules.|
|Resilience advisory (hail, wind, water, dust, smoke)|Orientation, relative exposure, and tier-two shading by facade. The advice itself is a director-curated judgement table, not a computed output.|

## 7. Use Cases & Reporting

Every project declares a **stage** — `pre_planning` or `remedial` — governing the shading-checklist requirement (Section 4.5) and the report template:

- **Pre-planning:** a 3–4 page bounding-advice pack — indicative facade performance guidance, explicitly framed as preliminary and subject to the client's eventual ESD consultant's formal assessment. This disclaimer covers narrative/judgement content (resilience advisory) as deliberately as it covers simulated figures.
- **Remedial:** a compliance-facing report referencing NCC methodology, held to the higher accuracy bar in Section 5, defensible to a building surveyor.

## 8. Development Phasing

Phase 1 constitutes the proof of concept: a short, self-contained build establishing whether the geometry-core architecture in Sections 2–4 can be delivered in weeks, not months.

- **Phase 1 — Geometry Core (PoC):** Site/Building/Footprint data model, `shapely`-based interval-membership floor-plate extraction with always-union, adjacency (including height-mismatch wall splitting), boolean union/difference on footprints, pre-flight validation.
- **Phase 2 — Authoring UI:** Typed-rectangle and PDF-trace-with-calibration entry, reference-angle definition and guided/snapped drawing (Section 3.1), plan-view authoring with docked live-3D and level-ghosting (Section 3.2), surface tagging and the declarative rule engine (Section 4.3), procedural window rendering from matched rules, roof-form metadata (via on-demand `manifold` realization), instance-based eave/skylight authoring, QA view. Sufficient to launch the pre-planning bounding-advice offering.
- **Phase 3 — AI Integration & Polish:** Text-brief and briefing-session parsing into rule-engine entries and authored instances, HVAC-relevant notes routed downstream, remedial shading checklist workflow, both report templates, optional tier-three aesthetic detail.
- **Downstream (parallel, separately scoped):** Reference-building generation and NCC schedule/construction logic, EnergyPlus execution (`geomeppy` — PyPI Alpha-status, revisit before production reliance), Radiance daylight export, WUFI/THERM/carbon exports, resilience advisory rule table.