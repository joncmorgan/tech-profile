---
id: "physics-informed-ml-surrogate-model"
title: "Physics-Informed ML Surrogate Model for Dynamic Building Performance"
company: "Moreland Energy Foundation (MEFL)"
period: "2014-2018"
outcome: "Decarbonisation and ESG Impact"
primaryCategory: "Computational Tooling, Infrastructure & Enterprise Systems"
secondaryCategory: "Building Physics & Envelope Performance"
status: "prototype"
confidentiality: "public"
---
# Physics-Informed ML Surrogate Model for Dynamic Building Performance

## Context
Overcoming the computational cost and latency of numerical physics simulations by building a high-speed machine learning surrogate model to predict dynamic building thermodynamic behaviour in milliseconds.

## Execution
- Parametric Simulation Orchestration: Scripted and orchestrated hundreds of parameterised multi-zone thermal dynamic simulations across diverse architectural, weather, and operational variables.
- Feature Engineering & Normalisation: Processed multi-dimensional input and output datasets, cleaning and normalising feature spaces spanning thermal mass, HVAC capacities, solar heat gain coefficients, and internal gains.
- Model Training with scikit-learn: Implemented and tested variants of regression models using scikit-learn to map input parameters directly to dynamic performance outcomes (energy loads, peak thermal demand, internal temperature fields).
- Inference & Accuracy Evaluation: Evaluated prediction accuracy against baseline physical simulation results, enabling rapid interactive scenario exploration without traditional solver run times.

## Note
UPDATED (24 Sep 2026): Jon has now recalled this was at Moreland Energy
Foundation, likely as a prototype — company and status fields updated
accordingly. Still **not fully confident** in this recollection ("I don't
quite recall") — treat as best-current-belief rather than fully settled,
and revisit if anything surfaces that contradicts it.

Checked against [[darebin-solar-savers]] (confirmed MEF, 2014-2018): a
different project — solar sizing/payback via demand and generation
profiles, not dynamic multi-zone thermal simulation via scikit-learn on
parameterised building variables — but it's independent evidence Jon was
doing surrogate-model-style ML work (trained regression standing in for
full simulation) at MEF in that era, consistent with this recollection.