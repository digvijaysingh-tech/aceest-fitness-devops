# Jenkins CI/CD Setup

Local Jenkins for ACEest Fitness & Gym. Runs on Docker with the host Docker socket mounted so pipeline stages can build and push images.

## Start Jenkins

```bash
cd jenkins
docker compose up -d
docker logs -f aceest-jenkins   # wait for "Jenkins is fully up and running"
```

Jenkins UI → http://localhost:8080

### First-time unlock

```bash
docker exec aceest-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Paste that password → **Install suggested plugins** → create admin user.

### Required plugins (install if not in suggested set)

- Pipeline (included in suggested)
- Git (included)
- Docker Pipeline
- SonarQube Scanner
- Credentials Binding (included)

## Credentials to add

In **Manage Jenkins → Credentials → System → Global credentials**:

| ID | Type | Used for |
|---|---|---|
| `dockerhub` | Username+password | Docker Hub push (`dshekhawat06640` + PAT) |
| `sonar-token` | Secret text | SonarQube scan (generate in Sonar UI after setup) |

## Create the pipeline job

1. **New Item → Pipeline → Name: `aceest-fitness`**
2. **Build Triggers:** Poll SCM → `H/5 * * * *` (every 5 min)
3. **Pipeline → Definition:** Pipeline script from SCM
4. **SCM:** Git → `https://github.com/digvijaysingh-tech/aceest-fitness-devops.git`
5. **Branch:** `*/main`
6. **Script Path:** `jenkins/Jenkinsfile`
7. Save → **Build Now**

## Pipeline stages

```
Checkout → Install & Test (pytest) → SonarQube Scan → Docker Build
        → Docker Push (main only) → Deploy to Minikube (main only)
```

## Stop / reset

```bash
docker compose down              # stops Jenkins, preserves jenkins_home volume
docker compose down -v           # also wipes all Jenkins config (start over)
```
