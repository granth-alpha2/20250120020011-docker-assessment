# FestPass Docker assessment

Three-tier FestPass registration app (Nginx, Flask, PostgreSQL), with a hardened backend image and a Docker Hub release.

## Assessment details

- Name: Granth Chauhan
- REGNO: `20250120020011`
- PORT: `8080`
- Docker Hub user: `granthaplha2`
- Docker Hub repository: <https://hub.docker.com/r/granthaplha2/fest-backend>

## Run locally

1. Copy `.env.example` to `.env`.
2. Set `REGNO` to your actual registration number and `DB_PASSWORD` to a strong password.
3. Run `docker compose up --build -d` and open `http://localhost:8080` (or your configured port).
4. Stop the stack with `docker compose down`. The named PostgreSQL volume keeps registrations when the stack is restarted; `docker compose down -v` deletes it.

The frontend and backend share the `edge` network; only the backend and database share the internal `data` network. The database is not published to the host. Compose waits for PostgreSQL's health check before starting the backend.

## Backend image

The backend image uses a version-pinned Alpine Python base, pinned Python dependencies, and a non-root runtime user. Build and scan it with:

```powershell
docker build --build-arg APP_VERSION=0.2 -t fest-backend:0.2 .\backend
trivy image fest-backend:0.2
trivy image --severity CRITICAL --ignore-unfixed --exit-code 1 fest-backend:0.2
```

The release tags required by the assessment are `granthaplha2/fest-backend:1.0.0` and `granthaplha2/fest-backend:1.0`. Publish only after building with `APP_VERSION=1.0.0`, scanning, and signing the image by digest.

## AI tools

Copilot SDK in VS Code was used to inspect the assessment, implement the app and container configuration, and help validate the work.

## Vulnerability comparison

| Image | CRITICAL | HIGH | Image size |
|---|---:|---:|---:|
| `fest-backend:0.1` (before fixes) | 234 | 2,249 | 129 MB |
| `fest-backend:0.2` (after fixes) | 0 | 0 | 112 MB |

Counts are from the saved Trivy 0.68.2 reports; the before report has separate OS and Python package totals. The fixed image also passes `trivy image --severity CRITICAL --ignore-unfixed --exit-code 1 fest-backend:0.2` with exit code 0. See `reports/`.

## Evidence and remaining submission work

Save unedited assessment screenshots under `screenshots/`, using the assessment evidence codes in their filenames. Do not claim a step is complete until its actual output or screenshot has been saved.

- Set REGNO and PORT to the values assigned to you; capture the required terminal and browser evidence.
- Install and run Trivy; save the baseline and fixed-image scan reports and confirm the fixed image passes the required critical-vulnerability check.
- Build and push both release tags to the public Docker Hub repository, record the pushed digest, and capture the repository Tags page.
- Generate a password-protected Cosign key pair, commit only `cosign.pub`, sign the `1.0.0` image by digest, verify it, and show that verification rejects the unsigned `1.0.1` image.
- Commit each completed assessment stage and push the final repository before the deadline. The final push and submission-portal step remain for the repository owner.
