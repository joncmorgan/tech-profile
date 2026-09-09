export const profile = {
    fullName: 'Jon Morgan',
    title: 'Principal Solutions Architect',
    institute: '',
    author_name: 'Jon Morgan',
    practice_statement: [
        'Drawing on over 25 years of hands-on engineering experience, I combine technical expertise with strategic execution and leadership. Over that time, I have run an independent ESD consulting practice, designed full-stack software architectures from the user interface down to containerisation, and built deep computational models for physical and environmental systems.',
        'I enjoy solving complex problems end-to-end, embracing an agile approach to adapt and deliver quickly. My focus is firmly on applying my multidisciplinary background and skill set where it can make a tangible difference, working with meaning and purpose.'
    ],
    practice_quote: 
        'Cities, infrastructure, and natural resources face a pivotal transition. Navigating this demands rigorous resilience and adaptation planning—challenges that are never just technology problems, but economic, human, and environmental issues all at once. Meeting this moment takes systems thinking and practical engineering to cut through complexity and turn insight into action.'
    ,
    background_pillars: [
        {
            title: 'Commercial & Operational Ownership',
            description: 'Running a small ESD consulting practice for nearly a decade means owning everything from cash flow, billing, and admin to branding, strategy, and team leadership. I understand the unglamorous mechanics of what it takes to keep an independent engineering business alive, solvent, and moving forward.',
            icon: 'briefcase'
        },
        {
            title: 'Sustainability & Built Environment',
            description: 'Two decades of applied work across sustainable buildings, human-focused design, and environmental systems. This isn’t theoretical policy work—it’s the ground-level reality of shaping how spaces actually perform for the people using them and the environment surrounding them.',
            icon: 'leaf'
        },
        {
            title: 'Full-Stack Development & Infrastructure',
            description: 'Building custom software because commercial tools rarely fit the job. My stack spans the full width: from front-end user interfaces and custom data pipelines all the way down to containerization, deployment, and local-first DevOps architecture.',
            icon: 'code'
        },
        {
            title: 'Physical Systems Simulation & Analytics',
            description: 'Decades of deep engineering work modeling how the physical world behaves. Whether it\'s fluid dynamics, thermal physics, or complex environmental mechanics, my focus has always been ensuring that analytical tools accurately reflect physical reality.',
            icon: 'cpu'
        }
    ],
    domain_knowledge: [
        {
            title: 'Critical Infrastructure & Transport',
            description: 'Applied systems work across road, rail, and major transport corridors, focusing on environmental integration, safety mechanics, and long-term asset resilience.',
            icon: 'compass'
        },
        {
            title: 'Offshore & Marine Engineering',
            description: 'Specialised environmental and hydrodynamic modelling for offshore installations and marine assets operating under extreme structural and weather loads.',
            icon: 'anchor'
        },
        {
            title: 'Thermal Dynamics & Building Physics',
            description: 'Advanced thermal performance modelling, bioclimatic design, and environmental systems optimisation for complex built environments.',
            icon: 'thermometer'
        },
        {
            title: 'Fluid Dynamics & Atmospheric Flow',
            description: 'Numerical simulation of fluid mechanics, ventilation performance, dispersion modelling, and microclimate interactions across physical assets.',
            icon: 'wind'
        },
        {
            title: 'Energy Systems & Infrastructure',
            description: 'Modelling for renewable energy integration, storage systems, complex HVAC mechanics, and grid-interactive built environments.',
            icon: 'zap'
        },
        {
            title: 'Climate Resilience & Adaptation',
            description: 'Assessing long-term environmental stress, urban heat dynamics, and climate vulnerability frameworks for cities and regional assets.',
            icon: 'globe'
        }
    ],
    research_areas: [
        { 
            title: 'Physical-Digital Systems Architecture', 
            description: 'Building the plumbing that connects physical assets to code. I design custom data schemas, automated computational pipelines, and local software infrastructure—replacing brittle spreadsheets with robust internal tools that actually work.' 
        },
        { 
            title: 'Thermal, Energy & Microclimate Dynamics', 
            description: 'Bioclimatic comfort, complex HVAC optimisation, and renewable integration. Moving beyond theoretical compliance to ensure built systems handle real environmental stress and survive local climate loads.' 
        },
        { 
            title: 'Fluid Dynamics & Risk Systems', 
            description: 'Numerical modelling for fluid mechanics, atmospheric dispersion, and critical infrastructure stress-testing. Rigorous engineering focus to ensure analytical models don\'t fall apart when conditions get extreme.' 
        },
        { 
            title: 'Technical Direction & Specialist Execution', 
            description: 'Stepping into engineering or software teams to cut through complexity. Whether providing high-level technical leadership or rolling up my sleeves to solve intractable computational problems, I keep workflows tied to physical reality.' 
        },
    ],
    modes_of_engagement: [
        { 
            title: 'Technical Direction & Leadership', 
            description: 'Working directly with engineering and software teams to cut through complexity. Making sure analytical workflows stay rigorous, practical, and tied to physical reality rather than getting bogged down in dogma.' 
        },
        { 
            title: 'Systems Architecture & R&D', 
            description: 'Designing custom computational engines, spatial data pipelines, and automated simulation workflows that replace brittle spreadsheets with robust internal infrastructure.' 
        },
        { 
            title: 'Specialist Domain Execution', 
            description: 'Rolling up my sleeves to tackle intractable computational problems in environmental physics, fluid dynamics, and microclimate systems.' 
        },
    ]
}

export const social = {
    email: 'jonmorgan@fastmail.com',
    linkedin: 'https://www.linkedin.com/in/linkjonmorgan/',
    x: '',
    bluesky: '',
    github: '',
    gitlab: '',
    scholar: '',
    inspire: '',
    arxiv: '',
    orcid: '',
}

export const template = {
    website_url: 'https://localhost:4321',
    menu_left: false,
    transitions: true,
    lightTheme: 'autumn',
    darkTheme: 'autumn',
    excerptLength: 200,
    postPerPage: 5,
    base: ''
}

export const seo = {
    default_title: 'Jon Morgan — Physical-Digital Systems & Technical Architecture',
    default_description: '25 years bridging applied physics, environmental simulation, and custom software systems.',
    default_image: '/images/astro-academia.png',
}