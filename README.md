# Mont Blanc Reservation Page Monitor

This Python script monitors the Mont Blanc reservation pages and sends an email notification whenever any of the pages change.

---

## Features

* Monitors multiple URLs simultaneously.
* Detects any change in the full page content.
* Sends email notifications to multiple recipients.
* **Deployment confirmation email** - Sends an email on startup to confirm the scraper is running.
* **Daily heartbeat email** - Sends a daily status email after 7 AM to confirm the scraper is still alive.
* **Enhanced terminal output** - Shows page content preview and change detection status.
* Configurable check interval via environment variable.
* Easy setup using a `.env` file.
* Can be tested locally using a local HTML file.
* **Fly.io deployment ready** - Includes Dockerfile and fly.toml for cloud deployment.

---

## Requirements

* Python 3.7 or higher
* Packages: `requests`, `python-dotenv`

Install required packages:

```bash
pip install requests python-dotenv
```

---

## Setup

### 1. Clone the repository or download the script

### 2. Create a `.env` file

Create a file named `.env` in the project folder with the following content:

```env
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_APP_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
RECIPIENTS=friend1@gmail.com,friend2@gmail.com
CHECK_INTERVAL_SECONDS=300
```

* `EMAIL_ADDRESS` → your Gmail address.
* `EMAIL_APP_PASSWORD` → Gmail App Password (see instructions below).
* `SMTP_SERVER` → usually `smtp.gmail.com` for Gmail.
* `SMTP_PORT` → usually `587` for Gmail.
* `RECIPIENTS` → comma-separated list of emails to notify.
* `CHECK_INTERVAL_SECONDS` → interval between checks in seconds (default: 300 = 5 minutes).

---

### 3. Generate a Gmail App Password

1. Enable 2-Step Verification in your Google account.
2. Go to **Security > App passwords**.
3. Create a new App password for **Mail** and your device (e.g., name it `MontBlancNotifier`).
4. Copy the password and use it as `EMAIL_APP_PASSWORD` in your `.env` file.

---

### 4. Configure URLs

In `monitor_montblanc.py`, edit the URLs to monitor:

```python
URLS = [
    "https://montblanc.ffcam.fr/index.php?&_lang=GB&&_lang=GB",
    "https://montblanc.ffcam.fr/GB_home.html"
]
```

* Add or remove URLs as needed.
* Adjust `CHECK_INTERVAL_SECONDS` in your `.env` file to change how often pages are checked.

---

### 5. Run the script

From the terminal, run:

```bash
python monitor_montblanc.py
```

* On first run, the script captures the initial state of all pages.
* **A deployment confirmation email will be sent immediately.**
* It will check the pages every `CHECK_INTERVAL_SECONDS` seconds.
* **A daily heartbeat email will be sent after 7 AM** to confirm the scraper is still running.
* If any page changes, an email will be sent listing the changed pages.
* The terminal will display page content previews and change detection status.

---

## Testing the script

To safely test without waiting for the Mont Blanc pages to change:

1. Create a local HTML file, e.g., `MontBlanc.html`.
2. Start a local HTTP server in the folder containing the file:

```bash
python -m http.server 8000
```

3. Change the URL in `URLS` to:

```python
URLS = ["http://localhost:8000/MontBlanc.html"]
```

4. Run the script. Edit the HTML file to trigger a change and check that an email is received.

---

## Notes

* The script only sends one email per detected change.
* For real Mont Blanc monitoring, a 5-minute interval is recommended.
* Ensure `.env` is **never shared publicly**.
* You can safely revoke your Gmail App Password anytime.

---

## Email Types

The scraper sends three types of emails:

1. **"Mont Blanc Scraper - Successfully Deployed"**
   - Sent immediately when the scraper starts
   - Confirms successful deployment
   - Lists all monitored URLs and check interval

2. **"Mont Blanc Scraper - Daily Heartbeat"**
   - Sent once per day after 7 AM
   - Confirms the scraper is still alive and running
   - Includes current time and configuration details

3. **"Mont Blanc Reservation Page Update"**
   - Sent whenever any monitored page changes
   - Lists which pages have changed
   - Only sent once per detected change

---

## Fly.io Deployment

This project is configured for deployment to Fly.io as a background worker.

### Prerequisites
```bash
# Install Fly.io CLI
curl -L https://fly.io/install.sh | sh

# Authenticate
flyctl auth login
```

### Deploy
```bash
# Create the app
flyctl apps create montblanc-scraper

# Set secrets
flyctl secrets set \
  EMAIL_ADDRESS="your-email@gmail.com" \
  EMAIL_APP_PASSWORD="your-gmail-app-password" \
  SMTP_SERVER="smtp.gmail.com" \
  SMTP_PORT="587" \
  RECIPIENTS="recipient1@email.com,recipient2@email.com" \
  CHECK_INTERVAL_SECONDS="300"

# Deploy
flyctl deploy

# View logs
flyctl logs
```

The scraper will run continuously on Fly.io, checking pages at the configured interval and sending emails as needed.

---

## Optional Improvements

* Persist the last page state to disk to survive script restarts.
* Add a log file to track changes over time.
* Integrate Telegram notifications as an alternative to email.
* Customize detection logic for specific keywords if desired.

---

## Author

* Generated by ChatGPT for monitoring Mont Blanc reservation pages.
