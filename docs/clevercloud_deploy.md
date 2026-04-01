# Clever Cloud deployment (EU-only)

## Prerequisites
- GitHub repository connected to Clever Cloud
- Python app created on Clever Cloud (region EU)

## Required files
- requirements.txt (Flask + gunicorn)
- Procfile (start command)

## Environment variables (beta)
- MIRACLE_ENV=staging
- MIRACLE_SECRET_KEY=long-random-value
- MIRACLE_SESSION_SECURE=true
- MIRACLE_BETA_WHITELIST=you@example.com,collaborator@example.com
- MIRACLE_LOGIN_MAX_ATTEMPTS=5
- MIRACLE_LOGIN_WINDOW_SECONDS=900
- MIRACLE_REGISTER_MAX_ATTEMPTS=5
- MIRACLE_REGISTER_WINDOW_SECONDS=900
- MIRACLE_LOGIN_MAX_IPS=3
- MIRACLE_LOGIN_BAN_WINDOW_SECONDS=1800

## Start command
- gunicorn app:app

## Database persistence
- Clever Cloud filesystem is ephemeral
- Use a persistent add-on (filesystem) and set:
  - MIRACLE_DB_PATH=/path/to/persistent/miracle.db

## Deploy
- Push to GitHub
- Click Deploy in Clever Cloud
- Verify login, whitelist, and feedback form
