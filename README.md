# security-bot-learning

A hands-on learning project to get comfortable with n8n, GitHub, and Python by building a GitHub-triggered security triage bot.

## What this does

When a new issue is opened on this repo, GitHub sends a webhook to a locally-running n8n instance (exposed publicly via ngrok). From there, the plan is for n8n to pull a URL out of the issue body, send it to a local Flask API for a VirusTotal scan, and post the verdict back as a comment on the issue.

## What's built so far

- **`src/triage.py`** — core script that submits a URL to VirusTotal, polls until the scan completes, and returns the verdict. Includes error handling for bad API keys and network failures.
- **`src/api.py`** — a small Flask API (`POST /scan`) that wraps `triage.py` so it can be called over HTTP instead of run as a command.
- **n8n workflow** — a GitHub webhook trigger, connected to a real repo via an ngrok tunnel. Confirmed working end-to-end: opening a GitHub issue successfully fires the workflow.
- **CI** — a GitHub Actions workflow (`.github/workflows/lint.yml`) that runs `flake8` on every push.

## Still to build

The full pipeline logic isn't wired up yet — pulling the issue body, calling the Flask API, and posting a comment back to GitHub is the next step.

## Running it locally

1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt` *(or manually: `requests python-dotenv flask`)*
3. Add a `.env` file with `VIRUSTOTAL_API_KEY=your_key_here`
4. `python src/api.py` — starts the Flask API on port 5001
5. `docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n` — starts n8n
6. `ngrok http 5678` — exposes n8n publicly so GitHub can reach it