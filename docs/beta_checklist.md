# Beta readiness checklist

## Security
- [ ] MIRACLE_SECRET_KEY is set to a long random value
- [ ] MIRACLE_ENV=staging (or production when ready)
- [ ] MIRACLE_SESSION_SECURE=true if HTTPS is enabled
- [ ] Beta whitelist is populated

## Access and accounts
- [ ] Test a new account registration
- [ ] Test login with a non-whitelisted email (should fail)
- [ ] Test password reset flow if available

## Data and backups
- [ ] Run a manual backup using scripts/backup_db.ps1
- [ ] Configure automated backups (Task Scheduler)
- [ ] Verify backup files are created in data/backups

## App behavior
- [ ] Verify feedback form submission
- [ ] Verify onboarding page loads
- [ ] Run a short smoke test: fiches, ministeres, quiz, stats

## Operations
- [ ] Capture the full env used for beta
- [ ] Keep a changelog for beta fixes
