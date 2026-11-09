# JISAN Premium TCP Bot Hosting Panel

Multi-user Free Fire TCP Bot panel with Arolinks ads, ban system, 12-hour time.

## Admin
- Email: `admin@jisan.host`
- Password: `admin123`

## Run locally
```bash
pip install -r requirements.txt
python app.py
```

## Deploy on Railway

1. Push this folder to GitHub (root of repo should contain `app.py`, `Procfile`, `requirements.txt`)
2. Railway → New Project → Deploy from GitHub
3. Select the repo
4. Railway will detect Python and run Gunicorn automatically
5. After deploy, open the Railway public URL
6. Admin Panel → set **Public Panel URL** = your Railway URL  
   Example: `https://your-app.up.railway.app`
7. Save Arolinks API token

### Important for Arolinks
Public Panel URL must be the Railway HTTPS URL, not localhost.

### Notes
- Free Railway may sleep / limit CPU — bots can stop when the service sleeps
- SQLite (`panel.db`) resets if the service is redeployed (ephemeral disk)
- For 24/7 bots, a VPS is more reliable than free Railway

## Fixes in this version (Start / Stop / Restart)
- **Persistent PID tracking**: Bot PID is saved in the database. After Railway / Gunicorn restart the panel can still detect and control previously running bots.
- **Robust process killing**: Uses process groups (`start_new_session` + `killpg`) so child processes are fully terminated.
- **psutil support**: Better process alive checks (added to requirements).
- **Deadlock-free**: Uses `RLock` so status / stop / restart never hang.
- **Auto cleanup**: On start it kills any leftover zombie process from previous crashes.
- Start / Stop / Restart now work reliably even after the panel process itself restarts.
