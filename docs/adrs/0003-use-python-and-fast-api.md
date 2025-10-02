# 3. Use Python and Fast API

Date: 2025-09-14

Author: Mandar Dharmadhikari

## Status

Accepted

## Context

We need to choose a programming language and web framework to implement the Personal Finance App APIs. The system must:  

- Expose a production-ready REST API.  
- Support **vertical slice architecture** and test-driven development (TDD).  
- Run well inside **Docker** and be deployable on cloud or Kubernetes.  
- Provide a good developer experience with rapid prototyping

Options considered:  

1. **Python + FastAPI**  
2. **Python + Flask**  
3. **Node.js + Express/NestJS**  
4. **Go + Gin/Fiber**  
5. **C# + ASP.NET Core**  

## Decision

Since we are exploring REST APIs with python, We will implement the Personal Finance APP APIs in **Python** using the **FastAPI** framework.  

- Python provides a strong ecosystem of libraries (SQLAlchemy, Alembic, Pytest, Pydantic, Celery).  
- FastAPI is lightweight, async-friendly, and provides automatic **OpenAPI documentation**.  
- Excellent fit for **vertical slice architecture**, where each slice can define its own router, schema, and business logic.  
- Native support for async I/O makes it scalable under concurrent traffic (important for redirect-heavy workloads).  
- Strong community adoption and wide documentation improve long-term maintainability.  

## Consequences

### Positive

- **High developer productivity**: rapid prototyping with type hints, Pydantic validation, and auto-generated docs.  
- **Modern async support**: suitable for high-concurrency redirect requests.  
- **Ecosystem**: easy integration with Postgres, Redis, and background workers.  
- **Onboarding**: Python is widely known, lowering barriers for new contributors.  

### Negative

- Python is slower than Go or Rust for raw performance (higher latency per request).  
- Requires care with async programming to avoid blocking calls.  
- Fewer built-in enterprise features compared to ASP.NET Core or Spring Boot.  

## References

- [FastAPI documentation](https://fastapi.tiangolo.com/)  
- [Why FastAPI?](https://fastapi.tiangolo.com/fastapi-in-production/)  
- [Benchmarking async Python frameworks](https://www.techempower.com/benchmarks/)  
