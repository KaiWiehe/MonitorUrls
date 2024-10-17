import smtplib
import requests
import certifi
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    smtp_server, smtp_port, smtp_user, smtp_password, to_address, subject, body
):
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Debug-Level aktivieren
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_address, msg.as_string())
        server.quit()
        print(f"[INFO] E-Mail an {to_address} gesendet.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERROR] Authentifizierungsfehler: {e}")
    except smtplib.SMTPConnectError as e:
        print(f"[ERROR] Verbindungsfehler: {e}")
    except Exception as e:
        print(f"[ERROR] Allgemeiner Fehler beim Senden der E-Mail: {e}")


def check_url(url):
    try:
        response = requests.get(url, timeout=10, verify=certifi.where())
        if response.status_code == 200:
            print(f"[INFO] URL {url} erfolgreich erreicht.")
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"[WARN] URL {url} nicht erreichbar: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Monitor URLs und sende E-Mails bei Nichterreichbarkeit."
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        required=True,
        help="Liste von URLs, die überwacht werden sollen",
    )
    parser.add_argument("--smtp_server", required=True, help="SMTP-Server-Adresse")
    parser.add_argument(
        "--smtp_port", type=int, default=587, help="SMTP-Server-Port (Standard: 587)"
    )
    parser.add_argument("--smtp_user", required=True, help="SMTP-Benutzername")
    parser.add_argument("--smtp_password", required=True, help="SMTP-Passwort")
    parser.add_argument(
        "--to_address", required=True, help="E-Mail-Adresse des Empfängers"
    )

    args = parser.parse_args()

    for url in args.urls:
        if not check_url(url):
            subject = f"[ALERT] URL nicht erreichbar: {url}"
            body = (
                f"Die URL {url} ist nicht erreichbar. Bitte überprüfen Sie den Dienst."
            )
            send_email(
                args.smtp_server,
                args.smtp_port,
                args.smtp_user,
                args.smtp_password,
                args.to_address,
                subject,
                body,
            )


if __name__ == "__main__":
    main()
