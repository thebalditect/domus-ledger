# 4. Use Poetry for dependency management

Date: 2025-09-14

Author: Mandar Dharmadhikari

## Status

Accepted

## Context

We need to decide how to manage dependencies for the Personal Finance App project.  
Two main options were considered:

* **requirements.txt (pip)**

  * The traditional Python way of declaring dependencies.  
  * Widely supported, simple to use.  
  * Requires manual or external tooling (e.g., pip-tools) for dependency resolution and lock files.  
  * Managing multiple environments (dev, test, prod) requires multiple files.  

* **Poetry (pyproject.toml)**  
  * A modern dependency and packaging manager for Python.  
  * Handles dependency resolution and generates a lock file automatically.  
  * Supports dependency groups (dev/test/prod) natively.  
  * Provides commands for virtual environment management, building, and publishing.  
  * Slightly more setup overhead, but better for long-term maintainability.  

## Decision

We will use **Poetry** as the dependency manager for this project.  
Additionally, for Docker and CI/CD compatibility, we will export a `requirements.txt` from Poetry (`poetry export`) so that standard Python tooling can install dependencies where needed.

## Consequences

### Positive

* **Reproducible builds** with `poetry.lock`.  
* **Simpler management of dev/test/prod dependencies** via groups.  
* **Automatic dependency resolution** avoids version conflicts.  
* Easier onboarding and long-term maintainability for a growing project.  

### Negative

* Adds a layer of tooling not always preinstalled in minimal environments.  
* Requires exporting `requirements.txt` for Docker, adding a minor step.  
