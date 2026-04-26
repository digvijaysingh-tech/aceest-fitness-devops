# ACEest Fitness & Gym — DevOps CI/CD Pipeline

BITS M.Tech Assignment 2 — end-to-end DevOps pipeline for the ACEest Fitness & Gym Flask application.

## Stack
- **App:** Python 3.12 + Flask
- **Tests:** Pytest + coverage
- **VCS:** Git + GitHub (`digvijaysingh-tech/aceest-fitness-devops`)
- **CI:** Jenkins (local) with polling SCM
- **Quality:** SonarQube (local, Docker)
- **Container:** Docker, images pushed to `digvijaysinghshekhawat/aceest-fitness` on Docker Hub
- **Orchestration:** Minikube (local Kubernetes)
- **Deployment strategies:** Blue-Green, Canary, Rolling Update, A/B Testing, Shadow

## Versions
Tracked via git tags: `v1.0`, `v1.1`, `v1.1.2`, `v2.0.1`, `v2.1.2`, `v2.2.1`, `v2.2.4`, `v3.0.1`, `v3.1.2`, `v3.2.4`.

## Quick start (local)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python -m app.main          # serves on http://localhost:5000
```

## Repo layout
```
app/            Flask application package
tests/          Pytest test suite
docker/         Dockerfile + supporting files
jenkins/        Jenkinsfile (declarative pipeline)
k8s/            Kubernetes manifests per deployment strategy
sonar/          sonar-project.properties + reports
report/         Submission report (2-3 pages)
versions/       Original Tkinter reference files from professor
```
