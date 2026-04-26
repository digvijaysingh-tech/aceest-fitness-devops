# SonarQube — Code Quality Setup

Local SonarQube for static analysis + coverage reporting.

## Start server

```bash
docker run -d \
  --name aceest-sonar \
  -p 9001:9000 \
  -v aceest_sonar_data:/opt/sonarqube/data \
  -v aceest_sonar_logs:/opt/sonarqube/logs \
  -v aceest_sonar_ext:/opt/sonarqube/extensions \
  sonarqube:community
```

UI → http://localhost:9001

Default credentials: `admin` / `admin` (forces password change on first login).

> **Note:** Host port 9001 is used because port 9000 was already bound
> on this machine. Container's internal port is still 9000.

## Generate a token (web UI)

1. Login as admin at http://localhost:9001
2. My Account → **Security** → **Generate Tokens**
3. **Name:** `aceest-scanner`  **Type:** Global Analysis Token
4. Copy the `sqa_...` token, save somewhere safe
5. Store it in Jenkins as Secret Text credential, ID = `sonar-token`

## Run the scanner locally

Regenerate coverage first (scanner reads `coverage.xml`):

```bash
source .venv/bin/activate
pytest                  # writes coverage.xml

docker run --rm \
  -e SONAR_HOST_URL=http://host.docker.internal:9001 \
  -e SONAR_TOKEN=<paste-token> \
  -v "$PWD:/usr/src" \
  sonarsource/sonar-scanner-cli:latest \
  -Dproject.settings=sonar/sonar-project.properties
```

Open http://localhost:9001/dashboard?id=aceest-fitness-devops to see the report.

## Stop / reset

```bash
docker stop aceest-sonar && docker rm aceest-sonar   # keeps volumes
docker volume rm aceest_sonar_data aceest_sonar_logs aceest_sonar_ext  # full wipe
```
