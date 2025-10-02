# 5. Use PyTestArch for Architecture Tests

Date: 2025-09-15

Author: Mandar Dharmadhikari

## Status

Accepted

## Context

As our system grows with multiple vertical slices, enforcing architectural boundaries manually becomes error-prone.  
Developers may unintentionally:

- Introduce forbidden dependencies between features.
- Create circular imports that cause runtime errors.
- Break the intended Vertical Slice Architecture (VSA) by mixing responsibilities.

We need **automated checks** that enforce architectural rules both locally and in CI/CD pipelines.  

## Decision

We will use **[`pytest-arch`](https://github.com/pytest-arch/pytest-arch)** to define and enforce architectural constraints in tests.  
`pytest-arch` was chosen over `pytest-archon` because it:

- Has a more expressive, ArchUnit-inspired DSL.
- Is actively maintained and widely adopted.
- Provides built-in support for detecting cycles and enforcing layered or modular boundaries.

### Rules Enforced

1. **Vertical Slice Isolation**  
   Each feature (`src/features/<feature>`) must not import from another feature directly.  
   Cross-feature communication goes through:
   - `src/shared` (utilities, base abstractions), or  
   - domain events / service interfaces.

2. **Shared Module Usage**  
   Features are allowed to depend on `src/shared` for cross-cutting concerns.

3. **No Cyclic Imports**  
   Circular dependencies across modules are forbidden.

4. **CI/CD Enforcement**  
   Architecture tests run as part of the GitHub Actions workflow.  
   Any violation blocks merging to `main`.

## Consequences

### Positive

- Enforces Vertical Slice Architecture boundaries automatically.
- Prevents architectural drift as system grows.
- Provides long-term maintainability and confidence in refactoring.

### Negative

- Developers may face failing tests when violating rules, requiring structural changes.
- Requires discipline to keep rules updated when new architectural patterns emerge.

### Neutral

- Some duplication may appear across slices, but this is an intentional trade-off.

## Alternatives Considered

- **Manual code reviews**: rejected due to inconsistency and human error.  
- **Static analysis with pylint/flake8**: useful for style, but not for domain-specific rules.  
- **`pytest-archon`**: considered, but rejected due to lower adoption and less expressive DSL.  

## Decision Outcome

Adopt **`pytest-arch`** for architecture tests to enforce feature boundaries, shared usage, and prevent cyclic imports.  
These tests will run locally and in CI/CD pipelines to guarantee long-term architectural integrity.
