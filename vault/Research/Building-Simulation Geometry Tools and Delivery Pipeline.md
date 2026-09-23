# Building-Simulation Geometry Tools and Delivery Pipeline

## Executive Summary

The objective is to establish an efficient production workflow in which architectural PDFs are converted by an offshore modelling team into simulation-ready analytical geometry. The returned model must then support NCC compliance, HVAC modelling, façade analysis and broader building-performance design workflows.

The preferred geometry paradigm is **2.5D**: levels, zone footprints, heights, openings, roofs and shading are defined using plan-based objects, from which analytical 3D surfaces are generated. Native 3D tools remain acceptable where they provide a practical simulation-geometry workflow. Open-source software is not a requirement; **reliable data interoperability is more important**.

The leading options are:

1. **Better Building** — best current hypothesis for a streamlined, Australian, straight-through PDF-to-model-to-NCC workflow.
2. **DesignBuilder** — strongest option for programmable access, editable model exchange, detailed HVAC and bidirectional automation.
3. **Rhino with Pollination/Ladybug Tools** — best exception pathway for complex geometry and custom scripted workflows.
4. **IESVE ModelIT** — strong integrated simulation environment when energy, daylight, loads and HVAC will remain within IESVE.
5. **HERO** — highly attractive for NatHERS residential modelling, but currently limited by the absence of a publicly documented geometry API or neutral geometry export.
6. **Pleiades Modeleur** — strong commercial 2.5D modeller with useful IFC-based exchange, but less aligned with Australian compliance.
7. **Dragonfly, Honeybee, OpenStudio and FloorSpaceJS** — better suited as internal schemas, translators, QA components or lightweight editors than as the default offshore production application.

The recommended strategy is not to select one monolithic application for every purpose. Instead:

- Use a constrained application such as **Better Building or DesignBuilder** for offshore model production.
- Require both the native file and one or more neutral or documented exchange files.
- Convert the returned model into a controlled canonical analytical model.
- Validate the geometry automatically.
- Add engineering and compliance data in a separate enrichment stage.
- Compile the validated model into façade, NCC, HVAC and simulation-specific outputs.

---

# Requirements

## Primary use case

The intended workflow is:

1. Receive architectural PDFs and related project documents.
2. Prepare a clear offshore modelling brief.
3. Send the drawing package to a trained model-production team.
4. Receive a simulation-ready geometry model.
5. Perform automated and human QA.
6. Add NCC, construction, glazing, schedule and HVAC data, either offshore under controlled rules or locally.
7. Generate proposed and reference simulation models.
8. Run the models through an automated analysis pipeline.
9. Reuse the geometric and semantic information in downstream façade-compliance and design workflows.

The main optimisation target is **total Australian technical effort per accepted model**, not merely offshore drawing speed.

## Software criteria

| Criterion | Priority |
|---|---:|
| Efficient modelling from PDFs or plan underlays | Critical |
| Constrained and trainable offshore workflow | Critical |
| Supported geometry extraction | Critical |
| Scriptable QA and transformation | Critical |
| Reliable zones, surfaces, openings and adjacencies | Critical |
| Australian NCC workflow support | High |
| Ability to add HVAC after geometry production | High |
| Stable model and object identifiers | High |
| Native or documented editable-model exchange | Medium–high |
| Bidirectional model automation | Medium |
| Handling of complex geometry | Medium |
| Open-source licensing | Low |

## Meaning of 2.5D

A 2.5D analytical building model normally contains:

- Planar zone footprints
- Storey or level elevations
- Floor-to-floor and ceiling heights
- Repeated storeys
- Openings hosted by walls
- Roof parameters
- Eaves, fins and shading objects
- Surface boundary conditions
- Adjacency relationships

The full three-dimensional thermal geometry is derived from these inputs. Dragonfly’s `Room2D`, for example, is based on a horizontal floor polygon and extrusion height, while URBANopt generates building forms by extruding footprints. [web:399][web:400][web:405]

This structure is generally preferable for outsourced production because it is easier to draw, check, revise and compare against architectural plans than unrestricted 3D surface modelling.

---

# Recommended Ranking

## Workflow-specific shortlist

| Rank | Program | Geometry model | Main exchange path | Best role |
|---:|---|---|---|---|
| 1 | **Better Building** | Native 2D/2.5D zones plus analytical 3D | IDF, epJSON and gbXML workflows | Australian straight-through production |
| 2 | **DesignBuilder** | Extruded blocks, partitions and thermal zones | dsbXML, gbXML, IDF and API | Programmable, editable and bidirectional production |
| 3 | **Rhino + Pollination** | Flexible 3D with analytical conversion | HBJSON, gbXML, GEM, OSM and IDF | Complex geometry and custom automation |
| 4 | **IESVE ModelIT** | Extruded rooms plus general 3D primitives | GEM, gbXML and DXF | Integrated multidisciplinary simulation |
| 5 | **HERO** | Strong residential 2.5D model | No public geometry exchange identified | NatHERS residential production |
| 6 | **Pleiades Modeleur** | Storey-based 2D modelling with derived 3D | IFC and gbXML-oriented workflows | Commercial 2.5D alternative |
| 7 | **IDA ICE** | Native plan and detailed 3D zones | IFC and automation interfaces | Detailed energy, comfort and plant modelling |
| 8 | **OpenStudio/FloorSpaceJS** | Browser-based 2D floor-space geometry | OSM, IDF and gbXML | OpenStudio editing and internal tooling |
| 9 | **Dragonfly/Honeybee** | Native 2.5D and detailed analytical 3D schemas | DFJSON and HBJSON | Canonical data and conversion layer |
| 10 | **ESP-r** | Native polygonal and extruded geometry | Open project formats | Specialist multidomain simulation |

This ranking is specific to the proposed operational workflow. It is not a general ranking of simulation accuracy or total application capability.

---

# Primary Programs

## Better Building

Better Building is the leading candidate for an initial pilot because it aligns closely with Australian energy and NCC workflows while providing an EnergyPlus-based downstream path.

Its geometry environment supports plan-based zone creation, levels, windows, shading masses, pitched roofs and analytical boundary conditions. The 3D Building Geometry Creator can use image, DXF and SVG inputs and export EnergyPlus epJSON containing zones, openings, constructions, shading and boundary conditions. [web:701][web:725]

Relevant strengths include:

- Relatively constrained geometry workflow
- Australian residential and commercial compliance orientation
- EnergyPlus simulation
- IDF and epJSON data paths
- gbXML workflows
- Simplified EnergyPlus HVAC templates
- More advanced HVAC capabilities where required
- Active product development and recent NCC documentation [web:700][web:709][web:727][web:731]

The principal limitation is that the public interoperability boundary appears to be mainly the **compiled EnergyPlus model**, rather than an exposed native 2D authoring schema or comprehensive geometry API.

Consequences include:

- Forward extraction into the pipeline should be practical.
- Recovering zone footprints from ordinary IDF or epJSON geometry should be manageable.
- Stable links back to original drawing objects may require external identifiers and sidecar data.
- Programmatically modifying the native 2D authoring model may be difficult.
- Round-trip workflows require testing.

Better Building is therefore strongest when the model moves primarily forward:

    Better Building geometry
        → IDF or epJSON
        → automated QA and normalisation
        → NCC and HVAC enrichment
        → simulations
        → façade outputs

### Better Building verdict

**Preferred initial candidate for Australian straight-through model production**, subject to a representative export-fidelity test.

---

## DesignBuilder

DesignBuilder is the strongest option where programmability, editable-model handoff and bidirectional workflows matter more than having the simplest offshore interface.

Its geometry model is based on blocks that are extruded from plan polygons and divided into zones through partitions. DesignBuilder can import PDF, DXF and raster underlays, use different plans at different storeys and regenerate zone surfaces and adjacencies as geometry changes. [web:548][web:550][web:553]

Its main advantage is developer-facing interoperability:

- Documented `dsbXML` model format
- Published object hierarchy and geometry definitions
- Model import and export through XML
- Python and C# scripting
- Plug-in interfaces
- Direct geometry access through the API
- IDF and gbXML exchange
- Programmatic model generation [web:691][web:692][web:694][web:697]

DesignBuilder can expose geometry closer to the editable authoring model, reducing the need to reconstruct 2.5D topology from EnergyPlus surface objects.

Its disadvantages are:

- Heavier user interface
- Greater training burden
- More modelling options that must be constrained in the offshore brief
- Potentially higher licensing and workstation-management overhead
- Risk that operators create valid but inconsistent models unless templates are tightly controlled

### DesignBuilder verdict

**Best long-term platform if model automation, revisions, native-model regeneration, detailed HVAC or bidirectional editing become central.**

---

## Better Building versus DesignBuilder

| Issue | Better Building | DesignBuilder |
|---|---|---|
| Offshore learning curve | Likely lower | Likely higher |
| Australian NCC alignment | Strong | Capable but more general |
| Plan-based modelling | Strong | Strong |
| Direct PDF handling | May require prepared image inputs in some workflows | Direct PDF and DXF support |
| IDF/epJSON handoff | Strong | Strong IDF handoff |
| Native editable exchange | Not publicly documented to the same extent | Strong through dsbXML |
| Geometry API | No comparable public API identified | Documented API |
| Python/C# automation | Primarily external file processing | Native scripting and plug-ins |
| Detailed HVAC | Available | Mature and extensive |
| One-way production pipeline | Very good fit | Good fit |
| Bidirectional integration | Requires testing | Better fit |
| Recommended position | First pilot | Benchmark and likely fallback |

Better Building should rank first if:

- Offshore modelling speed dominates.
- Australian compliance dominates.
- The model generally moves forward rather than returning to the authoring tool.
- IDF or epJSON contains sufficient geometry and metadata.
- Native authoring-object IDs are not essential.

DesignBuilder should rank first if:

- Models will undergo repeated revisions.
- Scripts must update editable models.
- Native model generation is required.
- Detailed HVAC will be built within the same environment.
- Complex geometry is common.
- A documented application-level API is valuable.

---

## HERO

HERO is a strong 2.5D residential modeller designed for Australian NatHERS assessments. It should remain on the shortlist even though its data access is less mature than Better Building or DesignBuilder.

Its analytical structure includes:

- Projects and multiple dwellings
- Levels
- Thermal zones
- Walls
- Separate floors and ceilings
- Windows, doors and permanent openings
- Eaves and shading objects
- Roof spaces and subfloor spaces
- Automatically generated or split surfaces
- Cross-level relationships [web:594][web:597][web:604][web:605][web:650][web:653]

This is close to an ideal residential 2.5D geometry schema. HERO is also accredited for NatHERS use and can model and simulate without a conventional software subscription, with costs associated principally with certification and related services. [web:577][web:618]

The primary issue is interoperability:

- No publicly documented geometry API was identified.
- No documented neutral geometry export was identified.
- Documented exports focus more strongly on simulation results.
- The project format may be proprietary.
- Reverse-engineering could create legal, maintenance and accreditation risks. [web:613][web:616]

A read-only extrusion or viewer would probably be technically straightforward if zone polygons, levels, heights, walls and openings could be accessed. The difficulty is obtaining the data through a stable and supported interface.

### HERO go/no-go investigation

Run a bounded technical spike:

1. Create a one-zone test project.
2. Create a two-zone adjacent project.
3. Create a two-level project.
4. Add windows, doors, eaves and a roofspace.
5. Save variants after changing one coordinate at a time.
6. Identify whether the project file is JSON, XML, SQLite, an archive, protobuf or opaque binary.
7. Determine whether objects use persistent IDs.
8. Ask HERO for a supported geometry export, SDK or read-only API.
9. Stop if extracting geometry would require sustained binary reverse-engineering.

### HERO verdict

**High-potential NatHERS production tool, but not suitable as the universal upstream model until supported geometry extraction is established.**

---

## Rhino and Pollination

Rhino is acceptable because its general geometry engine is powerful and highly scriptable, while Pollination and Ladybug Tools add analytical building semantics.

Relevant exchange paths include:

- HBJSON
- gbXML
- EnergyPlus/OpenStudio workflows
- IESVE GEM
- RhinoCommon and Grasshopper automation
- Python and C# scripting [web:445][web:449][web:667][web:684]

Rhino is particularly valuable for:

- Curved façades
- Irregular roofs
- Stepped sections
- Atria and complex voids
- Geometry repair
- Custom façade segmentation
- Parametric alternatives
- Visual QA

Its weakness for high-volume offshore work is excessive modelling freedom. Without strict templates, layers, naming conventions, analytical conversion rules and validation, operators can construct visually similar buildings using incompatible modelling methods.

### Rhino verdict

**Use as the controlled exception lane for difficult geometry and custom façade workflows, rather than necessarily as the default production editor.**

---

## IESVE ModelIT

IESVE ModelIT provides native simulation geometry using extruded rooms and additional three-dimensional primitives. It supports integrated workflows for thermal simulation, solar analysis, daylight, loads and HVAC.

Its native GEM format transfers geometry and site information between VE models, while gbXML and DXF pathways are also available. [web:540][web:661][web:662]

Pollination can export GEM from Rhino and Revit, providing an additional route into IESVE for difficult geometry. [web:667]

IESVE is most compelling where downstream analysis will remain in the IES ecosystem. If geometry is only an upstream commodity that will feed custom façade and EnergyPlus services, its breadth may add unnecessary licensing and training complexity.

### IESVE verdict

**Strong integrated environment when multidisciplinary IES analysis is required; probably not the simplest default offshore geometry workstation.**

---

## Pleiades Modeleur

Pleiades provides one of the clearest commercial examples of 2.5D simulation authoring. Users draw buildings storey by storey over image or DWG backgrounds, while the system derives 3D geometry, thermal zones and environmental context. [web:509][web:511]

Its IFC export can include:

- Rooms
- Walls
- Floors
- Roofs
- Windows and doors
- Construction names
- Material layers
- Thermal and regulatory classifications [web:688]

This makes targeted extraction with IfcOpenShell viable. The principal weakness is that Pleiades is more strongly aligned with French and European practice than Australian NCC workflows.

### Pleiades verdict

**Good 2.5D commercial benchmark and viable IFC-based alternative, but not the leading Australian production choice.**

---

## IDA ICE

IDA ICE supports plan-based and detailed three-dimensional thermal-zone modelling, CAD and IFC inputs, non-prismatic zones, plant systems and detailed comfort simulation.

It also has external automation capabilities, although licensing and API access conditions need confirmation for production use. [web:299][web:535][web:696]

### IDA ICE verdict

**Technically strong, particularly for detailed comfort and plant modelling, but likely more complex than required for the initial PDF-to-model production stage.**

---

# Open and Component-Based Tools

## Dragonfly

Dragonfly provides the strongest conceptual canonical 2.5D geometry model.

Its `Room2D` and building schemas support:

- Horizontal polygons
- Holes
- Levels and storeys
- Floor-to-ceiling heights
- Repeated storeys
- Roof specifications
- Window parameters
- Core and perimeter zoning
- Conversion to Honeybee analytical rooms [web:399][web:400][web:404]

Dragonfly’s common visual interface is Grasshopper, but its underlying Python libraries can be used independently.

**Recommended use:** canonical 2.5D schema, normalisation layer or inspiration for a custom internal schema.

---

## Honeybee

Honeybee provides detailed analytical 3D rooms consisting of planar faces with subordinate apertures and doors. It connects to EnergyPlus/OpenStudio for energy analysis and Radiance for daylight and solar analysis. [web:440][web:445]

Honeybee is better suited than Dragonfly to:

- Sloping floors
- Non-repeating storeys
- Stepped buildings
- Complex roofs
- Atria
- Unusual space volumes
- Detailed shading and daylight models

**Recommended use:** explicit 3D fallback for parts of a building that cannot be represented safely as 2.5D.

---

## FloorSpaceJS and OpenStudio

FloorSpaceJS is a browser-based widget specifically designed to create two-dimensional geometry for building-energy models. It is used by OpenStudio Application and can translate floor-space geometry into OpenStudio models. [web:470][web:495]

OpenStudio Application includes geometry, envelope, schedules, loads and HVAC functions around the OpenStudio/EnergyPlus ecosystem. [web:493][web:494]

**Recommended use:** lightweight internal editor, QA interface, geometry correction tool or OpenStudio model-processing workstation.

---

## URBANopt

URBANopt uses GeoJSON building footprints, heights and attributes to generate analytical building geometry. It can extrude footprints, create core/perimeter zones and include neighbouring-building shading. [web:405][web:408][web:413]

**Recommended use:** precincts, campuses, building portfolios and urban-scale work rather than detailed single-building production.

---

## ESP-r

ESP-r is a native open simulation environment integrating thermal, airflow, moisture, lighting, electrical and systems analysis. Its geometry methods include rectangles, polygonal plans, plan extrusion, tracing and CAD-related inputs. [web:559][web:561][web:572]

**Recommended use:** specialist research and multidomain simulation, rather than the primary offshore production interface.

---

# Other Programs Considered

| Program | Main characteristic | Relevance |
|---|---|---|
| **BEopt** | Residential level-by-level drawing with generated 3D and roofs | Useful interaction benchmark; residentially specialised [web:420][web:426] |
| **eQUEST** | Wizard-based shell and zoning creation for DOE-2 | Fast historical precedent; legacy workflow [web:375] |
| **Simergy** | EnergyPlus interface with internal and imported geometry | Current maintenance should be verified [web:475][web:478] |
| **CYPE Open BIM Analytical Model** | Derives analytical geometry from IFC | Useful IFC translation layer, not primarily PDF-first [web:435][web:437] |
| **BSim** | Native plan, section and 3D simulation model editing | Capable but geographically specialised [web:520][web:521] |
| **Cove drawing.tool** | Cloud geometry creation and performance analysis | Useful modern UX reference; proprietary cloud dependency [web:488][web:489] |
| **Sketchbox** | Simplified early-stage energy modelling | Suitable for rapid measures analysis, not broad interchange [web:468] |
| **Energy3D** | Integrated conceptual CAD and environmental feedback | Educational and early-design reference [web:501] |
| **BAGEL** | Blender-based geometry for Modelica-oriented urban modelling | Research and specialist Modelica workflows |

---

# Host-Dependent Tools

| Tool | Host | Simulation pathway | Assessment |
|---|---|---|---|
| Honeybee/Dragonfly | Rhino/Grasshopper | EnergyPlus, OpenStudio and Radiance | Excellent analytical workflow under strict governance |
| Pollination | Rhino/Revit | HBJSON, gbXML and GEM | Valuable interoperability and validation layer |
| TRNSYS3D | SketchUp | TRNSYS Type 56 | Useful where TRNSYS is already selected [web:383][web:384] |
| TRNLizard | Rhino/Grasshopper | TRNSYS | Parametric but commercially dependent [web:392] |
| Sefaira | SketchUp/Revit | Sefaira analysis | Early-design tool dependent on host geometry [web:485][web:491] |

These tools are valid specialist choices but are weaker as default offshore production systems because model correctness depends on both the host modeller and the simulation extension.

---

# Data Architecture

## Separate model layers

The pipeline should maintain four explicit data layers:

| Layer | Contents |
|---|---|
| **Source layer** | PDFs, drawings, revisions, dimensions, schedules and extracted text |
| **Geometry layer** | Buildings, levels, zones, surfaces, openings, roofs, shading and adjacencies |
| **Engineering layer** | Constructions, glazing, schedules, loads, infiltration and HVAC |
| **Compliance layer** | NCC pathways, proposed/reference transformations, assumptions and reporting data |

This separation avoids unnecessary geometry rework when an engineering or compliance assumption changes.

## Canonical model

The canonical model should be deliberately smaller than IFC, gbXML or a complete EnergyPlus model. A suitable conceptual structure is:

    Project
      Buildings
        Levels
          elevation
          height
          Spaces
            stable ID
            footprint
            holes
            usage
            conditioned status
            walls
            floors
            ceilings
            openings
            adjacency
            source references
          Shading objects
          Roof specifications

Use:

- A Dragonfly-like 2.5D structure for ordinary spaces.
- Honeybee-style explicit faces for exceptional 3D geometry.
- Sidecar records for provenance and assumptions.
- Engine-specific exporters as compilation targets.

## Format roles

| Format | Recommended purpose |
|---|---|
| **Native application file** | Continued editing in the authoring application |
| **dsbXML** | DesignBuilder editable-model exchange |
| **epJSON** | Structured EnergyPlus model exchange |
| **IDF** | EnergyPlus compatibility and established workflows |
| **OSM** | OpenStudio model processing |
| **DFJSON** | 2.5D analytical geometry |
| **HBJSON** | Detailed 3D analytical geometry |
| **IFC** | BIM and element-oriented exchange |
| **gbXML** | Broad legacy BEM exchange, with strict validation |
| **GEM** | IESVE geometry transfer |
| **glTF/GLB** | Browser-based visual inspection |
| **SVG** | Floor-plan review and marked-up QA |
| **JSON/CSV sidecars** | Provenance, assumptions, mappings and QA results |

Neither IFC nor gbXML should automatically be trusted as the sole source of truth. Research has repeatedly identified missing surfaces, fragmented geometry, incorrect volumes and misleading results in BIM-to-BEM exchanges. [web:88][web:681]

---

# Offshore Production Model

## Appropriate offshore scope

The offshore modelling team should initially perform factual interpretation and deterministic transcription:

- Register project and drawing revisions.
- Establish levels and elevations.
- Calibrate plan underlays.
- Trace zone footprints.
- Assign zone and room names.
- Define floor-to-floor and ceiling heights.
- Model external and internal analytical walls.
- Model floors, ceilings and roofs.
- Add windows, doors and skylights.
- Add eaves, fins and major shading.
- Model relevant context buildings.
- Establish zone and surface adjacencies.
- Identify voids, plenums, roofspaces and subfloors.
- Reference source sheets and details.
- Record assumptions and unresolved questions.

## Conditional offshore enrichment

Once geometry production is stable, offshore staff may also assign data governed by explicit decision tables:

- Construction references copied from schedules
- Glazing type references
- Conditioned and unconditioned classifications
- Space-use categories
- Occupancy categories
- Lighting and equipment values explicitly shown
- HVAC zones explicitly documented on services drawings
- Prescribed HVAC templates
- Proposed/reference tags where rules are deterministic

Better Building supplies EnergyPlus HVAC templates for common systems, while DesignBuilder supports both simplified and detailed HVAC modelling. [web:727][web:729][web:730]

## Local engineering scope

The Australian engineering team should retain responsibility for:

- NCC pathway selection
- Proposed/reference model interpretation
- Façade-system U-values
- Glazing acceptance criteria
- Thermal bridges
- Air leakage and infiltration
- Ambiguous zoning decisions
- HVAC equivalence assumptions
- Performance-solution conclusions
- Model approval
- Final certification and report narrative

For reference-building verification, model-control rules and software consistency are important, reinforcing the need for versioned transformations rather than informal manual edits. [web:732]

---

# Offshore Brief

## Required project brief

Each brief should state:

- Project identifier
- Building classification
- Site and climate location
- Drawing register and revisions
- Included and excluded buildings
- Included levels
- True north
- Coordinate and dimension units
- Zoning rules
- Treatment of corridors and common areas
- Treatment of roofspaces and subfloors
- Treatment of voids, atria and plenums
- Wall-location convention
- Floor and ceiling conventions
- Window and door modelling rules
- Shading inclusion threshold
- Context-building requirements
- Naming conventions
- Required exchange formats
- QA acceptance criteria
- Clarification process
- Assumption classifications
- Required screenshots and marked-up drawings

## Stable identifiers

All significant objects should use persistent external identifiers, for example:

    BLDG-A_L03_ZONE-031
    BLDG-A_L03_WALL-031-N
    BLDG-A_L03_WIN-031-N-02

These identifiers should remain stable across authoring, compliance, façade and simulation models wherever possible.

## Object register

| Object ID | Type | Level | Source | Verification | Assumption |
|---|---|---|---|---|---|
| `ZONE-031` | Thermal zone | L03 | A103 Rev C | Verified | None |
| `WALL-031-N` | External wall | L03 | A103/A401 | Inferred | Wall line unclear |
| `WIN-031-N-02` | Window | L03 | A601 | Verified | None |

This register allows façade objects to be grouped by elevation, orientation, system and construction without relying on fragile names generated by simulation software.

---

# Handoff Package

Every offshore submission should contain more than the native project file.

    project/
      source/
        original-drawing-set.pdf
        drawing-register.csv
      underlays/
        A101_L00_revC.png
        A102_L01_revC.png
      authoring/
        native-project-file
      exchange/
        proposed.idf
        proposed.epJSON
        proposed.gbxml
        model.dsbXML
      review/
        assumptions.csv
        object-register.csv
        geometry-summary.json
        qa-results.json
        model-preview.glb
        marked-up-plans.pdf
      manifest.json

Only the formats relevant to the selected authoring application need to be included.

## Manifest contents

The manifest should record:

- Project ID
- Model ID
- Drawing issue and revision
- Modeller
- Reviewer
- Software and version
- Exporter and schema versions
- Units
- Coordinate system
- True north
- Creation date
- Review date
- Model status
- Known exclusions
- Unresolved issues
- File names
- File hashes

---

# Automated QA

Development effort should focus on QA, normalisation and model compilation rather than building another geometry editor.

## Geometry checks

- Valid polygons
- No self-intersections
- No duplicate vertices
- No zero-area surfaces
- Correct face orientation
- Closed thermal volumes
- Consistent zone heights
- Correct level elevations
- Matching interior surfaces
- No orphaned surfaces
- No unintended gaps or overlaps
- Openings contained by parent walls
- Openings coplanar with parent walls
- No duplicated openings
- Correct exterior and interior boundary conditions
- Valid shading geometry
- Valid roof geometry
- No unintended building/shading intersections

## Semantic checks

- Unique object IDs
- Required names populated
- Zone classifications present
- Conditioned status present
- Every object linked to a source drawing or assumption
- Construction assignments present or explicitly null
- HVAC assignments present or explicitly null
- Proposed/reference classification controlled
- Units and coordinate systems recorded
- Application and schema versions recorded

## Reconciliation checks

- Zone floor area against architectural schedules
- Gross floor area against project data
- Zone volume against geometry
- Façade area by orientation
- Window area by orientation
- Window-to-wall ratio
- Roof and floor area
- Number of zones by level
- Number of windows by schedule type
- Construction type quantities
- Conditioned and unconditioned areas

## Visual checks

Generate automatically:

- GLB model
- Colour-coded zones
- Boundary-condition view
- Construction-type view
- Glazing-type view
- Source-sheet links
- Level-by-level SVG plans
- Façade elevation diagrams
- Model-versus-source overlays

---

# Downstream Pipeline

## Recommended architecture

    Architectural PDFs
        ↓
    Sheet extraction, OCR and revision registration
        ↓
    Prepared modelling pack and structured brief
        ↓
    Offshore analytical model production
        ↓
    Native model + exchange files + assumptions
        ↓
    Canonical analytical geometry
        ↓
    Automated topology, semantic and provenance QA
        ↓
    Australian technical review
        ↓
    NCC, construction, schedule and HVAC enrichment
        ↓
    Proposed and reference simulation models
        ↓
    EnergyPlus or other simulation engines
        ↓
    Façade schedules, compliance outputs and design feedback

## Treat exports as compilation

The pipeline should not assume universal round-trip interoperability.

Instead:

    Authoring model
        → importer
        → canonical model
        → validation and repair
        → engineering enrichment
        → engine-specific compiler
        → simulation or compliance model

Each target model should be reproducible from the canonical model and a versioned transformation configuration.

## Façade integration

The canonical model should support downstream generation of:

- Façade areas by elevation and orientation
- Window and opaque-envelope schedules
- Window-to-wall ratios
- Glazing type distributions
- Construction-system mappings
- Solar-exposure inputs
- Zone-to-façade relationships
- Thermal-model boundary dimensions
- Condensation-analysis inputs
- NCC façade-performance summaries
- Design-change comparisons
- Alternative façade-option models

Façade systems should reference persistent source surface and opening IDs rather than depend solely on EnergyPlus-generated names.

---

# Implementation Priorities

## Scripts worth building

Targeted scripts are viable and should focus on:

1. PDF sheet extraction and rasterisation.
2. OCR of sheet names, room labels and dimensions.
3. Drawing-register generation.
4. Underlay naming and revision control.
5. IDF-to-epJSON conversion.
6. epJSON geometry extraction.
7. dsbXML parsing.
8. IFC room and envelope extraction.
9. Canonical-model generation.
10. Geometry validation.
11. Surface and opening reconciliation.
12. GLB and SVG visualisation.
13. Object-register generation.
14. NCC proposed/reference transformations.
15. Façade schedule generation.
16. Model revision comparison.
17. Automated offshore QA reports.

## Work to avoid initially

Avoid investing early effort in:

- A complete geometry editor
- Full bidirectional IFC round-tripping
- Generic BIM-to-BEM automation for every BIM platform
- Unsupported binary reverse-engineering
- Writing directly into proprietary project files
- Automatic interpretation of all NCC judgement
- Fully automatic HVAC inference from incomplete drawings
- Forcing all complex geometry into 2.5D
- Supporting every exchange format equally

---

# Pilot Program

## Pilot tools

Run an initial comparison using:

1. **Better Building**
2. **DesignBuilder**
3. **HERO**, for a separate residential data-access test
4. **Rhino/Pollination**, as the complex-geometry control

## Pilot projects

Use at least two representative projects:

### Residential pilot

- Class 1 dwelling or small apartment project
- Pitched roof
- Roofspace
- Garage or unconditioned zone
- Mixed glazing types
- Eaves and shading
- Several construction types
- NatHERS or Specification 44 relevance

### Commercial pilot

- Small Class 5–9 building
- Multiple levels
- Perimeter and internal zones
- Several façade orientations
- Mixed glazing
- Core or common areas
- Nontrivial shading
- Simplified and detailed HVAC requirements

## Pilot metrics

Measure:

- Brief-preparation time
- Operator training time
- Modelling time
- Clarification count
- First-pass QA failure count
- Local review time
- Local correction time
- Export completeness
- Geometry reconstruction effort
- Ability to preserve identifiers
- Time to add constructions
- Time to add HVAC
- Time to create proposed/reference models
- Time to generate façade schedules
- Time to process an architectural revision
- Total cost per accepted model

The most important metric is:

> Australian technical review and correction time per accepted model.

---

# Decision Framework

## Choose Better Building if

- Australian NCC work dominates.
- The offshore team benefits from a constrained interface.
- The process is mainly forward-moving.
- IDF or epJSON is an acceptable handoff.
- Native authoring-object round-tripping is not essential.
- Browser or cloud deployment simplifies offshore operations.
- The export-fidelity pilot succeeds.

## Choose DesignBuilder if

- Programmatic editing is required.
- Native model regeneration is required.
- Models undergo repeated revisions.
- Rich editable handoff is important.
- Detailed HVAC is commonly built in the same platform.
- Complex geometry is frequent.
- Python, C# or API automation justifies the heavier platform.

## Choose HERO if

- NatHERS certification is the primary endpoint.
- Residential and apartment modelling dominates.
- HERO provides supported geometry access.
- A separate façade or EnergyPlus model is acceptable.
- The data-access spike succeeds.

## Choose Rhino/Pollination if

- The building has geometry outside the comfortable range of 2.5D tools.
- Façade segmentation or parametric studies dominate.
- A tightly governed Grasshopper workflow can be maintained.
- Skilled operators are available.

## Choose IESVE if

- Energy, daylight, solar, loads and HVAC will remain in IESVE.
- GEM is useful to the broader workflow.
- The benefits of one integrated simulation environment outweigh licensing and training complexity.

---

# Key Takeaways

1. **Better Building is the strongest initial hypothesis** for the proposed Australian, straight-through PDF-to-model-to-compliance workflow.

2. **DesignBuilder remains the safest integration platform** where native editable exchange, API access, model regeneration and bidirectional workflows matter.

3. **HERO is a credible high-priority residential option**, but geometry extraction must be proven through a short, vendor-aware feasibility study.

4. **Rhino/Pollination should be retained as an exception pathway** for complex roofs, curved façades, irregular sections and specialised façade geometry.

5. **Do not make any authoring application the integration backbone.** Treat it as a replaceable production workstation.

6. **Require neutral or documented exchange files in every handoff.** A native project file alone is insufficient.

7. **Separate geometry, engineering and compliance layers.** This prevents unnecessary remodelling when construction, HVAC or NCC assumptions change.

8. **Use persistent identifiers and source references.** Every significant zone, surface and opening should map to a drawing or logged assumption.

9. **Invest development effort in QA and transformation rather than geometry authoring.** Targeted scripts provide greater leverage than building another modeller.

10. **Treat model exports as compiler targets rather than expecting perfect round-tripping.**

11. **Use a hybrid canonical representation:** Dragonfly-style 2.5D objects for normal spaces and Honeybee-style explicit 3D geometry for exceptions.

12. **Select the production tool using pilot evidence.** Offshore modelling speed alone is not enough; local correction time, downstream usability and revision performance determine the true cost.

---

# Recommended Next Actions

1. Obtain trial or evaluation access to Better Building and DesignBuilder.
2. Select one representative residential project and one commercial project.
3. Prepare a single controlled offshore modelling brief.
4. Build both projects in Better Building and DesignBuilder.
5. Export IDF and epJSON from Better Building.
6. Export dsbXML, IDF and gbXML from DesignBuilder.
7. Create a short HERO geometry-access test.
8. Write an initial epJSON geometry extractor.
9. Write an initial dsbXML parser or use the published schema.
10. Generate canonical JSON, GLB and level SVG outputs.
11. Implement the first automated QA checks.
12. Measure offshore time, local correction time and downstream façade usability.
13. Select the default platform based on accepted-model economics.
14. Retain Rhino/Pollination as the formal complex-geometry exception workflow.
15. Approach HERO regarding a supported read-only geometry export or JSON interface.