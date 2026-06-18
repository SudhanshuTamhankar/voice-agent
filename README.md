# Antigravity Multi-Agent Software Engineering Template

This template gives you a reusable AI software engineering team for Antigravity.

## What is included

- `.agents/agents.md` — role definitions for the multi-agent engineering team
- `.agents/workflows/` — reusable workflows/slash-command style instructions
- `.agents/skills/` — focused skills for product, architecture, frontend, backend, database, QA, security, DevOps, and docs
- `production_artifacts/` — PRD, technical specification, implementation plan, test report, security report, deployment report, and release checklist placeholders
- `docs/` — API docs, ADR notes, and production runbook placeholders
- `app/` — placeholder folder for your actual project code

## How to use

Copy this folder into the root of your project, or copy only the `.agents`, `production_artifacts`, and `docs` folders into an existing project.

Then use workflows like:

```txt
/build-feature "Build a SaaS dashboard where users can sign up, create projects, invite teammates, and view usage analytics."
```

```txt
/production-readiness
```

```txt
/bugfix "Users are redirected to the dashboard after login, but the dashboard API returns 401 until refresh."
```

```txt
/release "Prepare version 1.0.0 for production deployment, but do not deploy until I approve."
```

## Recommended operating rule

Do not call a project production-ready until PRD, technical specification, implementation, QA, security, DevOps, documentation, and release checklist are complete.
