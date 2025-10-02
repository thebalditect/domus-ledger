# 2. Use Vertical Architecture For Project

Date: 2025-09-14

Author: Mandar Dharmadhikari

## Context

Traditional layered architecture (e.g., `api`, `core`, `infra`) often leads to
tight coupling between layers, and makes it harder to see where specific business
logic lives. As the system grows, changes can ripple across multiple layers,
increasing cognitive load and slowing down feature development.

We want an architecture that:

- Groups code by **business feature** (expenses, income, users, reports).
- Keeps each slice **independent** and self-contained.
- Encourages **modularity** and easier testing.
- Supports growth toward microservices if needed.

## Decision

We will implement the API using **Vertical Slice Architecture**:

- Each feature is a slice (`/features/<name>`) containing its models, schemas,
  services, routes, and tests.
- Shared concerns (DB, security, config) live in `/infra`.
- Routers are registered in `main.py`, one per slice.
- Business logic is kept inside services in each slice, not spread across layers.

## Consequences

- Features are self-contained and easy to reason about.
- Easier to onboard new developers (look in one folder per feature).
- Encourages domain-driven thinking.
- Some duplication may occur (e.g., shared schema patterns).
- Requires discipline to keep infra concerns out of slices.

## Alternatives Considered

- **Layered architecture**: Rejected due to long-term complexity and coupling.
- **Clean/Hexagonal architecture**: More abstract than needed for this project.
