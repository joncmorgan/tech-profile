# Software Design Document (SDD) & Technical Specification

**Project Title:** Automated Building Enclosure Physics & Geometry Engine (`ber-engine`)

**Document Type:** Technical Specification, System Architecture & Phased Roadmap

**Target Audience:** Computational Engineers, Full-Stack Python Developers, AI/Agentic Engineers

**Version:** 2.0-PROPOSED

**Status:** Ready for Sprint Execution

## 1. Executive Summary & Core Objective

### 1.1 Purpose

The **BER-Engine** is a modular, open-source Python system designed to ingest early-stage, non-CAD architectural concept data (voice transcripts, site coordinates, and simple 2D concept sketches) and programmatically assemble a watertight, simulation-ready EnergyPlus (`.idf`) thermal model.

The engine replaces manual CAD/BIM tracing and setup loops. It queries surrounding urban massing via OpenStreetMap, enforces Australian National Construction Code (NCC) 2025 Section J and Specification 33 compliance constraints, and executes headless sensitivity simulations via `ZoneHVAC:IdealLoadsAirSystem`. The system outputs structured JSON metrics to drive front-end reporting and early-phase client advisory briefs.

### 1.2 Phased Delivery Strategy

To maximize velocity and de-risk the physics pipeline, implementation is structured into three progressive iterations:

```
[ Phase 1: Rapid CLI PoC ] ──► [ Phase 2: Streamlit + 3D Viewer ] ──► [ Phase 3: Full Containerized Engine ]
  • Synthetic & GeoJSON intake    • Interactive Streamlit dashboard     • Local multimodal (Whisper + Vision)
  • Programmatic IDF (geomeppy)   • 3D WebGL / PyVista model viewer      • Docker containerization
  • EnergyPlus CLI execution      • Automated OSMnx GIS context         • API / Batch reporting pipeline
  • Fast terminal output (<60s)   • Parameter adjustment sliders        • Production deployment
```

- **Phase 1 (Proof of Concept, 3-Day Sprint):** A headless Command-Line Interface (CLI) tool. Uses typed Pydantic intake, programmatic geometry building via `geomeppy`, runs headless EnergyPlus, and outputs peak cooling/heating metrics.
    
- **Phase 2 (Interactive Prototype, Sprint 2):** A lightweight **Streamlit** front-end with an embedded 3D viewer (Plotly / Three.js / PyVista) enabling architects to view generated thermal zones, fenestration, and surrounding context shading before running simulations.
    
- **Phase 3 (Production Engine, Sprint 3):** Full containerization (Docker), complete local multimodal parsing (Whisper audio transcription + Qwen2.5-VL sketch extraction via Ollama/vLLM), and integration into automated report builders.
    

### 1.3 Key Success Criteria

- **Execution Velocity:** Total end-to-end pipeline run (intake to thermal results) in $< 45$ seconds.
    
- **Geometric Watertightness:** 100% compliant outward surface normals and counter-clockwise (CCW) vertex winding with zero non-convex surface errors in EnergyPlus.
    
- **Agentic Friendliness:** Codebase structured into pure, deterministic functions with type hints and test fixtures, allowing VS Code AI agents (e.g., Cline, Roo Code, GitHub Copilot) to execute and self-heal autonomously.
    
- **100% Open-Source Toolchain:** Zero proprietary runtime or CAD license dependencies.
    

## 2. Open-Source Technology Stack

|   |   |   |
|---|---|---|
|**Layer / Concern**|**Recommended Tool**|**Rationale & Agentic Value**|
|**Language Runtime**|Python 3.11+|Strong type annotations, high-performance data classes, fast async I/O.|
|**Data Contracts**|`pydantic` (v2)|Runtime data validation; generates JSON schemas natively for AI agent tools.|
|**GIS & Projections**|`osmnx`, `pyproj`, `shapely`|Auto-reprojects lat/long to local Cartesian UTM coordinates (e.g., EPSG:32755 for Melbourne).|
|**Geometry & IDF Engine**|`geomeppy` (built on `eppy`)|Eliminates error-prone Jinja2 string templating. Guarantees watertight vertex ordering and native zone slicing.|
|**Simulation Core**|Headless EnergyPlus (v24.1+)|DOE/NREL open-source thermal simulator.|
|**Interactive UI**|`streamlit`|Fast, pure-Python UI iteration; no JavaScript build overhead for the PoC.|
|**3D Visualization**|`pyvista` / `plotly` / `deck.gl`|Renders extruded 3D multi-zone models, window cutouts, and shading context directly in Streamlit.|
|**Multimodal Extraction**|`faster-whisper` + `Qwen2.5-VL`|Fully open-weight, self-hostable models for transcript and floorplate polygon extraction.|
|**Testing Harness**|`pytest`, `hypothesis`|Provides deterministic feedback loops for VS Code autonomous agents.|

## 3. System Architecture & Component Design

```
                       DATA FLOW & MODULE PIPELINE
                       
   [ Voice Audio ]           [ Sketch Image ]          [ Address / Lat-Lon ]
          │                         │                            │
          ▼                         ▼                            ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │ MODULE 1: INTAKE & NORMALIZATION (Phase 1: Synthetic / Phase 3: AI)    │
  │ • Audio -> faster-whisper -> raw transcript text                       │
  │ • Sketch -> Qwen2.5-VL -> normalized 2D loop coordinates [0, 1]        │
  │ • pyproj converts site Lat/Long to localized UTM coordinate frame      │
  │ • Shoelace scaler adjusts 2D footprint to target Gross Floor Area (GFA)│
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │ ProjectIntakeSpec (Pydantic Model)
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │ MODULE 2: GIS CONTEXT FETCHER (context_gis.py via OSMnx)               │
  │ • Queries OSM building footprints within radius $R$ (default: 150m)    │
  │ • Reprojects context footprints into local origin $(0, 0)$             │
  │ • Extracts heights or tags default storeys ($h = 3.5\text{m}$)         │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │ ContextMassing Model
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │ MODULE 3: PARAMETRIC GEOMETRY & ZONE SLICER (geometry_engine.py)       │
  │ • Builds base thermal zones using geomeppy                             │
  │ • Splits perimeter ($4.5\text{m}$ depth) & core zones per NCC Spec 33  │
  │ • Handles concave multi-polygon buffering safely                       │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │ MultiZoneIDF (In-memory)
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │ MODULE 4: FENESTRATION & SHADING INJECTOR (fenestration_engine.py)     │
  │ • Calculates outward normals and cardinal orientations (N, S, E, W)    │
  │ • Punches orientation-specific Window-to-Wall Ratio (WWR) sub-surfaces │
  │ • Adds horizontal shading fins / overhangs for balconies               │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │ Complete IDF Geometry
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │ MODULE 5: NCC PHYSICS & IDEAL LOADS COMPILER (physics_compiler.py)     │
  │ • Injects NCC 2025 Climate Zone boundary conditions                    │
  │ • Sets internal loads: People ($10\text{m}^2/\text{p}$), Lights, Plugs │
  │ • Assigns ZoneHVAC:IdealLoadsAirSystem to all zones                    │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │ Watertight model.idf
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │ MODULE 6: SIMULATION EXECUTOR & METRIC EXTRACTOR (sim_runner.py)       │
  │ • Invokes EnergyPlus CLI in headless subprocess                        │
  │ • Reads output SQLite / tabular CSV data                               │
  │ • Emits final SimulationSummaryPayload (JSON)                          │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
     [ Streamlit 3D Dashboard ]                   [ Final Report Payload ]
```

## 4. Mathematical Formulation & Algorithmic Rules

### 4.1 Coordinate Projection & Shoelace Area Scaling

To avoid geographic distortions, coordinates are projected to Universal Transverse Mercator (UTM) meters using `pyproj`.

Given $n$ normalized polygon vertices from vision intake $(x_i, y_i) \in [0, 1]$:

$$A_{\text{norm}} = \frac{1}{2} \left\vert{} \sum_{i=0}^{n-1} \left( x_i y_{i+1} - x_{i+1} y_i \right) \right\vert{} \quad \text{with } (x_n, y_n) = (x_0, y_0)$$

Target GFA per floor is $A_{\text{target}}$. The linear scale factor $S$ is computed as:

$$S = \sqrt{\frac{A_{\text{target}}}{A_{\text{norm}}}}$$

Scaled local coordinates:

$$(X_i, Y_i) = (x_i \cdot S, \; y_i \cdot S)$$

### 4.2 Facet Azimuth & Cardinal Orientation

For a wall facet defined by points $P_1(X_1, Y_1)$ to $P_2(X_2, Y_2)$ in counter-clockwise order:

$$\vec{d} = (X_2 - X_1, \; Y_2 - Y_1)$$

Outward normal vector $\vec{n}$:

$$\vec{n} = (Y_2 - Y_1, \; -(X_2 - X_1))$$

Azimuth angle $\theta$ relative to True North ($0^\circ$):

$$\theta = \left( \operatorname{atan2}(n_x, n_y) \cdot \frac{180}{\pi} + 360 \right) \pmod{360}$$

- **North:** $315^\circ \le \theta < 45^\circ$  
    
- **East:** $45^\circ \le \theta < 135^\circ$  
    
- **South:** $135^\circ \le \theta < 225^\circ$  
    
- **West:** $225^\circ \le \theta < 315^\circ$  
    

### 4.3 Safe Non-Convex Perimeter Slicing

Perimeter zoning requires offsetting exterior facets inward by $4.5\text{m}$ (NCC Specification 33). For non-convex polygons, `shapely.geometry.Polygon.buffer(-4.5)` can split into disjoint polygons (`MultiPolygon`).

The geometry algorithm must handle this via:

```
buffered = footprint.buffer(-4.5, join_style="mitre", mitre_limit=2.0)
if buffered.is_empty:
    # Floorplate is too narrow; entire floor defaults to a single perimeter zone
    core_zones = []
elif buffered.geom_type == "Polygon":
    core_zones = [buffered]
elif buffered.geom_type == "MultiPolygon":
    # Disjoint core regions treated as distinct thermal zones
    core_zones = list(buffered.geoms)
```

## 5. Canonical Data Contracts (Pydantic Models)

Using Pydantic models provides immediate type safety, auto-generated JSON schemas, and structured error reporting for VS Code agents.

```
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple

class WWRTarget(BaseModel):
    north: float = Field(default=0.60, ge=0.0, le=0.95)
    south: float = Field(default=0.65, ge=0.0, le=0.95)
    east: float = Field(default=0.45, ge=0.0, le=0.95)
    west: float = Field(default=0.35, ge=0.0, le=0.95)

class ProjectIntakeSpec(BaseModel):
    project_name: str
    site_address: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    storeys: int = Field(default=1, ge=1, le=100)
    floor_to_floor_height_m: float = Field(default=3.6, ge=2.4, le=6.0)
    target_gfa_per_floor_sqm: float = Field(..., gt=10.0)
    footprint_polygon_normalized: List[Tuple[float, float]] = Field(
        ..., min_length=3, description="Clockwise or CCW ordered normalized 2D loop [(x, y)]"
    )
    wwr_targets: WWRTarget = Field(default_factory=WWRTarget)
    balcony_depth_m: float = Field(default=0.0, ge=0.0, le=5.0)
    ncc_climate_zone: int = Field(default=6, ge=1, le=8)

class ZoneThermalMetric(BaseModel):
    zone_name: str
    orientation: str
    floor_level: int
    peak_cooling_watts_per_sqm: float
    peak_heating_watts_per_sqm: float

class SimulationSummaryPayload(BaseModel):
    status: str
    runtime_seconds: float
    project_name: str
    gross_floor_area_sqm: float
    total_glazing_area_sqm: float
    overall_wwr: float
    peak_cooling_sensible_watts_per_sqm: float
    peak_heating_watts_per_sqm: float
    critical_facade_orientation: str
    zone_metrics: List[ZoneThermalMetric]
```

## 6. Phased Implementation Roadmap

### Phase 1: Rapid CLI End-to-End PoC (Target: 3-Day Sprint)

**Objective:** Validate the core physics loop from normalized input to EnergyPlus output JSON without any front-end overhead.

- **Day 1: Intake & Geometric Foundations**
    
    - Set up directory structure and `.clinerules` / `.cursorrules`.
        
    - Implement `ProjectIntakeSpec` schema and synthetic JSON test fixtures (Rectangle, L-shape, U-shape).
        
    - Build Shoelace scaler and local UTM reprojection with `pyproj`.
        
- **Day 2: Programmatic IDF Generation (`geomeppy`)**
    
    - Instantiate clean EnergyPlus IDF via `geomeppy`.
        
    - Extrude storeys and perform $4.5\text{m}$ perimeter/core slicing.
        
    - Punch directional windows per WWR inputs.
        
    - Inject NCC 2025 Section J default constructions and `ZoneHVAC:IdealLoadsAirSystem`.
        
- **Day 3: Headless Execution & CLI Harness**
    
    - Implement CLI runner: `python -m ber_engine.cli run --input sample.json`.
        
    - Subprocess invocation of EnergyPlus with bundled Australian `.epw` weather file.
        
    - Parse EnergyPlus output files (`eplusout.csv` or SQLite) into `SimulationSummaryPayload`.
        
    - Benchmark execution velocity ($< 60\text{s}$).
        

### Phase 2: Streamlit Interface & 3D Model Viewer (Target: Sprint 2)

**Objective:** Deliver an interactive web dashboard for real-time model preview, context inspection, and simulation triggers.

- **Interactive Controls:**
    
    - Sliders for WWR by orientation (North, South, East, West).
        
    - Floor-to-floor height, balcony depth, and storey count inputs.
        
- **3D Geometry & Context Visualizer:**
    
    - Render extruded thermal zones with differentiated color codes (Perimeter vs. Core).
        
    - Embed 3D building visualization using `pydeck` or `plotly.graph_objects.Mesh3d` directly in Streamlit.
        
- **OSM Context Integration:**
    
    - Integrate `context_gis.py` using `osmnx` to query surrounding building massing within $150\text{m}$.
        
    - Render surrounding urban shading context in the 3D viewport.
        
- **Results Panel:**
    
    - Metric cards displaying peak cooling/heating loads ($\text{W/m}^2$).
        
    - Sensitivity charts showing thermal loads across orientation variants.
        

### Phase 3: Multimodal Intake, Dockerization & Production Polish (Target: Sprint 3)

**Objective:** Eliminate manual parameter entry via open-source multimodal AI and package into an isolated container.

- **Multimodal Extraction Layer:**
    
    - Audio intake: Transcribe user audio briefs using local `faster-whisper`.
        
    - Sketch intake: Ingest hand-drawn/concept floorplate sketches using local `Qwen2.5-VL` (via Ollama or vLLM) to output ordered polygon vertices $[(x, y)]$.
        
- **Docker Containerization:**
    
    - Multi-stage `Dockerfile` bundling Ubuntu, Python 3.11, EnergyPlus 24.1+, and weather data.
        
    - Health checks and CLI/Streamlit entrypoints.
        
- **Automated Brief Reporting:**
    
    - Render HTML/PDF pre-planning advisory brief summarizing facade compliance and thermal performance.
        

## 7. VS Code & Agentic Tooling Architecture

To enable autonomous coding agents (e.g., Cline, Roo Code, GitHub Copilot) to generate and debug features independently, the codebase must adhere to strict modular boundaries and automated test loops.

### 7.1 Repository Structure

```
ber-engine/
├── .clinerules                      # Autonomous agent guidelines & commands
├── Dockerfile                       # Container definition (Phase 3)
├── pyproject.toml                   # Poetry or Pip-tools dependencies
├── README.md
├── src/
│   └── ber_engine/
│       ├── __init__.py
│       ├── cli.py                   # Phase 1: CLI entry point
│       ├── app.py                   # Phase 2: Streamlit web application
│       ├── contracts/
│       │   ├── __init__.py
│       │   └── schemas.py           # Pydantic v2 data models
│       ├── intake/
│       │   ├── __init__.py
│       │   ├── scaler.py            # Shoelace scaling & pyproj UTM transform
│       │   └── multimodal.py        # Phase 3: Whisper & Vision parsing
│       ├── gis/
│       │   ├── __init__.py
│       │   └── context_osm.py       # OSMnx context fetcher
│       ├── geometry/
│       │   ├── __init__.py
│       │   ├── slicer.py            # Perimeter / Core zone decomposition
│       │   └── builder.py           # geomeppy IDF assembly & window puncher
│       ├── physics/
│       │   ├── __init__.py
│       │   └── ncc_loads.py         # NCC 2025 Section J & Ideal Loads injection
│       └── runner/
│           ├── __init__.py
│           ├── eplus.py             # Headless EnergyPlus runner
│           └── parser.py            # SQLite/CSV results parser
├── weather/
│   └── AUS_VIC.Melbourne.AP.948680_TMYx.2007-2021.epw
└── tests/
    ├── conftest.py
    ├── fixtures/
    │   ├── intake_sample_rect.json
    │   ├── intake_sample_lshape.json
    │   └── intake_sample_concave.json
    ├── test_scaler.py
    ├── test_geometry.py
    └── test_end_to_end.py
```

### 7.2 Agent Configuration Contract (`.clinerules` / `.cursorrules`)

Store this specification in the project root to enforce execution boundaries for autonomous agents:

```
# Agent Execution Rules for ber-engine

1. Architecture Principles:
   - Pure functions only: Keep core calculation routines decoupled from I/O.
   - Strict typing: All functions must use standard Python typing and Pydantic schemas.
   - Programmatic IDF: Never assemble EnergyPlus files using raw string or Jinja2 templating. Always use `geomeppy`.

2. Verification & Testing:
   - Run `pytest tests/` after modifying any geometry or physics files.
   - If tests fail, inspect the eplusout.err output log to diagnose geometry or boundary condition errors.
   - Any new geometry feature MUST include an accompanying test fixture in `tests/fixtures/`.

3. EnergyPlus Rules:
   - Surface vertices MUST always be wound counter-clockwise when viewed from the exterior.
   - ZoneHVAC:IdealLoadsAirSystem must be attached to every conditioned zone.
   - Floor surfaces must use ground or adiabatic boundary conditions; roofs must use outdoor boundary conditions.
```

## 8. Operational Guardrails & Edge Cases

1. **Complex / Narrow Floorplates:**
    
    If a building facet is narrower than $9.0\text{m}$, inward buffering of $4.5\text{m}$ leaves zero core area. The geometry engine must gracefully detect an empty core buffer and classify the entire floor segment as perimeter.
    
2. **Missing Shading Context:**
    
    If OSM returns zero building ways in the requested radius (e.g., greenfield sites), the context processor must log a warning and return an empty context list without breaking the downstream pipeline.
    
3. **EnergyPlus Non-Convex Warning Mitigation:**
    
    While EnergyPlus allows non-convex zones if triangulation flags are set, using `geomeppy`’s built-in zone triangulation utilities ensures surface surfaces are decomposed into convex polygons prior to simulation.
    
4. **Execution Isolation:**
    
    Every simulation run must execute inside an isolated temporary directory (`tempfile.TemporaryDirectory()`) to avoid file contention and race conditions when running concurrent sensitivity analyses.