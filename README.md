# AI Chat App
## End-to-End DevSecOps CI/CD Pipeline

An AI Chat Application created using Flask, with an end-to-end CI/CD + DevSecOps pipeline built entirely using GitHub Actions.

The app communicates with Groq's OpenAI-compatible chat completions API using the `llama-3.3-70b-versatile` model.

## Project structure

```text
ai-chat-app/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── gunicorn.conf.py
├── requirements.txt
├── templates/
│   └── index.html
├── .github/
│   └── workflows/
│       ├── code-quality.yml
│       ├── dependency-scan.yml
│       ├── deploy-to-server.yml
│       ├── devsecops-pipeline.yml
│       ├── docker-build-push.yml
│       ├── docker-lint.yml
│       ├── image-scan.yml
│       └── secrets-scan.yml
└── README.md
```


## Why this repo exists

This project demonstrates a security-first deployment flow for a simple AI chat service:

- Enforced code quality with linting and static analysis
- Dependency vulnerability scanning
- Dockerfile validation and container image scanning
- Secrets detection in repository history
- Secure production deployment through GitHub Actions and SSH

## DevSecOps Pipeline

```
push to main
    ├── Code Quality ──── flake8 + bandit SAST (matrix: 3.11–3.13)
    ├── Secrets Scan ──── gitleaks (full git history)
    ├── Dependency Scan ─ pip-audit (package CVEs)
    ├── Docker Lint ───── hadolint (Dockerfile best practices)
    └── Tests ─────────── pytest (route tests)
            │ (all five must pass)
            ▼
        Docker Build & Push ── build image, push to Docker Hub
            │
            ▼
        Image Scan ─────────── Trivy (CRITICAL + HIGH CVEs)
            │
            ▼
        Deploy to Server ───── SSH into EC2, docker compose up
```

The root pipeline is `devsecops-pipeline.yml`. On `push` to `main`, it executes all the following workflows.

| Workflow | Purpose | Key tools |
|---|---|---|
| `code-quality.yml` | Validate code style and application security | `flake8`, `bandit` |
| `dependency-scan.yml` | Scan Python dependencies for vulnerabilities | `pip-audit` |
| `docker-lint.yml` | Validate Dockerfile best practices | `hadolint` |
| `docker-build-push.yml` | Build and push Docker image to Docker Hub | `docker/build-push-action` |
| `image-scan.yml` | Scan container image for CVEs | `trivy` |
| `secrets-scan.yml` | Detect exposed secrets in Git history | `gitleaks` |
| `deploy-to-server.yml` | Deploy the app to production via SSH | `appleboy/ssh-action`, `docker compose` |

### Workflow Summary

1. `code-quality.yml` runs linting and static analysis across supported Python versions (`3.11`, `3.12`, `3.13`).
2. `secrets-scan.yml` performs GitLeaks scanning with full history.
3. `dependency-scan.yml` checks dependencies against known vulnerabilities.
4. `docker-lint.yml` validates the Dockerfile.
5. `docker-build-push.yml` builds and pushes the Docker image to Docker Hub.
6. `image-scan.yml` scans the image for high/critical vulnerabilities.
7. `deploy-to-server.yml` deploys only after all prior stages pass.

## Getting Started

1. Fork this repo.
2. Set up secrets — go to repo **Settings → Secrets and Variables → Actions**:
   - Secret: `GROQ_API_KEY` (your Groq API Key, Create a key on www.groq.com > console > API Keys)
   - Secret: `DOCKERHUB_TOKEN` (your Docker Hub access token)
   - Secret: `EC2_SSH_HOST`, `EC2_SSH_USER`, `EC2_SSH_PRIVATE_KEY` (for server deploy)
   - Secret: `GITLEAKS_LICENSE` (for gitleaks action)
   - Variable: `DOCKERHUB_USER` (your Docker Hub username)
3. Push to `main` — the DevSecOps pipeline triggers automatically.

> Note: `deploy` and `image-scan` jobs will fail until you configure your own server and Docker Hub secrets. This is expected — the CI jobs (`code-quality`, `dependency-scan`, `docker-lint`, `secrets-scan`) will work out of the box.

4. Try manual triggers — go to the Actions tab → pick a workflow → Run workflow.
5. Read each workflow file — they are commented for learning.

## Dependencies

This app is intentionally minimal to keep the security baseline small.

- `Flask` — web framework
- `requests` — HTTP client
- `gunicorn` — production WSGI server
- `python-dotenv` — environment variable loader for local development
- `flake8` — Python linting
- `bandit` — Python security static analysis

## Notes

- The application sends chat requests to `https://api.groq.com/openai/v1/chat/completions`.

- Security checks are enforced before any deployment step.

<br/>

---

**Aayush Madan**
- **Email**: aayush.madan4611@gmail.com
- **LinkedIn**: [http://www.linkedin.com/in/aayush-madan-devops](http://www.linkedin.com/in/aayush-madan-devops)
