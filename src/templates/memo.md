---
compiler: jonmorgan
document_type: memo
to: Will Symons, Deloitte
from: Jon Morgan
subject: Integration of Computational Fluid Dynamics (CFD) within Digital Twin Architecture
date: 22 June 2026
reference: JM-2026-0622
version: 1.0
---

# Project Appreciation

## Facility Architecture & Core Ecosystem
Based on our recent 40-minute briefing, my understanding is that you are developing a digital twin capability to support an AI Infrastructure Center of Excellence (CoE). This capability is being built on the NVIDIA Omniverse platform. Your current architecture focuses on integrating multiple operational modules—specifically Building Management Systems (BMS), Electrical Power Monitoring Systems (EPMS), and Data Center Infrastructure Management (DCIM)—utilising the NVIDIA Omniverse Data Center Blueprint framework. 

The focus of our initial conversation, and the likely direction of ongoing work, relates specifically to the application of Computational Fluid Dynamics (CFD) to enhance this digital twin framework. While I am still establishing a complete understanding of your core commercial drivers, my current appreciation is that the primary focus centres on risk mitigation, failure mitigation, the tracking of operational degradation, and the management of environmental stresses.

## The Cascade Mechanism & Component Thermal Risks
Specifically, I understand there is a critical need to address potential gaps regarding mechanisms that trigger cascading thermal events. These events—whether caused by an abrupt failure, the gradual degradation of components over time, or external environmental stresses—begin by affecting air-side cooling, which subsequently impacts server rack and individual server cooling. Even in environments where GPUs are liquid-cooled, many critical components remain air-cooled, including:

* Memory (RAM)
* Storage (SSDs)
* Power Supply Units (PSUs)
* PCIe Buses, Interconnects, and CPUs

The digital twin needs to be enhanced to accurately understand and simulate the thermal impact on these specific air-cooled components during sudden failure events, extended degradation phases, or periods of environmental stress. Additionally, there may be a potential requirement for the digital twin to track or look at real-time updates to Power Usage Effectiveness (PUE), though this needs to be confirmed.

## Technical Data Flow & Multiscale Interaction
From a technical integration perspective, my understanding of the data flow and physics interaction is as follows:

* **The Environment Scale:** The BMS provides real-time monitoring data points across the facility, while the DCIM provides complementary real-time operational telemetry. Though their polling times vary, this changing BMS telemetry dynamically drives updates to the macro-level CFD model of the entire data centre. This updates the simulated air circulation and thermal variations across the facility.
* **The Boundary Condition:** The macro-level CFD model computes these environmental shifts to determine localised parameters, such as the specific "air-on" temperature at the intake of a given server rack. 
* **The Component Scale:** By combining this localised room-scale boundary condition with the real-time server-level telemetry provided by the DCIM, the twin can build an accurate profile of internal server conditions. This allows the system to anticipate thermal variations and predict potential risks to individual air-cooled components inside the chassis due to component degradation, environmental stress, or system anomalies.

# Preliminary Observations
Based on our briefing, I note the following aspects of your proposed approach to implementing the CFD capability:

* **Modeling Scope:** The current plan targets solving both the macro-level and server-level airflow and thermal solutions.
* **Software Platforms:** The platforms mentioned for generating the baseline high-fidelity datasets are OpenFOAM and ANSYS (with a preference for OpenFOAM due to licensing costs). These datasets will be critical for training the real-time AI surrogate models, bypassing traditional solver runtime constraints.
* **Delivery Model:** It remains to be determined whether this CFD capability will be implemented via an in-house capability or through an external partnership.

# Strategic Context
A key strength of your platform selection is that the wider data centre simulation ecosystem has already transitioned toward this real-time requirement via **AI-driven surrogate models** and **Real-Time Model Predictive Control (MPC)**. Established market solutions demonstrate that the industry is actively shifting away from raw numerical solver execution online:

* Platforms like **SimScale** utilise native AI surrogates to instantly evaluate layout changes and cooling options before running full solver validations.
* **Cadence Design Systems** leverages high-fidelity 3D datasets to train deep learning surrogate models specifically for real-time data centre operational environments.
* NVIDIA natively supports this approach via frameworks like NVIDIA Modulus, designed explicitly to build physics-ML models and neural operators (such as Fourier Neural Operators) that deploy directly as AI surrogates within the Omniverse environment.

Evaluating how these established surrogate methodologies align with your requirements—relative to building custom, raw solver integration loops—will be a key consideration in determining how the AI Infrastructure Center of Excellence (CoE) achieves real-time functionality while managing computational lag and potential seat-licensing barriers.

# Summary of Scoping Observations
The following operational parameters require formal baseline definition to move forward:

* **Commercial Driver Confirmation:** Definitive confirmation of the primary use cases (e.g., risk mitigation, component degradation tracking, or real-time PUE updates) to set the required engineering boundaries.

* **Solver Architecture Selection:** Determination of the mathematical strategy required to deliver immediate computational insights inside Omniverse, bypassing traditional offline solver delays.

* **Multi-Scale Interface Mapping:** Structural mapping of the data handoff between the overarching data centre hall volume and the localised server chassis component layers.

* **Telemetry Synchronisation Framework:** Designing a data digestion mechanism to handle the asynchronous polling times inherent to combining BMS and DCIM telemetry.

* **Capability Delivery Strategy:** Deciding whether the integration roadmap will focus on building custom, internal CFD pipelines or establishing strategic partner ecosystem integrations.

* **Ecosystem Agnosticism Framework:** Determining how to integrate open-source datasets and third-party commercial platform inputs while avoiding proprietary vendor lock-in.

* **Commercial SLA Risk Mapping:** Structuring how the digital twin translates physical thermal stress profiles into commercial risk metrics, particularly around mixed air- and liquid-cooled environments.