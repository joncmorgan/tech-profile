# Building-Performance Physics Pipeline Research Summary

## Purpose

This conversation explored the current market for software platforms, simulation engines, interoperability tools, and workflow approaches used for **physics-based building-performance assessment**.

The underlying objective is to design a highly efficient, scalable pipeline that can transform varied architectural inputs—such as Revit models, IFC files, Rhino/Grasshopper models, SketchUp files, CAD drawings, PDFs, specifications, and other project documents—into robust analysis models for:

- Operational energy consumption
- Heating and cooling loads
- Envelope heat transfer
- Daylight and glare
- Solar exposure and shading
- Thermal comfort
- Natural ventilation
- Airflow and CFD
- Outdoor wind and microclimate
- Hygrothermal and condensation analysis
- Thermal bridges
- Embodied carbon and life-cycle assessment

A central business goal is to create a **human-in-the-loop data-production workflow** that can be performed partly by offshore teams, while preserving technical quality, traceability, repeatability, and senior engineering oversight.

---

## Core conclusion

The strongest opportunity is not to build another building-performance simulation engine, BIM viewer, or generic model-sharing platform.

The opportunity is to build an **analysis-model production and governance layer** that sits between messy project inputs and downstream simulation engines.

That layer should:

1. Accept and version diverse source materials.
2. Extract useful data automatically where possible.
3. Route ambiguity and model-cleanup work to trained human analysts.
4. Convert source information into a controlled canonical analysis model.
5. Apply standardized assumptions, libraries, and engineering templates.
6. Validate geometry, physics inputs, and simulation readiness.
7. Compile the canonical model into solver-specific formats.
8. Run or hand off simulations through specialized analysis platforms.
9. Normalize results into consistent reporting formats.
10. Preserve traceability from each result back to its source files and assumptions.

The preferred architecture is:

\[
\text{Source evidence}
\rightarrow
\text{Canonical analysis model}
\rightarrow
\text{Solver-specific model}
\rightarrow
\text{Simulation results}
\rightarrow
\text{QA, reporting, and audit trail}
\]

---

# 1. Market landscape

The market can be understood in five layers.

| Layer | Purpose | Representative platforms and tools | Main value | Main limitation |
|---|---|---|---|---|
| Design-data hubs | Store, exchange, version, review, and share project models | Speckle, Autodesk Docs, Autodesk Construction Cloud, Trimble Connect, Dalux, BIMcollab | Model sharing, version history, collaboration, review | Do not automatically create valid building-physics models |
| Interoperability and object-model frameworks | Normalize and translate engineering data between software systems | Speckle, BHoM, IFC, IfcOpenShell, Hypar, custom APIs and JSON schemas | Data movement, automation, open workflows, cross-disciplinary interoperability | Require deliberate mapping, validation, and governance |
| Analysis authoring and conversion tools | Create simulation models from BIM/CAD geometry | Pollination, Honeybee, DesignBuilder, IES VE, Sefaira, Autodesk Insight, cove.tool | Faster conversion from design models to analysis workflows | Imported models still need human checking and repair |
| Physics engines | Perform scientific calculations | EnergyPlus, OpenStudio, Radiance, OpenFOAM, IES Apache, ESP-r, TRNSYS, WUFI, THERM, WINDOW | Detailed and credible domain-specific calculations | Do not provide a full human workflow or reliable intake process |
| Orchestration and reporting | Manage batches, scenarios, QA, results, and decision reporting | OpenStudio SDK, Pollination cloud, custom Python systems, IES APIs, dashboards | Repeatability, automation, scalable simulation delivery | Requires a strong internal data model and validation framework |

---

# 2. Key platform findings

## Speckle

Speckle is highly relevant as a **design-data exchange, model review, versioning, and collaboration platform**.

It can exchange data across common AEC environments, including:

- Revit
- Rhino
- Grasshopper
- Archicad
- AutoCAD
- IFC workflows
- Custom web applications
- Data analytics environments

Speckle can preserve and exchange:

- Geometry
- Metadata
- Element relationships
- Object properties
- Quantities
- Model versions
- Revision history

### Best role in the proposed pipeline

Speckle should be treated as a potential:

- Source-model intake layer
- Version-control layer for design data
- Browser-based review environment
- Issue and QA context layer
- Collaboration interface between clients, offshore analysts, engineers, and reviewers
- Way to connect Revit/Rhino/IFC data into internal automation tools

### What Speckle should not be treated as

Speckle should not automatically be treated as the authoritative physics model.

A building-performance model needs information that is often missing, incomplete, ambiguous, or unsuitable in architectural BIM:

- Thermal zones
- Surface adjacencies
- Air boundaries
- Construction build-ups
- Material thermal properties
- HVAC systems
- Plant systems
- Controls
- Occupancy schedules
- Internal gains
- Infiltration
- Ventilation
- Thermal bridging assumptions
- Operable-window logic
- Shading controls
- Simulation weather files
- Analysis scenarios

Speckle is therefore best used as a flexible transport, collaboration, and provenance layer rather than as the sole physics-authoring environment.

---

## BHoM

BHoM, or the Building and Habitats object Model, is an engineering-focused interoperability framework.

It is relevant because it aims to provide a shared object model and adapter ecosystem across engineering disciplines.

Potential applications include:

- Structural engineering workflows
- Environmental engineering workflows
- Geometry and model exchange
- Analysis-data interoperability
- Automation
- Multi-disciplinary computational design
- EnergyPlus interoperability

BHoM has an EnergyPlus Toolkit that supports the creation of EnergyPlus IDF models.

### Strategic relevance

BHoM may be useful where a more formal engineering object model is desired.

A practical distinction is:

| Tool or approach | Best use |
|---|---|
| Speckle | Cloud collaboration, source-model exchange, web review, versions, design-data streams |
| BHoM | Engineering object models, specialist adapters, computational workflows |
| Internal canonical schema | Long-term stable data contract between offshore production, QA, simulation engines, reporting, and clients |

A mature system could use Speckle for exchange and collaboration while using BHoM or an internal model as the engineering normalization layer.

---

## IFC and IfcOpenShell

IFC is essential for vendor-neutral BIM exchange, but IFC should be treated as a **source format**, not an automatically valid simulation input.

IFC may contain:

- Building geometry
- Building hierarchy
- Storeys
- Walls
- Floors
- Roofs
- Windows
- Doors
- Spaces
- Quantities
- Object properties
- Materials
- Construction information
- Space boundaries

However, IFC files frequently have issues relevant to analysis:

- Missing or poorly defined spaces
- Incorrect second-level space boundaries
- Inconsistent coordinates
- Duplicated geometry
- Missing materials
- Missing thermal properties
- Incomplete adjacencies
- Incorrect classification of elements
- Ambiguous shading geometry
- Architectural objects that do not represent thermal boundaries
- Excessive model detail that is unsuitable for simulation

### Key lesson

“IFC-compatible” does not mean “analysis-ready.”

IFC should be ingested, checked, and transformed through controlled rules before being used for energy modelling, daylight analysis, CFD, or hygrothermal assessment.

---

## Hypar

Hypar is a cloud-based, code-first building-design platform focused on publishing and running building design logic.

It is relevant for:

- Generative design
- Configurable building systems
- Space planning
- Parametric workflows
- Revit integration
- JSON-based data exchange
- Repeatable design logic

Hypar is potentially valuable if the longer-term vision includes generating or standardizing building designs that are inherently analysis-ready.

It is less naturally suited than Speckle to serving as the primary intake and QA platform for arbitrary, messy client BIM, CAD, and PDF files.

---

# 3. EnergyPlus ecosystem

## EnergyPlus

EnergyPlus is one of the most important whole-building simulation engines in the market.

It is used for:

- Whole-building energy simulation
- Heating and cooling loads
- HVAC system modelling
- Plant modelling
- Controls
- Water use
- Internal gains
- Envelope heat transfer
- Solar gains
- Thermal comfort workflows
- Airflow Network workflows
- Scenario analysis
- Parametric studies
- Operational-energy modelling

### Why it matters

EnergyPlus is especially strong as a foundation for a scalable internal platform because it is:

- Widely adopted
- Open and scriptable
- Suitable for batch processing
- Supported by a large ecosystem
- Well suited to custom automation
- Compatible with many commercial and open-source front ends
- Suitable for both simplified and detailed simulation workflows

### Limitation

EnergyPlus itself is not a user-friendly source-data intake system.

Native EnergyPlus formats such as IDF and epJSON are powerful but require strong model-authoring discipline.

A scalable delivery model therefore requires:

- Standardized libraries
- Construction templates
- HVAC archetypes
- Schedule libraries
- QA checks
- Geometry-validation rules
- Model-generation scripts
- Simulation templates
- Results normalization
- Senior review

---

## OpenStudio

OpenStudio is arguably the most important technical layer above EnergyPlus for a custom data pipeline.

It is a cross-platform toolkit and SDK supporting:

- Whole-building energy modelling using EnergyPlus
- Advanced daylight workflows using Radiance
- Model transformation
- Simulation workflow automation
- Parametric analysis
- Reporting
- OpenStudio Measures
- API-driven workflow generation

### Why OpenStudio is strategically important

OpenStudio can act as a compiler and orchestration layer between an internal canonical analysis model and an EnergyPlus simulation.

A recommended data path is:

\[
\text{Canonical analysis model}
\rightarrow
\text{OpenStudio model}
\rightarrow
\text{EnergyPlus IDF or epJSON}
\rightarrow
\text{Simulation}
\rightarrow
\text{Standardized results}
\]

### OpenStudio Measures

OpenStudio Measures can encode reusable modelling and transformation rules.

Potential internal Measures include:

- Assigning constructions based on element type and climate zone
- Mapping space types to occupancy schedules
- Mapping building uses to internal loads
- Applying infiltration assumptions
- Assigning ventilation rates
- Applying heating and cooling setpoints
- Creating HVAC archetypes
- Creating code-compliance baseline variants
- Running pre-simulation QA checks
- Creating scenario variants
- Exporting standardized output variables
- Generating model reports and warnings

### Recommended role

OpenStudio should be strongly considered as the primary internal energy-modelling and orchestration layer for a vendor-independent, scalable workflow.

---

# 4. Pollination and Ladybug Tools

## Ladybug Tools

Ladybug Tools is the leading open parametric environmental-analysis ecosystem for Rhino and Grasshopper.

The ecosystem includes workflows for:

- Climate analysis
- Solar analysis
- Daylight
- Glare
- Energy modelling
- Thermal comfort
- Outdoor comfort
- Sunlight hours
- Radiation
- Natural ventilation
- Parametric design studies

## Honeybee

Honeybee is a key part of Ladybug Tools and connects Rhino/Grasshopper geometry to simulation engines such as:

- EnergyPlus
- OpenStudio
- Radiance
- Daysim
- Other environmental simulation workflows

## Pollination

Pollination is the cloud-based collaboration, simulation, automation, and results layer associated with Ladybug Tools.

It is relevant because it supports:

- Model editing
- Simulation execution
- Results review
- Automation
- Web-based workflows
- Revit integration
- Rhino/Grasshopper integration
- Energy modelling
- Daylight analysis
- Radiance workflows
- OpenStudio/EnergyPlus workflows
- URBANopt workflows
- Potential CFD-related workflows

### Strategic value

Pollination is one of the strongest market options where the workflow includes:

- Rhino
- Grasshopper
- Parametric façades
- Solar studies
- Daylight studies
- Environmental design
- Revit-to-energy workflows
- Cloud-based analysis management
- Cross-disciplinary performance modelling

It is particularly useful for high-performance design teams that already use Rhino/Grasshopper.

### Limitation

Pollination does not eliminate the need for:

- Input-data standards
- Model validation
- Construction mapping
- Assumption management
- Quality assurance
- Human interpretation
- Technical review

It should be evaluated as either:

- A commercial platform to use directly, or
- An execution environment and analyst tool within a broader internal pipeline.

---

# 5. Commercial energy-modelling platforms

## DesignBuilder

DesignBuilder is a mature commercial application built around EnergyPlus.

It supports import and interoperability through:

- gbXML
- IDF
- Revit workflows
- Grasshopper workflows
- Archicad workflows
- MicroStation workflows
- Other gbXML-capable BIM systems

It is useful for:

- Whole-building energy modelling
- HVAC and plant modelling
- Heating and cooling loads
- Thermal comfort
- Natural ventilation
- Daylight workflows
- EnergyPlus simulation
- Model visualization
- Analyst-driven geometry cleanup
- Professional reporting

### Best role

DesignBuilder is a strong option for an offshore or distributed analyst team because it provides a visual, analyst-friendly interface for converting and cleaning models before EnergyPlus simulation.

### Limitation

It is primarily an application-centered workflow.

It can be highly productive, but it is less suitable than an OpenStudio-based architecture if the goal is a deeply customized, API-first, solver-neutral production platform.

---

## IES VE

IES VE is one of the most mature and capable integrated building-performance simulation suites.

It supports multi-domain analysis including:

- Dynamic thermal simulation
- Energy use
- Heating and cooling loads
- Daylight
- Solar
- Thermal comfort
- Airflow
- Natural ventilation
- Carbon
- Operational performance
- Compliance-related workflows

It has long-standing integration pathways from Revit, including plug-ins and gbXML workflows.

### Best role

IES VE is especially suitable for:

- High-end engineering consultancy
- Detailed performance simulation
- Complex multidisciplinary analysis
- Senior analyst workflows
- Detailed technical deliverables
- Projects requiring formal quality assurance
- Detailed compliance or rating work
- Centralized analyst teams working from validated input models

### Important insight

IES VE’s ongoing work on Revit synchronization highlights a broader industry reality:

- Geometry transfer is one problem.
- Physics semantics are another problem.

A model may transfer walls, floors, roofs, windows, voids, and plenums successfully while still lacking validated constructions, thermal properties, schedules, and system definitions.

### Limitation

IES VE is a proprietary ecosystem and should not become the sole long-term repository of your business’s analysis data.

Maintain an independent canonical analysis model and treat the IES VE file as a solver-specific derivative.

---

## Autodesk Insight and Revit Energy Analysis Model

Autodesk Insight is a Revit-integrated building-performance analysis product.

It supports workflows involving:

- Energy analysis
- Heating and cooling loads
- Revit Energy Analysis Model
- EnergyPlus
- DOE-2.2
- Conceptual design feedback
- Autodesk Forma integration

### Best role

Autodesk Insight is useful where:

- Client and design-team inputs are primarily Revit.
- Architects want direct feedback inside their familiar software.
- Early-stage analysis is the priority.
- Autodesk ecosystem alignment is acceptable.
- Fast, low-friction performance feedback is more important than complete customization.

### Limitation

Revit Energy Analysis Model and gbXML exports should be treated as useful starting points rather than trusted final physics models.

They still require checks for:

- Zoning
- Adjacencies
- Construction assignments
- Model simplification
- System assumptions
- Shading
- Infiltration
- Schedules
- Geometry errors

---

## Sefaira

Sefaira is a cloud-based early-stage building-performance platform integrated with:

- SketchUp
- Revit
- Web-based reporting workflows

It provides rapid feedback on:

- Energy use
- Carbon emissions
- HVAC performance
- Daylight
- Solar exposure
- Glazing
- Shading
- Façade options
- Building orientation
- Comfort-related design factors

It uses recognized analysis engines, including EnergyPlus and Radiance-related workflows.

### Best role

Sefaira is valuable for:

- Rapid architectural feedback
- Early-stage massing studies
- Concept design
- SketchUp-centric workflows
- Revit-centric early energy studies
- Client-facing performance dashboards
- Fast option comparison

### Limitation

Sefaira is not a complete universal data-ingestion, offshore-production, or multi-physics platform.

It is best treated as an early-stage analysis and design-feedback product rather than the core data-production infrastructure.

---

## cove.tool

cove.tool is a cloud-oriented building-performance platform aimed at architects and sustainability teams.

It supports workflows around:

- Energy analysis
- Early-stage design
- HVAC-load calculations
- Daylight
- Water
- Carbon
- Compliance
- gbXML exchange
- Exports or handoffs to other analysis environments

### Best role

cove.tool can be useful for:

- Rapid energy and carbon studies
- Early-stage design decision-making
- Standardized architectural workflows
- Compliance-oriented work
- Simplified, repeatable performance studies

### Limitation

It is not a substitute for a fully controlled multi-physics data pipeline with custom schemas, solver orchestration, and engineering governance.

---

# 6. Daylight, solar, airflow, CFD, and façade tools

## Radiance

Radiance is one of the core daylight and lighting simulation engines in the building-performance ecosystem.

It is often accessed through tools such as:

- Honeybee
- Pollination
- OpenStudio
- ClimateStudio
- Sefaira
- Specialist daylight workflows

It is particularly relevant for:

- Daylight autonomy
- Annual sunlight exposure
- Spatial daylight autonomy
- Glare
- Illuminance
- Solar penetration
- Façade design
- Shading design
- Visual comfort

---

## ClimateStudio

ClimateStudio is a Rhino-based environmental performance platform.

It is particularly strong for:

- Daylight
- Glare
- Electric-light analysis
- Solar analysis
- Visual comfort
- Façade analysis
- Standards-oriented daylight assessment
- Rhino-based high-performance design workflows

### Best role

ClimateStudio is valuable as a specialist downstream tool for daylight and façade performance.

It is not the preferred primary platform for a whole-building, multi-engine EnergyPlus pipeline, but it can form a strong dedicated daylight lane.

---

## Eddy3D

Eddy3D is a Rhino/Grasshopper-oriented simulation environment for airflow, wind, microclimate, radiation, heat, and moisture workflows.

It includes modules for:

- Outdoor wind simulation
- Mean radiant temperature
- Urban microclimate
- Indoor airflow
- Passive scalar transport
- Moisture
- Radiation
- EnergyPlus Airflow Network integration
- OpenFOAM workflows

### Best role

Eddy3D is especially relevant for:

- Façade engineering
- Outdoor comfort
- Pedestrian wind
- Urban microclimate
- Natural ventilation
- Passive design
- Coupled radiation and airflow studies
- Advanced Rhino/Grasshopper workflows

### Limitation

CFD requires considerably more geometric preparation and specialist judgment than typical energy modelling.

Important CFD preparation tasks include:

- Watertight geometry
- Surface simplification
- Context modelling
- Terrain setup
- Computational domain definition
- Mesh design
- Boundary conditions
- Turbulence model selection
- Convergence assessment
- Results interpretation

CFD should be treated as a specialized workflow lane with its own production templates and QA system.

---

## OpenFOAM

OpenFOAM is an open-source CFD engine used for:

- Wind
- Outdoor comfort
- Indoor airflow
- Ventilation
- Thermal plumes
- Smoke or contaminant transport
- Heat transfer
- Specialist coupled physics

### Recommended role

OpenFOAM is suitable as the computational engine for a dedicated CFD service line.

However, it requires stronger geometry control, computational resources, and specialist review than EnergyPlus or Radiance.

---

# 7. Input formats and their limitations

The central insight is:

> Data intake is not file conversion. It is a controlled reconstruction and interpretation process.

Different input types provide different levels of useful information.

| Input type | Information commonly available | Information commonly missing or unreliable | Recommended workflow |
|---|---|---|---|
| Revit RVT | Rooms, levels, walls, floors, roofs, windows, quantities, metadata, possible MEP data | Thermal zoning, construction validity, systems logic, schedules, thermal bridging, natural-ventilation assumptions | Prefer direct extraction via Revit connector/API or Revit Energy Analysis Model; retain RVT as source evidence |
| IFC | Geometry, hierarchy, elements, quantities, properties, sometimes spaces and materials | Reliable space boundaries, thermal properties, correct adjacencies, useful system information | Ingest and validate using IFC rules; use as vendor-neutral source evidence |
| gbXML | Spaces, surfaces, openings, adjacencies, analysis-oriented geometry when exported correctly | HVAC, schedules, thermal properties, shading, export errors, unreliable topology | Use as a fast path, but always apply QA before simulation |
| Rhino/Grasshopper | Parametric geometry, metadata, custom design logic | Space-use data, zoning, constructions, HVAC, operational schedules | Use controlled Honeybee/Pollination or Grasshopper recipes |
| SketchUp | Concept geometry and simple massing | Detailed thermal, construction, HVAC, schedule, and adjacency information | Use for early-stage Sefaira or concept studies |
| DWG/DXF | 2D geometry, layers, annotations, dimensions | Building semantics, zones, materials, systems, heights, adjacencies | Human tracing and simplified analysis-model reconstruction |
| PDF plans/specifications | Human-readable plans, sections, schedules, material information | Machine-readable geometry, reliable scale, complete systems logic | Use document extraction plus human verification |
| Scans/images/photos | Visual evidence | Dimensions, orientation, materials, building operation, system data | Manual reconstruction with explicit assumptions |

---

# 8. The recommended pipeline architecture

## Three-model approach

A robust system should maintain three different models.

### 1. Source model

The source model includes original project evidence:

- Revit files
- IFC files
- Rhino files
- SketchUp files
- CAD files
- PDFs
- Specifications
- Schedules
- Images
- Site information
- Equipment schedules
- MEP documentation
- Client clarifications

This layer should be immutable and version-controlled.

### 2. Canonical analysis model

The canonical analysis model is the internal normalized representation of building physics.

It should not depend entirely on:

- Revit
- Speckle
- IES VE
- DesignBuilder
- Honeybee
- EnergyPlus IDF
- Any single vendor

It should capture the building’s analysis-relevant structure, assumptions, and provenance.

### 3. Solver-specific model

This is a generated derivative created for a specific simulation platform.

Examples include:

- OpenStudio model
- EnergyPlus IDF
- EnergyPlus epJSON
- IES VE project
- DesignBuilder model
- Radiance scene
- Honeybee model
- OpenFOAM CFD case
- WUFI wall assembly
- THERM model
- WINDOW model
- LCA quantity package

The solver-specific model should never become the only authoritative model.

---

# 9. Canonical analysis schema

The canonical model should contain at least four information domains.

| Domain | Core entities and fields |
|---|---|
| Project context | Site, location, weather file, climate zone, orientation, terrain, nearby context, scenario, analysis period, relevant standard |
| Geometry and spatial structure | Building, storey, space, thermal zone, surfaces, windows, shading, adjacencies, coordinates, areas, volumes |
| Physics assumptions | Materials, layers, constructions, U-values, glazing properties, solar properties, infiltration, ventilation, schedules, loads, setpoints, HVAC archetypes |
| Governance and provenance | Source references, transformation rules, analyst assumptions, reviewer approvals, confidence ratings, issue history, versions, timestamps |

## Provenance requirement

Every important data point should record its origin.

Suggested categories:

- Imported directly from source.
- Derived by an automated transformation rule.
- Assigned from an approved library.
- Estimated by an analyst.
- Confirmed by the client or design team.
- Rejected or superseded.
- Pending clarification.

This will make the pipeline more defensible, scalable, and transparent.

---

# 10. Data-confidence tiers

A production system should classify projects according to the quality of available inputs.

| Tier | Typical source quality | Expected workflow |
|---|---|---|
| Tier A — Analysis-ready BIM | High-quality Revit or IFC with spaces, constructions, schedules, systems, and usable boundaries | Fast conversion, lower analyst time, detailed validation |
| Tier B — Usable design BIM | Good architectural Revit/IFC but incomplete building-physics data | Semi-automated extraction plus human zoning, construction, system, and schedule assignment |
| Tier C — Geometry evidence | Rhino, SketchUp, CAD, partial BIM, massing model | Human reconstruction of simplified analysis geometry and documented assumptions |
| Tier D — Documentary evidence | PDFs, scans, drawings, reports, photos, incomplete schedules | Manual reconstruction, explicit assumptions, uncertainty ranges, preliminary findings only |

This tiering system is essential when outsourcing work offshore.

It ensures that analysts are not simply rewarded for speed or model completion. They should be evaluated on:

- Correct classification of source quality
- Appropriate level of modelling effort
- Quality of assumptions
- Traceability
- QA performance
- Clear escalation of uncertainty

---

# 11. Offshore production model

The offshore workflow should be modular rather than assigning one person responsibility for all modelling.

Recommended roles include:

| Role | Responsibilities |
|---|---|
| Intake technician | Checks file completeness, file naming, versions, units, coordinates, missing information, and intake status |
| Geometry technician | Extracts, simplifies, repairs, or rebuilds analysis geometry; checks areas, volumes, enclosure, and adjacencies |
| Envelope technician | Maps walls, roofs, floors, glazing, and shading to approved construction libraries |
| Zoning and operations technician | Assigns zone use, occupancy, lighting, equipment, schedules, ventilation, and setpoints |
| Systems technician | Maps documented HVAC systems or applies approved system archetypes |
| QA technician | Runs automated and visual checks; identifies geometry, physics, or data issues |
| Senior analyst | Approves assumptions, exceptions, simulation approach, outputs, and client-facing interpretation |

## Important operating principle

Do not outsource the responsibility for engineering judgment.

Offshore teams can efficiently perform:

- Data extraction
- Geometry cleanup
- Model reconstruction
- Classification
- Template application
- Documentation
- QA preparation
- Simulation setup

Senior engineering staff should retain responsibility for:

- Analysis basis
- Assumption standards
- Exception handling
- Model approval
- Interpretation
- Technical sign-off
- Client recommendations

---

# 12. Required QA gates

Automation should not allow poor inputs to enter simulation without validation.

## Geometry QA

- Units, coordinates, orientation, and scale are plausible.
- Building location and weather file match.
- Thermal zones are enclosed.
- Zone volumes are positive.
- Surfaces have valid areas and orientations.
- No duplicated or zero-area surfaces exist.
- No self-intersecting geometry exists.
- Interior adjacencies are correctly paired.
- Exterior surfaces have valid boundary conditions.
- Window-to-wall ratios are plausible.
- Envelope area reconciles with source quantities.
- Gross floor area reconciles with source drawings or BIM quantities.

## Envelope and thermal QA

- Every heat-transfer surface has an assigned construction.
- Every construction has valid materials, layers, or approved equivalent thermal properties.
- Windows include U-value, solar heat-gain coefficient, visible transmittance, and frame assumptions where required.
- Thermal bridging is represented, approximated, or explicitly excluded.
- Infiltration assumptions have a stated method and units.
- Ventilation assumptions are traceable.
- Shading geometry and shading controls are documented.

## Operations QA

- Every zone has a building use classification.
- Every zone has occupancy assumptions.
- Lighting loads are assigned.
- Equipment loads are assigned.
- Schedules are assigned.
- Heating and cooling setpoints are assigned.
- Ventilation is assigned.
- HVAC systems are assigned or deliberately excluded.
- System assumptions match the intended analysis stage.

## Simulation QA

- EnergyPlus or other solver severe errors are treated as failures unless formally waived.
- Warnings are categorized and reviewed.
- Peak heating and cooling loads are plausible.
- Energy-use intensity is plausible.
- Monthly profiles are plausible.
- End-use breakdowns are reviewed.
- Unmet-hours results are reviewed.
- Zone temperatures are reviewed.
- Output confidence level is linked to source-data tier and assumption quality.

---

# 13. Separate analysis lanes

A common mistake is to force every physics problem through one model.

Instead, maintain a shared canonical model but create specialist solver-specific representations.

| Analysis lane | Recommended foundation | Typical tools | Important specialist inputs |
|---|---|---|---|
| Annual energy and HVAC | OpenStudio + EnergyPlus | DesignBuilder, IES VE, Pollination, Autodesk Insight | Zones, constructions, schedules, HVAC, infiltration, ventilation |
| Heating and cooling loads | EnergyPlus, IES VE, DesignBuilder | IES VE, DesignBuilder, Insight | Design days, setpoints, ventilation, envelope, internal gains |
| Daylight and glare | Radiance | Honeybee, Pollination, ClimateStudio, Sefaira | Apertures, glazing, shading, reflectances, context, sensor grids |
| Solar and façade studies | Radiance and solar engines | Honeybee, Pollination, ClimateStudio, Sefaira | Orientation, shading, façade geometry, materials, nearby context |
| Thermal comfort | EnergyPlus plus post-processing | IES VE, Honeybee, DesignBuilder | Air temperature, radiant temperature, air speed, clothing, activity |
| Natural ventilation | EnergyPlus Airflow Network or CFD | IES VE, Eddy3D, OpenFOAM | Openings, flow paths, wind data, discharge coefficients, control logic |
| Outdoor wind and microclimate | CFD | Eddy3D, OpenFOAM, specialist cloud CFD | Context geometry, terrain, mesh, weather, radiation, surface conditions |
| Hygrothermal and condensation | Hygrothermal solver | WUFI and specialist façade tools | Layer order, vapour properties, sorption, driving rain, climate, junction details |
| Thermal bridges | 2D or 3D thermal bridge solver | THERM, WINDOW, specialist façade tools | Junction geometry, conductivities, frames, spacers, boundary conditions |
| Embodied carbon | Quantity extraction plus LCA database | One Click LCA, EC3-like tools, in-house calculations | Material quantities, classification, EPD mapping, lifecycle scenario |

---

# 14. Recommended technology strategy

## What to buy or use

Use established market tools where they are already strong.

| Capability | Suggested tools to adopt | Reason |
|---|---|---|
| Source-model sharing and review | Speckle, Autodesk Docs, Autodesk Construction Cloud | Model access, versions, web review, collaboration |
| BIM and IFC extraction | Revit API, Speckle connectors, IfcOpenShell | Reliable source extraction and custom validation |
| Energy simulation | EnergyPlus and OpenStudio | Open, scriptable, scalable, ecosystem support |
| Parametric environmental analysis | Ladybug Tools, Honeybee, Pollination | Strong Rhino/Grasshopper and daylight/energy workflows |
| Detailed commercial analysis | IES VE and/or DesignBuilder | Mature analyst tools and professional simulation workflows |
| Early-stage architectural feedback | Sefaira, Autodesk Insight, cove.tool | Faster feedback inside architect-facing environments |
| CFD and microclimate | Eddy3D, OpenFOAM, selected cloud CFD platform | Specialist airflow and outdoor-comfort simulation |
| Reporting | Power BI, Metabase, custom web dashboard | Standardized result presentation and portfolio-level analytics |

## What to build internally

The defensible intellectual property is the workflow and data-governance layer.

Build:

- Intake portal
- Project register
- Source-version registry
- Canonical analysis schema
- Assumption library
- Construction library
- HVAC archetype library
- Space-use and schedule library
- Geometry-validation service
- Model QA engine
- Task-routing system
- Offshore production dashboard
- Issue management process
- Approval workflow
- OpenStudio/EnergyPlus model compiler
- Scenario engine
- Results-normalization engine
- Reporting templates
- Audit trail
- Confidence-scoring system
- Client-facing explanation of assumptions and limitations

---

# 15. Recommended first implementation

A first 90-day proof-of-concept should focus on a limited but commercially valuable scope.

## Initial target analyses

- Annual operational energy
- End-use energy breakdown
- Heating and cooling loads
- Peak demand
- Envelope heat transfer assumptions
- Solar exposure
- Simplified daylight screening
- Basic thermal comfort indicators

## Initial supported inputs

- Revit
- IFC
- gbXML
- Rhino/Grasshopper
- SketchUp
- DWG
- PDF plans
- Spreadsheet schedules

## Minimum viable workflow

1. Upload and register source files.
2. Automatically record metadata and version information.
3. Perform intake checklist and source-quality classification.
4. Create an analysis basis.
5. Build a canonical thermal model.
6. Apply approved constructions, schedules, loads, and HVAC templates.
7. Run automated QA.
8. Route exceptions to human reviewers.
9. Compile to OpenStudio/EnergyPlus.
10. Run simulations.
11. Normalize results.
12. Produce a report containing assumptions, warnings, confidence level, and traceability.

## Suggested first reporting outputs

- Gross floor area
- Envelope area
- Window-to-wall ratio
- Heating load
- Cooling load
- Annual energy use intensity
- Annual energy use
- Energy end-use breakdown
- Monthly energy profile
- Peak demand
- Zone temperature summary
- Unmet hours
- Solar exposure indicators
- Key assumptions
- Key uncertainties
- Input confidence tier
- QA status

---

# 16. Key risks and misconceptions

## Misconception: “IFC means interoperable”

IFC is a critical exchange format, but a valid IFC file may still be unusable for energy modelling or other physics simulations.

It may lack:

- Correct spaces
- Correct space boundaries
- Usable adjacencies
- Material thermal properties
- Construction build-ups
- Reliable openings
- Analysis zoning
- Operational information
- HVAC information

## Misconception: “gbXML means analysis-ready”

gbXML can accelerate workflows, especially from controlled Revit exports.

However, gbXML quality depends on:

- Revit analytical-model configuration
- Source geometry quality
- Space and room quality
- Boundary conditions
- Export settings
- Surface adjacencies
- Construction assignments
- Shading interpretation

It should always be checked before use.

## Misconception: “Automation removes analysts”

The more credible operating model is **human-guided automation**.

Machines should:

- Extract data
- Detect errors
- Apply templates
- Generate geometry
- Compile solver models
- Run simulations
- Compare outputs
- Generate reports
- Flag exceptions

Humans should:

- Interpret incomplete source information
- Resolve ambiguity
- Select assumptions
- Review quality
- Approve model basis
- Interpret results
- Communicate uncertainty
- Provide engineering judgment

---

# 17. Actionable strategic insights

## Build the data pipeline, not another solver

The core opportunity is an operating system for building-performance model production.

Existing tools already handle many pieces of the technical stack:

- EnergyPlus performs whole-building energy simulation.
- Radiance performs daylight and lighting simulation.
- OpenFOAM performs CFD.
- WUFI supports hygrothermal analysis.
- THERM supports thermal-bridge analysis.
- IES VE and DesignBuilder provide mature analyst environments.
- Pollination and Honeybee support parametric environmental workflows.
- Speckle supports design-data exchange and collaboration.

The missing piece is a controlled, scalable system that reliably connects input evidence to validated analysis models.

## Make provenance a first-class product feature

Every result should be traceable to:

- Original source files
- Source revision
- Transformation rules
- Analyst decisions
- Assumption libraries
- Solver version
- Weather file
- Simulation settings
- QA checks
- Reviewer approvals

This is essential for client confidence, repeatability, dispute avoidance, quality assurance, and technical credibility.

## Productize uncertainty

Do not hide uncertainty from messy input data.

Instead, communicate:

- Input-data confidence tier
- Missing information
- Assumptions made
- Parameters derived from templates
- Parameters verified by the client
- Sensitivity ranges
- Recommended next information requests

This can become a commercial advantage.

## Standardize analyst work packages

Offshore scaling becomes feasible when work is decomposed into repeatable roles:

- Intake
- Geometry
- Envelope
- Zoning
- Operations
- HVAC
- QA
- Senior review

This reduces training burden, improves quality control, and allows each role to become more efficient.

## Maintain separate solver lanes

Do not force all physics work through an annual EnergyPlus model.

Use the canonical model as a shared foundation, then create appropriate solver-specific derivatives for:

- Energy
- Daylight
- CFD
- Hygrothermal
- Thermal bridges
- Embodied carbon
- Façade performance

---

# Final recommendation

The recommended long-term architecture is:

1. Use **Speckle and/or Autodesk ecosystem tools** for source-data access, versioning, model review, and collaboration.
2. Create a vendor-neutral **canonical analysis model** as the internal source of truth.
3. Use **IfcOpenShell, Revit APIs, and custom extraction logic** to collect and validate source data.
4. Use a human-in-the-loop offshore production team to resolve ambiguity, rebuild analysis geometry, apply assumptions, and document decisions.
5. Use **OpenStudio and EnergyPlus** as the core open, scalable energy-modelling and simulation backbone.
6. Use **Pollination, Ladybug Tools, Honeybee, and Radiance** for parametric environmental, daylight, solar, and Rhino/Grasshopper workflows.
7. Use **IES VE and DesignBuilder** for detailed commercial simulation workflows and specialist analyst production.
8. Use **Eddy3D and OpenFOAM** for CFD, wind, natural ventilation, and microclimate workflows.
9. Use specialist tools such as **WUFI, THERM, and WINDOW** for façade condensation, thermal bridges, and detailed envelope physics.
10. Build internal intellectual property around orchestration, QA, assumption libraries, provenance, confidence ratings, standardized results, and workflow governance.

The commercially defensible proposition is not merely:

> “We can run simulations.”

It is:

> “We can take almost any design evidence, convert it into a validated analysis model through a transparent human-and-automation workflow, run appropriate physics engines, and deliver results with a clear record of evidence, assumptions, limitations, and confidence.”