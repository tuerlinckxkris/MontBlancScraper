import os
import time
import requests
from dotenv import load_dotenv
import smtplib
from datetime import datetime, time as dt_time

load_dotenv()

# List all websites you want to monitor
URLS = [
    "https://montblanc.ffcam.fr/index.php?&_lang=GB&&_lang=GB",
    "https://montblanc.ffcam.fr/GB_home.html"
]

CHECK_INTERVAL_SECONDS = os.getenv("CHECK_INTERVAL_SECONDS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
RECIPIENTS = os.getenv("RECIPIENTS").split(",")


def fetch_page(url):
    """Download the full page content as a string."""
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.text


def send_email(subject, body):
    """Send an email with the given subject and body."""
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENTS, message)


def send_change_notification(changed_urls):
    """Send notification when pages change."""
    subject = "Mont Blanc Reservation Page Update"
    body = "The following Mont Blanc pages have changed:\n\n"
    for url in changed_urls:
        body += f"- {url}\n"
    body += "\nCheck them immediately!"
    send_email(subject, body)


def send_deployment_confirmation():
    """Send email to confirm successful deployment."""
    subject = "Mont Blanc Scraper - Successfully Deployed"
    body = (
        "The Mont Blanc scraper has been successfully deployed and is now running.\n\n"
        f"Monitoring {len(URLS)} URL(s):\n"
    )
    for url in URLS:
        body += f"- {url}\n"
    body += f"\nCheck interval: Every {CHECK_INTERVAL_SECONDS // 60} minutes\n"
    body += f"Deployment time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    send_email(subject, body)


def send_heartbeat():
    """Send daily heartbeat email to confirm scraper is still alive."""
    subject = "Mont Blanc Scraper - Daily Heartbeat"
    body = (
        "This is your daily confirmation that the Mont Blanc scraper is still running.\n\n"
        f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        f"Monitoring {len(URLS)} URL(s)\n"
        f"Check interval: Every {CHECK_INTERVAL_SECONDS // 60} minutes\n\n"
        "The scraper is healthy and actively monitoring for changes."
    )
    send_email(subject, body)


def main():
    print("Mont Blanc multi-page monitor started...")
    last_states = {}
    last_heartbeat_date = None

    # Initialize the states
    for url in URLS:
        last_states[url] = fetch_page(url)
    print("Initial pages captured.")

    # Send deployment confirmation email
    try:
        send_deployment_confirmation()
        print("Deployment confirmation email sent.")
    except Exception as e:
        print(f"Failed to send deployment confirmation: {e}")

    while True:
        try:
            current_time = datetime.now()
            current_date = current_time.date()
            current_hour = current_time.hour

            # Send daily heartbeat after 7 AM if not sent today
            if current_hour >= 7 and last_heartbeat_date != current_date:
                try:
                    send_heartbeat()
                    last_heartbeat_date = current_date
                    print(f"Daily heartbeat sent at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                except Exception as e:
                    print(f"Failed to send heartbeat: {e}")

            # Check for page changes
            changed_urls = []
            print("Checking pages.")
            for url in URLS:
                print(f"\n{'='*80}")
                print(f"URL: {url}")
                current_state = fetch_page(url)
                print(f"Content length: {len(current_state)} characters")
                print(f"Preview (first 500 chars):")
                print(f"{current_state[:500]}...")
                print(f"{'='*80}\n")

                if current_state != last_states[url]:
                    changed_urls.append(url)
                    last_states[url] = current_state
                    print(f"⚠️  CHANGE DETECTED on {url}")
                else:
                    print(f"✓ No changes detected")

            if changed_urls:
                send_change_notification(changed_urls)
                print(f"Changes detected on: {changed_urls}, sending Email")

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
