---
id: "darebin-solar-savers"
title: "Darebin Solar Savers — Real-Time Phone Support Tool"
company: "Moreland Energy Foundation (MEFL)"
period: "2014-2018"
outcome: "Decarbonisation and ESG Impact"
primaryCategory: "Energy Systems, Decarbonisation & Carbon Accounting"
secondaryCategory: "Computational Tooling, Infrastructure & Enterprise Systems"
status: "delivered"
confidentiality: "public"
---
# Darebin Solar Savers — Real-Time Phone Support Tool

## Context
Built a tool for Darebin City Council's Solar Savers program, used by council
officers taking phone calls from residents/tenants. Superseded roughly a
decade ago; no longer in use.

## Execution
- Built typical household demand profiles and typical solar generation
  profiles in Python.
- Ran these through a simple multi-dimensional regression/ML model
  trained on that data, to predict system-sizing and payback outcomes
  without needing a full physics simulation per call.
- Wrapped in a simple front end (possibly Qt or similar — unconfirmed,
  a long time ago) usable by a non-technical front-line user.
- Council officer captures key billing data from the resident live, over
  the phone.
- Tool immediately recommends an appropriate solar system size for the
  household and presents the expected payback period.
- Designed for a real-time, defensible financial/technical recommendation
  deliverable during a single phone call.

## Note
This is an early example of a physics-informed ML surrogate model (a
trained regression standing in for a full simulation) built at Moreland
Energy Foundation — relevant context for [[physics-informed-ml-surrogate-model]],
whose employer attribution is still unconfirmed. Worth checking whether
that's describing this same project, a related one, or something
different entirely.