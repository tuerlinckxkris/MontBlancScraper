import os
import time
import requests
from dotenv import load_dotenv
import smtplib

load_dotenv()

# List all websites you want to monitor
URLS = [
    "https://montblanc.ffcam.fr/index.php?&_lang=GB&&_lang=GB",
    "https://montblanc.ffcam.fr/GB_home.html"
]

CHECK_INTERVAL = 300  # 5 minutes

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


def send_email(changed_urls):
    subject = "Mont Blanc Reservation Page Update"
    body = "The following Mont Blanc pages have changed:\n\n"
    for url in changed_urls:
        body += f"- {url}\n"
    body += "\nCheck them immediately!"

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENTS, message)


def main():
    print("Mont Blanc multi-page monitor started...")
    last_states = {}

    # Initialize the states
    for url in URLS:
        last_states[url] = fetch_page(url)
    print("Initial pages captured.")

    while True:
        try:
            changed_urls = []
            print("Checking pages.")
            for url in URLS:
                print(url)
                current_state = fetch_page(url)
                if current_state != last_states[url]:
                    changed_urls.append(url)
                    last_states[url] = current_state

            if changed_urls:
                send_email(changed_urls)
                print(f"Changes detected on: {changed_urls}, sending Email")

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
