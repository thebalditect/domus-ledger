# 1. Use Conventional Commits

Date: 2025-09-14

Author: Mandar Dharmadhikari

## Status

Accepted

## Context

We want to maintain a clean, consistent, and machine-readable Git history for the URL Shortener project.

Key reasons:

* Automation: Conventional Commit messages enable automatic changelog generation and semantic versioning in the future.
* Collaboration: Enforcing a shared standard helps all contributors write meaningful commit messages.
* Quality gates: Prevents accidental commits with vague messages like “fix stuff” or “update code”.

## Options considered

* **Free-form commit messages**: No enforcement, relies on developer discipline.

* **Git hooks with custom scripts**: DIY validation, more maintenance.

* **Husky + Commitlint + Conventional Commits**: Industry standard, supported ecosystem, integrates with CI.

## Decision

We will adopt Conventional Commits as the commit message format, enforced locally with Husky and Commitlint, and validated remotely in CI.

* **Local enforcement**: Husky runs a commit-msg Git hook. Commitlint checks the commit message against the Conventional Commits spec.

* **Remote enforcement**: A GitHub Action (commitlint-github-action) validates all commits in PRs. This ensures that no commit can bypass validation, even if local hooks are disabled.

## Consequences

### Positive

* Commit history is structured and readable.

* We can later adopt semantic-release to automate versioning and changelogs.

* Developers receive fast feedback locally (via Husky hooks).

* CI provides an additional safety net.

### Negative

* Developers need Node.js installed to run Husky + Commitlint locally.

* Small learning curve for new contributors unfamiliar with Conventional Commits.
