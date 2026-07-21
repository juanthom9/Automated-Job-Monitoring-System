from emailer import EmailService
from models import Job


def main() -> None:
    # Create a fake internship
    job = Job(
        external_id="test-job",
        company="Google",
        title="Software Engineer Intern",
        url="https://careers.google.com",
        location="Toronto",
    )

    # Send the email
    email_service = EmailService()
    email_service.send_job_alert(job)

    print("Test email sent successfully.")


if __name__ == "__main__":
    main()