# C++ framework architecture

## Purpose

Design a reusable C++ framework that can be embedded in different applications
without coupling the world model to a specific game engine.

## Module boundaries

Candidate modules include:

- core identifiers, types, world state, and event interfaces;
- ontology and schema loading/validation;
- resource, organization, quest, and other optional domain modules;
- event graph and rule evaluation, with separate interfaces for optional
  reasoning and collective-decision sub-plugins;
- persistence and interchange;
- Unreal Engine and Godot adapters.

Keep the core free of engine headers and engine-owned object lifetimes. Optional
reasoners, databases, and authoring tools should sit behind narrow interfaces.
The collective-decision sub-plugin should be independently selectable and
replaceable, so games can choose voting, delegation, individual decision
policies, or no collective-governance automation.

## C++ standard compatibility

The requirement is to support C++20, C++23, and C++26. A practical policy is to
keep the public API expressible in C++20 and compile/test the library under each
supported language mode. C++23- or C++26-only implementation optimizations can
be conditional, but must not leak into the baseline API.

Confirm compiler and standard-library availability for all targeted engines
before declaring a configuration supported. The C++26 toolchain matrix may
depend on compiler maturity; document exact compiler versions and tested
configurations rather than assuming that a language flag alone proves
compatibility.

## Public API and binary boundaries

Prefer value types, explicit ownership, and stable opaque identifiers at module
boundaries. C++ ABI compatibility across different compilers and engine
versions should not be assumed. Evaluate source integration, static/shared
libraries, and a narrow C-compatible boundary based on the plugin and
distribution needs.

Avoid exposing unstable third-party types from public headers. Use explicit
error/result types for loading, validation, rule evaluation, and persistence.

## Build and packaging

Use a portable build configuration (for example, CMake) with independently
selectable modules and tests. Engine plugin packaging may require engine-owned
build systems in addition to the standalone build. Document supported
platforms, compilers, runtime libraries, and dependency licenses.

Optional decision-making strategies should be build-time and/or runtime
configurable according to the host game's needs. Keep configuration explicit
and validated; disabling a strategy must leave a defined fallback rather than
an unresolved decision.

## Open questions

- Is the framework distributed as source, static libraries, shared libraries,
  or more than one form?
- What is the minimum platform/compiler matrix required by target projects?
- Which data types and APIs need long-term source or binary stability?
