from __future__ import annotations

import html
import smtplib
import ssl
from email.message import EmailMessage

from config import ALERT_EMAIL, SMTP_EMAIL, SMTP_PASSWORD
from models import Job


class EmailService:
    def __init__(self) -> None:
        # Gmail account used to send notifications
        self.smtp_email = SMTP_EMAIL
        self.smtp_password = SMTP_PASSWORD
        self.recipient = ALERT_EMAIL

    def send_job_alert(self, job: Job) -> None:
        # Escape values used inside the HTML email
        safe_company = html.escape(job.company)
        safe_title = html.escape(job.title)
        safe_location = html.escape(job.location or "Not specified")
        safe_url = html.escape(job.url, quote=True)

        # Create the email
        message = EmailMessage()
        message["From"] = self.smtp_email
        message["To"] = self.recipient
        message["Subject"] = (
            f"New Internship - {job.company} - {job.title}"
        )

        # Plain text version
        message.set_content(
            f"""
New internship posting found

Company: {job.company}
Position: {job.title}
Location: {job.location or "Not specified"}

Apply here:
{job.url}
            """.strip()
        )

        # HTML version
        message.add_alternative(
            f"""
            <html>
                <body>
                    <h2>{safe_title}</h2>

                    <p>
                        <strong>Company:</strong> {safe_company}
                    </p>

                    <p>
                        <strong>Location:</strong> {safe_location}
                    </p>

                    <p>
                        <a href="{safe_url}">
                            View Job Posting
                        </a>
                    </p>

                    <hr>

                    <p style="color:gray;">
                        Sent automatically by Internship Job Monitor
                    </p>

                </body>
            </html>
            """,
            subtype="html",
        )

        # Send through Gmail
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            context=context,
            timeout=30,
        ) as server:
            server.login(
                self.smtp_email,
                self.smtp_password,
            )

            server.send_message(message)