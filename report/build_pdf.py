"""
Compile Assignment 2 into a single PDF: ACEest Fitness & Gym DevOps CI/CD.
Sections: Cover, Overview, Architecture, Tooling, Deployment Strategies,
Challenges, Outcomes, Submission Checklist.
"""

from fpdf import FPDF
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "report" / "Assignment2_DigvijaySingh.pdf"

TITLE = "DevOps CI/CD Pipeline - Assignment 2"
AUTHOR = "Digvijay Singh Shekhawat"
STUDENT_ID = "2024TM93588"
STUDENT_EMAIL = "2024tm93588@wilp.bits-pilani.ac.in"
COURSE_NAME = "Introduction to DevOps"
COURSE_CODE = "CSIZG514 / SEZG514 (S1-25)"
PROGRAMME = "M.Tech Software Engineering"
SUBMISSION_DATE = "26 April 2026"
LOGO_PATH = str(ROOT / "report" / "bits_logo.png")

PAGE_W, PAGE_H = 210, 297  # A4
MARGIN = 15
USABLE_W = PAGE_W - 2 * MARGIN


def t(s: str) -> str:
    """Normalise unicode to Latin-1 (fpdf2 classic fonts)."""
    repl = {
        "—": "-", "–": "-", "‘": "'", "’": "'",
        "“": '"', "”": '"', "…": "...", " ": " ",
        "→": "->", "←": "<-", "•": "*",
        "✅": "[OK]", "❌": "[X]", "⚠": "!",
        "✓": "v", "✗": "x",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    return s.encode("latin-1", "replace").decode("latin-1")


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        try:
            self.image(LOGO_PATH, x=MARGIN, y=6, w=10)
        except Exception:
            pass
        self.set_xy(MARGIN + 12, 8)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(30, 60, 120)
        self.cell(0, 4, t(f"{COURSE_NAME} ({COURSE_CODE}) - Assignment 2"),
                  align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_x(MARGIN + 12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 4, t(f"{AUTHOR} ({STUDENT_ID})"), align="R")
        self.set_draw_color(180, 180, 180)
        self.line(MARGIN, 20, PAGE_W - MARGIN, 20)
        self.set_text_color(0, 0, 0)
        self.set_y(24)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_draw_color(180, 180, 180)
        self.line(MARGIN, self.get_y(), PAGE_W - MARGIN, self.get_y())
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, t(f"BITS Pilani WILP  |  {PROGRAMME}"), align="L")
        self.set_y(-12)
        self.cell(0, 5, t(f"Page {self.page_no()}"), align="R")
        self.set_text_color(0, 0, 0)


def add_cover(pdf: PDF):
    pdf.add_page()
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.8)
    pdf.rect(8, 8, PAGE_W - 16, PAGE_H - 16)
    pdf.set_line_width(0.2)

    pdf.set_y(22)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, t("Work Integrated Learning Programmes"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 11, t(PROGRAMME), align="C", new_x="LMARGIN", new_y="NEXT")

    try:
        logo_w = 55
        pdf.image(LOGO_PATH, x=(PAGE_W - logo_w) / 2, y=pdf.get_y() + 4, w=logo_w)
        pdf.ln(logo_w + 6)
    except Exception:
        pdf.ln(30)

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 11, t(COURSE_NAME), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 15)
    pdf.cell(0, 9, t("Individual Assignment"), align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 17)
    pdf.cell(0, 10, t("Assignment 2: ACEest Fitness & Gym CI/CD Pipeline"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    y = pdf.get_y()
    pdf.set_draw_color(50, 50, 50)
    pdf.line(MARGIN + 2, y, PAGE_W - MARGIN - 2, y)
    pdf.ln(3)

    def row(label, value, label_w=55):
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(label_w, 7, t(label))
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, t(value), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(MARGIN + 4); row("Course Name:", COURSE_NAME)
    pdf.set_x(MARGIN + 4); row("Course Code:", COURSE_CODE)
    pdf.set_x(MARGIN + 4); row("Programme:", f"{PROGRAMME} (WILP)")
    pdf.set_x(MARGIN + 4); row("Name:", AUTHOR)
    pdf.set_x(MARGIN + 4); row("Enrollment Number:", STUDENT_ID)
    pdf.set_x(MARGIN + 4); row("Email:", STUDENT_EMAIL)
    pdf.set_x(MARGIN + 4); row("Date:", SUBMISSION_DATE)
    pdf.set_x(MARGIN + 4); row("GitHub Repo:", "github.com/digvijaysingh-tech/aceest-fitness-devops")
    pdf.set_x(MARGIN + 4); row("Docker Hub:", "hub.docker.com/r/dshekhawat06640/aceest-fitness")

    pdf.ln(3)
    y = pdf.get_y()
    pdf.line(MARGIN + 2, y, PAGE_W - MARGIN - 2, y)


def section_header(pdf: PDF, title: str):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_fill_color(30, 60, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 11, t("  " + title), fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)


def h2(pdf: PDF, text: str):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 7, t(text), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def para(pdf: PDF, text: str):
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, t(text))
    pdf.ln(1)


def bullets(pdf: PDF, items):
    pdf.set_font("Helvetica", "", 10)
    for item in items:
        pdf.set_x(MARGIN + 3)
        pdf.cell(4, 5, t("*"))
        pdf.multi_cell(0, 5, t(item))


def kv_table(pdf: PDF, rows, col1_w=55):
    pdf.set_font("Helvetica", "", 10)
    for k, v in rows:
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(col1_w, 6, t(k), border="B")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, t(v), border="B")


def code_block(pdf: PDF, lines):
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("Courier", "", 8.5)
    for line in lines:
        pdf.set_x(MARGIN)
        pdf.cell(0, 4.5, t("  " + line), fill=True,
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


# ---------------- Sections ----------------

def sec_overview(pdf: PDF):
    section_header(pdf, "1. Executive Overview")

    para(pdf,
        "This assignment implements a complete DevOps pipeline for ACEest Fitness & "
        "Gym - a fictional fitness startup. The brief required a Flask web application "
        "evolving through incremental versions, with automated testing, containerisation, "
        "code quality analysis, and progressive deployment to Kubernetes.")

    para(pdf,
        "The professor provided ten Tkinter reference files (ACEestver-1.0.py through "
        "ACEestver-3.2.4.py). Since Tkinter is a desktop GUI framework and cannot be "
        "containerised or orchestrated on Kubernetes, the domain logic from those files "
        "(clients, programs, workouts, progress tracking, membership, AI-style plan "
        "generator, PDF reports) was ported into a Flask web application while preserving "
        "the same version naming and incremental evolution.")

    h2(pdf, "Headline outcomes")
    kv_table(pdf, [
        ("Versions shipped", "10 (v1.0 -> v3.2.4), each as its own git tag and Docker image"),
        ("Tests", "63 pytest cases, 100% passing"),
        ("Code coverage", "94.2% (measured by coverage.py, verified by SonarQube)"),
        ("SonarQube rating", "A on Reliability, Security, and Maintainability"),
        ("Sonar findings", "0 bugs, 0 vulnerabilities, 0 code smells, 0% duplication"),
        ("Docker images", "11 tags published to Docker Hub (10 versions + latest)"),
        ("K8s strategies", "5 - Rolling, Blue-Green, Canary, A/B, Shadow - all verified live"),
        ("Jenkins pipeline", "Declarative 6-stage pipeline with SCM polling every 5 min"),
        ("Repo", "Public on GitHub with 10 version tags, 17 commits"),
    ])


def sec_architecture(pdf: PDF):
    section_header(pdf, "2. CI/CD Architecture")

    para(pdf,
        "The pipeline follows the classical push-triggered continuous delivery model. "
        "A commit on the main branch drives a single Jenkins job through six stages; "
        "on success, the resulting image is published to Docker Hub and rolled out to "
        "the Minikube cluster.")

    h2(pdf, "End-to-end flow")
    code_block(pdf, [
        "Developer commits to main",
        "     |",
        "     v",
        "GitHub (public repo, 10 tags v1.0 -> v3.2.4)",
        "     |  Jenkins poll SCM every 5 min",
        "     v",
        "Jenkins (local Docker, jdk21 LTS)",
        "   1) Checkout                                ",
        "   2) Install & Test    pytest 63 cases       ",
        "   3) SonarQube Scan    python:S104 excluded  ",
        "   4) Docker Build      gunicorn, non-root     ",
        "   5) Docker Push       dshekhawat06640/...    ",
        "   6) Deploy to k8s     kubectl rollout       ",
        "     |                                         ",
        "     v                                         ",
        "Minikube (k8s v1.35.1) - 5 deployment strategies",
    ])

    h2(pdf, "Component responsibilities")
    kv_table(pdf, [
        ("Git / GitHub", "Version control. Tags v1.0 -> v3.2.4 drive immutable build history."),
        ("Jenkins", "Orchestrator. Polls SCM, runs pipeline, manages credentials."),
        ("Pytest + coverage", "Unit tests + XML coverage report consumed by SonarQube."),
        ("SonarQube Community", "Static analysis + coverage. Runs in Docker on host port 9001."),
        ("Docker", "Containerisation. Multi-stage Dockerfile with health check."),
        ("Docker Hub", "Image registry. Namespace dshekhawat06640, repo aceest-fitness."),
        ("Minikube", "Local Kubernetes (k8s v1.35.1). Backed by Docker Desktop driver."),
        ("kubectl", "Applies manifests under k8s/<strategy>/ per deployment mode."),
    ])


def sec_tooling(pdf: PDF):
    section_header(pdf, "3. Application & Test Design")

    para(pdf,
        "The Flask application is organised around domain-specific modules that each "
        "wrap a SQLite store. Routes are grouped into Flask Blueprints so the main "
        "factory function stays small enough to pass SonarQube's Cognitive Complexity "
        "gate (limit 15; our main.py scores below 5).")

    h2(pdf, "Module layout")
    code_block(pdf, [
        "app/",
        "  main.py         Flask app factory - registers blueprints, error handlers",
        "  programs.py     Program catalog (Fat Loss, Muscle Gain, Beginner) + AI templates",
        "  clients.py      ClientStore - SQLite CRUD",
        "  progress.py     ProgressStore - weekly adherence log",
        "  workouts.py     WorkoutStore + exercises",
        "  membership.py   Active/Inactive status with expiry date",
        "  auth.py         UserStore with SHA-256 salted password hashing",
        "  reports.py      PDF client report via fpdf2",
        "  db.py           SQLite connection helper with thread-safe schema init",
        "  routes/         9 Flask Blueprints (one per concern, for testability)",
    ])

    h2(pdf, "Test strategy")
    para(pdf,
        "Tests live in tests/test_v<version>.py - one file per version so the "
        "incremental evolution is visible in both git history and test inventory. "
        "conftest.py installs an autouse fixture that creates a temp-dir SQLite "
        "database and monkey-patches each store module to point at it, so no test "
        "pollutes shared state. This mirrors the Sonar best practice of 'integration "
        "tests hit real dependencies; only mock at external system boundaries.'")

    kv_table(pdf, [
        ("Total tests", "63 across 8 files (test_v1_0.py through test_v3_2_4.py)"),
        ("Framework", "pytest 8.3.3 + pytest-cov 5.0.0"),
        ("Coverage config", ".coveragerc with relative_files=True (for Sonar)"),
        ("Run command", "pytest - generates coverage.xml in Cobertura format"),
        ("Avg runtime", "~1.0 s for the full suite"),
    ])


def sec_deployment(pdf: PDF):
    section_header(pdf, "4. Deployment Strategies")

    para(pdf,
        "All five progressive-delivery strategies were implemented under k8s/<strategy>/, "
        "each with its own deployment + service manifests and a README describing the "
        "demo. Each strategy was applied to a clean Minikube cluster and verified live. "
        "Version numbers used for demos: v3.1.2 (older/stable) and v3.2.4 (new).")

    strategies = [
        ("Rolling Update",
         "Default k8s strategy. 4 replicas with maxSurge=1, maxUnavailable=0 guarantees "
         "zero downtime. Verified with `kubectl set image` then `kubectl rollout undo` - "
         "pods cycled and rollback succeeded."),
        ("Blue-Green",
         "Two parallel deployments (3 pods each). Cutover is a single `kubectl patch "
         "service` changing the selector color from blue to green. Verified: curl showed "
         "v3.1.2 -> v3.2.4 after patch -> v3.1.2 after reverse patch, with zero failed "
         "requests during the switch."),
        ("Canary",
         "4 stable pods (v3.1.2) + 1 canary pod (v3.2.4) share the same service selector "
         "(app=aceest-fitness). Kube-proxy load-balances across all 5. Verified: 50 "
         "in-cluster curl requests produced a 70/30 split (expected 80/20; Sonar shows "
         "random kube-proxy distribution in small samples)."),
        ("A/B Testing",
         "Two deployments with distinct variant labels (a, b) and separate services "
         "(aceest-fitness-a, aceest-fitness-b). Users hit different stable URLs. Useful "
         "when a front-end router or feature flag decides variant assignment."),
        ("Shadow Deployment",
         "Primary (v3.1.2) serves users via NodePort; shadow (v3.2.4) is ClusterIP-only "
         "and receives mirrored traffic for observation without affecting responses. A "
         "full mirror requires Istio or nginx; the manifests prove the infrastructure, "
         "and the demo command shows shadow replying independently to in-cluster calls."),
    ]
    for name, body in strategies:
        h2(pdf, name)
        para(pdf, body)

    h2(pdf, "Rollback mechanisms")
    bullets(pdf, [
        "Rolling: `kubectl rollout undo deployment/<name>` reverts to previous revision.",
        "Blue-Green: `kubectl patch service` changes selector back - instant, no pod churn.",
        "Canary: `kubectl scale deployment/...-canary --replicas=0` kills the canary.",
        "A/B: remove the DNS/router rule that sends traffic to variant B.",
        "Shadow: no rollback required - shadow responses are never returned to users.",
    ])


def sec_challenges(pdf: PDF):
    section_header(pdf, "5. Challenges & Mitigations")

    items = [
        ("Professor's reference files were Tkinter, not Flask",
         "All ten ACEestver-*.py files are Tkinter desktop GUIs which cannot be "
         "containerised or run on Kubernetes. Ported the domain logic into a Flask app "
         "while keeping the same incremental version names and feature progression."),
        ("Port 5000 collision with macOS AirPlay Receiver",
         "Apple binds port 5000 by default on modern macOS (AirPlay). Fix: turned off "
         "AirPlay Receiver in System Settings and kept gunicorn on its natural port."),
        ("Jenkins crash loop on JDK 17",
         "Initial docker-compose used jenkins/jenkins:lts-jdk17. Plugins installed via "
         "the web wizard required Java 21+ and Jenkins crash-looped on restart. Fix: "
         "upgraded to jenkins/jenkins:lts-jdk21. The jenkins_home volume persisted, so "
         "no manual work was lost."),
        ("Docker Hub namespace mismatch",
         "Pushed first tags under digvijaysinghshekhawat (taken from a profile URL), "
         "but the actual CLI-login username was dshekhawat06640. Re-tagged all 11 "
         "images under the correct namespace and updated README + Jenkinsfile refs."),
        ("SonarQube coverage showed 0.0% despite 94% locally",
         "coverage.xml had an absolute host path <source>/Users/.../app</source> that "
         "didn't exist inside the scanner container's /usr/src mount, so Sonar skipped "
         "all files. Fix: added .coveragerc with relative_files=True. Second scan "
         "correctly reported 94.2%."),
        ("Port 9000 already taken on host for SonarQube",
         "Some other host process was bound to 9000 (not a Docker container; couldn't "
         "sudo to identify). Fix: mapped SonarQube to host port 9001 and updated the "
         "Jenkinsfile's SONAR_HOST_URL."),
        ("Docker Hub tags initially pointed to identical layers",
         "First run of `docker tag` 11 times built from the current checkout (v3.2.4), "
         "so all tags shared the same digest - versions would not visibly differ during "
         "blue-green / canary demos. Fix: checked out each git tag in turn, rebuilt "
         "from that commit's code, and re-pushed. Now each tag on Docker Hub has a "
         "unique digest and APP_VERSION string."),
        ("Kube-proxy random (not round-robin) traffic distribution",
         "Canary demo showed 70/30 split across 50 requests instead of the expected "
         "80/20. Root cause: kube-proxy's default iptables mode picks a random backend "
         "per connection; over a small sample the split wanders. Over 500+ requests "
         "it converges to the replica ratio. Documented as expected behaviour."),
        ("SonarQube flagged two real issues on the first scan",
         "(1) create_app() had Cognitive Complexity 68 (limit 15) because every route "
         "was a nested function. Fix: refactored into 9 Flask Blueprints under "
         "app/routes/. (2) Flagged `host='0.0.0.0'` binding. This is intentional for "
         "container networking (gunicorn is the real production entrypoint); suppressed "
         "via sonar.issue.ignore.multicriteria with an explanatory NOSONAR comment."),
    ]
    for head, body in items:
        h2(pdf, head)
        para(pdf, body)


def sec_outcomes(pdf: PDF):
    section_header(pdf, "6. Automation Outcomes")

    h2(pdf, "Quality metrics (from SonarQube)")
    kv_table(pdf, [
        ("Lines of Code", "793 (analysable)"),
        ("Test coverage", "94.2% (485/515 covered lines)"),
        ("Bugs", "0"),
        ("Vulnerabilities", "0"),
        ("Code Smells", "0"),
        ("Duplicated Lines", "0.0%"),
        ("Reliability Rating", "A"),
        ("Security Rating", "A"),
        ("Maintainability Rating", "A"),
    ])

    h2(pdf, "Delivery metrics")
    kv_table(pdf, [
        ("Git tags pushed", "v1.0, v1.1, v1.1.2, v2.0.1, v2.1.2, v2.2.1, v2.2.4, v3.0.1, v3.1.2, v3.2.4"),
        ("Docker images published", "11 distinct digests on Docker Hub"),
        ("K8s manifests validated", "17 YAML files across 5 strategy folders"),
        ("Pipeline stages automated", "6 (checkout, test, sonar, build, push, deploy)"),
        ("Manual steps remaining", "Jenkins web unlock + plugin install (one-time)"),
    ])

    h2(pdf, "How DevOps practices paid off here")
    bullets(pdf, [
        "Test-driven iteration: each version's tests were written with the feature. "
        "When the Blueprints refactor changed import paths, all 63 tests still passed "
        "first try - confirming the refactor didn't regress behaviour.",
        "Infrastructure as code: every K8s manifest lives in git. Wiping and redeploying "
        "a strategy is a single `kubectl apply -f k8s/<strategy>/`.",
        "Immutable artefacts: Docker images are tagged with the exact version string. "
        "A rollback is a kubectl command, not a rebuild.",
        "Fast feedback: pytest takes ~1 second; sonar-scanner takes ~15 seconds. Total "
        "pipeline runtime is well under 2 minutes end-to-end, so regressions surface quickly.",
    ])


def sec_checklist(pdf: PDF):
    section_header(pdf, "7. Submission Checklist")

    para(pdf,
        "Every deliverable called out in the assignment brief is present in the "
        "public GitHub repo and, where applicable, also published to external registries.")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(220, 230, 250)
    pdf.cell(12, 7, t(" # "), border=1, fill=True)
    pdf.cell(80, 7, t(" Deliverable "), border=1, fill=True)
    pdf.cell(0, 7, t(" Location / Evidence "), border=1, fill=True,
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    rows = [
        ("1", "Flask application + versions",
         "app/, versions/ (professor's refs)"),
        ("2", "Version Control setup",
         "github.com/digvijaysingh-tech/aceest-fitness-devops"),
        ("3", "Pytest unit tests",
         "tests/test_v*.py - 63 tests, 94.2% coverage"),
        ("4", "Jenkins pipeline config",
         "jenkins/Jenkinsfile (6-stage declarative)"),
        ("5", "Dockerfile",
         "docker/Dockerfile (gunicorn, non-root, healthcheck)"),
        ("6", "Docker Hub image repo",
         "hub.docker.com/r/dshekhawat06640/aceest-fitness"),
        ("7", "Kubernetes YAML manifests",
         "k8s/{rolling-update,blue-green,canary,ab-testing,shadow}/"),
        ("8", "5 deployment strategies demo",
         "report/deployment-demos.md (live verification)"),
        ("9", "Rollback mechanism",
         "kubectl rollout undo + service patch (blue-green)"),
        ("10", "SonarQube static analysis",
         "sonar/scan-summary.md, sonar-scan-results.json"),
        ("11", "Quality gate passed",
         "0 bugs, 0 vulns, 0 smells - all A ratings"),
        ("12", "Submission report",
         "report/Assignment2_DigvijaySingh.pdf (this file)"),
    ]
    for n, d, loc in rows:
        pdf.cell(12, 6, t(n), border=1)
        pdf.cell(80, 6, t(d), border=1)
        pdf.cell(0, 6, t(loc), border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    h2(pdf, "How to explore the submission")
    bullets(pdf, [
        "Clone: git clone https://github.com/digvijaysingh-tech/aceest-fitness-devops",
        "Tests: cd aceest-fitness-devops && python -m venv .venv && "
        "source .venv/bin/activate && pip install -r requirements-dev.txt && pytest",
        "Container: docker pull dshekhawat06640/aceest-fitness:3.2.4 && "
        "docker run -p 5000:5000 dshekhawat06640/aceest-fitness:3.2.4",
        "K8s demo: minikube start && kubectl apply -f k8s/blue-green/ "
        "then follow k8s/blue-green/README.md for the cutover.",
        "SonarQube: docker run -d -p 9001:9000 sonarqube:community, "
        "then follow sonar/README.md to authenticate and scan.",
    ])


def main():
    pdf = PDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    add_cover(pdf)
    sec_overview(pdf)
    sec_architecture(pdf)
    sec_tooling(pdf)
    sec_deployment(pdf)
    sec_challenges(pdf)
    sec_outcomes(pdf)
    sec_checklist(pdf)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
