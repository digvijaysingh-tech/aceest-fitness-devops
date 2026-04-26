# SonarQube Scan Results

**Project:** `aceest-fitness-devops`
**Scan date:** 2026-04-26
**Dashboard:** http://localhost:9001/dashboard?id=aceest-fitness-devops

## Quality Gate: **Passed** ✅

| Metric | Value | Status |
|---|---|---|
| Lines of Code | 793 |  |
| Coverage | **94.2%** | 485 / 515 lines |
| Bugs | **0** | Best |
| Vulnerabilities | **0** | Best |
| Code Smells | **0** | Best |
| Duplicated Lines Density | **0.0%** | Best |
| Reliability Rating | **A** | Best |
| Security Rating | **A** | Best |
| Maintainability Rating | **A** | Best |
| Security Hotspots | 1 | Intentional (default admin/admin seed — documented) |

## Findings addressed during review

Two issues flagged on the first scan were fixed:

1. **Cognitive Complexity = 68 in `create_app()`** (Sonar limit: 15)
   Refactored into 9 Flask Blueprints under [app/routes/](../app/routes/):
   `meta`, `programs`, `clients`, `progress`, `workouts`, `membership`,
   `ai`, `reports`, `auth`. [app/main.py](../app/main.py) is now a thin
   composition root that just registers blueprints + error handlers.

2. **Binding to 0.0.0.0** (rule python:S104)
   This is intentional for containerized deployment — gunicorn (the real
   production entrypoint) binds 0.0.0.0 by design so the container accepts
   external traffic. The `__main__` block is for dev only. Suppressed via
   `sonar.issue.ignore.multicriteria` in [sonar-project.properties](sonar-project.properties)
   with an inline `# NOSONAR` comment explaining the why.

## How to reproduce

```bash
# Start SonarQube (once)
docker run -d --name aceest-sonar -p 9001:9000 \
  -v aceest_sonar_data:/opt/sonarqube/data \
  sonarqube:community

# Regenerate coverage
source .venv/bin/activate && pytest

# Run scanner
docker run --rm \
  -e SONAR_HOST_URL=http://host.docker.internal:9001 \
  -e SONAR_TOKEN=<token> \
  -v "$PWD:/usr/src" \
  sonarsource/sonar-scanner-cli:latest \
  -Dproject.settings=sonar/sonar-project.properties
```

Raw API snapshot saved in [sonar-scan-results.json](sonar-scan-results.json).
