export interface Project {
    title: string
    tag: string
    category: string
    description: string
    highlights: string[]
    featured: boolean
}

export const projects: Project[] = [
    {
        title: 'Government resilient housing prototype and heatwave stress testing',
        tag: 'Climate resilience, adaptation and strategic policy',
        category: 'Thermal and environmental physics',
        description: 'Engineered a comprehensive digital twin to evaluate building envelope performance and severe thermal resilience for a government-backed residential prototype.',
        highlights: [
            'Simulated extreme thermal loads by splicing historical extreme heatwave datasets directly into local meteorological weather profiles.',
            'Optimised building envelope parameters, thermal mass distribution, and shading geometries to prevent indoor overheating during severe climate events.',
            'Delivered a verified benchmark of climate-adaptive architecture currently used to inform regional resilient housing standards.'
        ],
        featured: false
    },
    {
        title: 'Masterplan microclimate and human thermal comfort index suite',
        tag: 'Microclimate, urban physics and human comfort',
        category: 'Energy and microclimate dynamics',
        description: 'Implemented advanced human thermal comfort modelling frameworks to evaluate outdoor environmental conditions across complex urban developments.',
        highlights: [
            'Quantified complex bioclimatic physics across diverse microclimates using multi-index thermal comfort evaluations.',
            'Synthesised meteorological wind, radiation, and humidity data into actionable spatial design parameters for urban master planning.',
            'Guided public realm design to mitigate urban heat island effects and significantly improve pedestrian thermal comfort.'
        ],
        featured: false
    },
    {
        title: 'Future climate weather file application and stress testing',
        tag: 'Climate resilience, adaptation and strategic policy',
        category: 'Thermal and environmental physics',
        description: 'Evaluated long-term infrastructure resilience and overheating risks under projected future climate scenarios using dynamic thermal simulation.',
        highlights: [
            'Injected synthetic future climate projections into building energy models to test asset durability against long-term thermal shifts.',
            'Calculated forward-looking HVAC energy consumption spikes and unadapted free-running building overheating rates.',
            'Provided asset owners with quantitative risk profiles to future-proof capital investments against projected climate extremes.'
        ],
        featured: false
    },
    {
        title: 'Facade thermal physics and heat transfer analysis',
        tag: 'Building physics and envelope performance',
        category: 'Thermal and environmental physics',
        description: 'Conducted rigorous steady-state heat transfer analysis on high-performance architectural envelope assemblies and framing geometries.',
        highlights: [
            'Evaluated two-dimensional thermal bridging across complex mullion and transom assemblies to calculate accurate linear thermal transmittance.',
            'Modelled advanced glazing configurations to balance solar heat gain coefficients, centre-of-glass U-values, and low-emissivity coating performance.',
            'Eliminated localised condensation risks and ensured compliance with stringent envelope thermal performance standards.'
        ],
        featured: false
    },
    {
        title: 'Enterprise data-driven reporting ecosystem and documentation engine',
        tag: 'Computational tooling, infrastructure and enterprise systems',
        category: 'Physical-digital systems architecture',
        description: 'Architected a centralised data-driven documentation and reporting ecosystem to automate technical consulting deliverables across the practice.',
        highlights: [
            'Established a single source of truth database capturing thousands of project metadata fields to eliminate redundant manual data entry.',
            'Engineered automated document assembly pipelines linking simulation outputs and engineering tables directly into client deliverables.',
            'Containerised the entire typesetting workflow onto local servers, slashing report compilation times and removing quality assurance bottlenecks.'
        ],
        featured: false
    },
    {
        title: 'Commercial rebrand and operational overhaul',
        tag: 'Strategy and practice operations',
        category: 'Physical-digital systems architecture',
        description: 'Restructured professional services, market positioning, and client communication workflows to navigate macroeconomic headwinds.',
        highlights: [
            'Overhauled technical messaging and service offerings to realign the business with high-value advisory engineering work.',
            'Standardised client-facing technical communications and digital touchpoints to streamline project acquisition.',
            'Protected senior engineering capacity and optimised operational workflows for resilient small practice management.'
        ],
        featured: false
    },
    {
        title: 'Gas turbine engine performance digital twin',
        tag: 'Thermodynamic systems and power generation',
        category: 'Thermal and environmental physics',
        description: 'Developed an iterative optimisation simulation model to diagnose thermodynamic degradation vectors in aircraft gas turbine engines.',
        highlights: [
            'Programmed automated mathematical optimisation routines to process physical test bed sensor recordings from aircraft engines.',
            'Mapped multi-parameter thermodynamic degradation vectors against empirical pressure, temperature, and thrust measurements.',
            'Accurately identified component-level efficiency losses to support rigorous aerospace testing and diagnostic validation.'
        ],
        featured: false
    },
    {
        title: 'Kilometre-high solar updraft chimney simulation pipeline',
        tag: 'Thermodynamic systems and power generation',
        category: 'Thermal and environmental physics',
        description: 'Architected an extreme-scale fluid dynamics and thermal-updraft simulation pipeline for a multi-kilometre solar power tower.',
        highlights: [
            'Modelled complex ground heat transfer and diurnal thermal storage across expansive sub-canopy air volumes.',
            'Simulated dynamic solar transmission through massive glass canopies coupled with atmospheric thermodynamics over high vertical profiles.',
            'Quantified aerodynamic friction and turbine momentum extraction to validate large-scale renewable power generation potential.'
        ],
        featured: false
    },
    {
        title: 'Battery energy storage systems digital twin and tariff optimisation',
        tag: 'Energy systems, decarbonisation and carbon accounting',
        category: 'Energy and microclimate dynamics',
        description: 'Engineered a containerised computational wrapper to evaluate financial viability and optimal sizing for commercial battery storage systems.',
        highlights: [
            'Simulated complex diurnal electrical demand profiles and variable onsite solar generation outputs.',
            'Evaluated round-trip efficiency, degradation factors, and multi-tiered commercial electricity tariff structures.',
            'Delivered rapid, automated financial payback assessments to guide municipal energy infrastructure investments.'
        ],
        featured: false
    },
    {
        title: 'Complex HVAC system simulation and NABERS commitment agreements',
        tag: 'Thermodynamic systems and power generation',
        category: 'Thermal and environmental physics',
        description: 'Executed predictive thermal energy simulations to model operational building physics for formal pre-construction environmental ratings.',
        highlights: [
            'Engineered detailed building physics models incorporating off-axis performance drift, part-load efficiencies, and complex zoning schedules.',
            'Simulated multi-zone variable air volume and refrigerant flow systems alongside integrated photovoltaic metering layouts.',
            'Successfully secured official high-star pre-construction environmental ratings through rigorous independent third-party audits.'
        ],
        featured: false
    },
    {
        title: 'Whole-of-building upfront embodied carbon quantification',
        tag: 'Energy systems, decarbonisation and carbon accounting',
        category: 'Energy and microclimate dynamics',
        description: 'Delivered whole-of-building embodied carbon assessments and regulatory rating submissions for major commercial construction projects.',
        highlights: [
            'Ingested and sanitised complex contractor bills of quantities across thousands of structural and envelope line items.',
            'Applied rigorous data-cleansing rules to eliminate double-counting between structural reinforcement and concrete volumes.',
            'Linked material quantities to verified environmental product declarations to secure official green building sustainability ratings.'
        ],
        featured: false
    },
    {
        title: 'Offshore platform explosion overpressure and CFD automation',
        tag: 'Fluid dynamics, aerodynamics and safety engineering',
        category: 'Fluid dynamics and risk systems',
        description: 'Automated computational fluid dynamics workflows to evaluate blast wave propagation and explosion overpressures on offshore infrastructure.',
        highlights: [
            'Modelled complex turbulence acceleration caused by gas clouds passing through dense networks of industrial pipework.',
            'Engineered custom geometric translation scripts to ingest complex computer-aided design files directly into explosion simulation solvers.',
            'Eliminated manual geometry recreation bottlenecks, saving hundreds of engineering hours while enhancing structural safety analysis.'
        ],
        featured: false
    },
    {
        title: 'Industrial fire behaviour, smoke dynamics and compute infrastructure',
        tag: 'Fluid dynamics, aerodynamics and safety engineering',
        category: 'Fluid dynamics and risk systems',
        description: 'Deployed high-performance computing infrastructure and advanced simulation pipelines to model complex fire dynamics and smoke propagation.',
        highlights: [
            'Configured rigorous computational fluid dynamics models to simulate fire growth, heat release rates, and toxic smoke movement.',
            'Specified and deployed a dedicated headless Linux compute cluster managed via batch queuing protocols to accelerate processing times.',
            'Delivered critical visibility and toxic gas timeline outputs to integrate seamlessly with life safety evacuation egress models.'
        ],
        featured: false
    },
    {
        title: 'Industrial stack plume dispersion and aviation safety assessment',
        tag: 'Fluid dynamics, aerodynamics and safety engineering',
        category: 'Fluid dynamics and risk systems',
        description: 'Evaluated environmental compliance and aviation safety constraints for industrial exhaust stack emissions within protected airspaces.',
        highlights: [
            'Modelled atmospheric boundary layer profiles and local surface roughness lengths to capture velocity gradients and dispersion patterns.',
            'Analysed historical meteorological data to track thermal buoyancy, vertical velocity, and worst-case atmospheric inversion conditions.',
            'Verified stack geometries against civil aviation obstacle limitation surfaces to prevent hazardous plume penetration into flight corridors.'
        ],
        featured: false
    },
    {
        title: 'Rail tunnel and enclosed car park ventilation architecture',
        tag: 'Fluid dynamics, aerodynamics and safety engineering',
        category: 'Fluid dynamics and risk systems',
        description: 'Engineered multi-level computational airflow and contaminant dispersion models for underground transportation infrastructure.',
        highlights: [
            'Simulated vehicle emission rates and traffic queue distributions to map carbon monoxide concentration profiles across basement car parks.',
            'Optimised impulse jet fan placements and bulk airflow paths to eliminate stagnant pockets and drive pollutants toward extraction shafts.',
            'Verified pollutant levels against strict regulatory exposure thresholds to ensure safe environmental conditions for occupants.'
        ],
        featured: false
    },
    {
        title: 'Urban wind microclimate, pedestrian safety and CFD validation',
        tag: 'Microclimate, urban physics and human comfort',
        category: 'Energy and microclimate dynamics',
        description: 'Assessed pedestrian wind comfort and safety around high-rise developments by combining physical wind tunnel testing with numerical simulation.',
        highlights: [
            'Conducted physical boundary layer wind tunnel testing and benchmarked concurrent transient fluid dynamics numerical models.',
            'Resolved complex flow separation and high-velocity corner streams to evaluate peak gust forces against human instability criteria.',
            'Guided architectural canopy and podium setback designs to mitigate severe wind hazards in dense urban public realms.'
        ],
        featured: false
    },
    {
        title: 'Reflected glare hazard studies and geometric automation',
        tag: 'Microclimate, urban physics and human comfort',
        category: 'Energy and microclimate dynamics',
        description: 'Developed an automated numerical framework to evaluate specular reflections and veiling glare hazards impacting transport infrastructure.',
        highlights: [
            'Converted manual geometric drafting rules into an automated computational algorithm calculating vector angles of reflected sunlight.',
            'Generated synthetic luminance maps along complex transit corridors and road overpasses to measure driver visual impairment risks.',
            'Optimised facade glass reflectance limits and exterior shading geometry to eliminate hazardous glare into surrounding public zones.'
        ],
        featured: false
    },
    {
        title: 'Stadium pitch microclimate and cumulative PAR radiometric modelling',
        tag: 'Microclimate, urban physics and human comfort',
        category: 'Energy and microclimate dynamics',
        description: 'Evaluated solar access and photosynthetically active radiation distribution across major sports stadia to optimise turf agronomic health.',
        highlights: [
            'Constructed detailed three-dimensional stadium bowl geometries to model complex diurnal and seasonal overshadowing patterns.',
            'Developed cumulative sky radiometric models integrating direct and diffuse solar radiation components against turf species requirements.',
            'Optimised mobile artificial growth lighting schedules and spatial placements to eliminate chronic shadow deficits while minimising operational costs.'
        ],
        featured: false
    },
    {
        title: 'Daylight availability, solar access and visual comfort simulation',
        tag: 'Building physics and envelope performance',
        category: 'Thermal and environmental physics',
        description: 'Engineered comprehensive daylighting and visual comfort assessments to balance statutory planning compliance with occupant wellbeing.',
        highlights: [
            'Modelled complex sky brightness distributions and angle-dependent optical glass properties across commercial and residential developments.',
            'Evaluated internal daylight autonomy and computer screen glare to optimise workspace layouts and living area natural lighting.',
            'Formulated computational abstraction methods to run high-fidelity ray-tracing simulations within strict commercial delivery windows.'
        ],
        featured: false
    },
    {
        title: 'Indoor air quality and cleanroom aerodynamic CFD optimisation',
        tag: 'Fluid dynamics, aerodynamics and safety engineering',
        category: 'Fluid dynamics and risk systems',
        description: 'Modelled internal air distribution, contaminant clearance efficiency, and laminar airflow integrity across specialised controlled environments.',
        highlights: [
            'Simulated multi-zone mechanical ventilation and displacement airflow configurations to track age of air and carbon dioxide dispersion.',
            'Evaluated cleanroom particle clearance dynamics and laminar flow preservation under operational boundary conditions.',
            'Partnered with mechanical design teams to refine diffuser placements and supply velocities for superior indoor air quality.'
        ],
        featured: false
    },
    {
        title: 'Enterprise infrastructure risk audit and systems formalisation',
        tag: 'Computational tooling, infrastructure and enterprise systems',
        category: 'Physical-digital systems architecture',
        description: 'Conducted a comprehensive audit of practice-wide digital infrastructure and data workflows to mitigate key-person operational risk.',
        highlights: [
            'Deconstructed and mapped the complete end-to-end digital ecosystem spanning servers, containerised workloads, and relational databases.',
            'Established standardised technical taxonomies and formal IT notations to document system dependencies and operational pipelines.',
            'Created a structured delegation matrix to uncouple high-value strategic architecture from routine maintenance tasks.'
        ],
        featured: false
    }
]