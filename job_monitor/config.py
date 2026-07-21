import os

from dotenv import load_dotenv


# Load values from the .env file
load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"{name} is missing from .env")

    return value


# Database settings
DATABASE_URL = get_required_env("DATABASE_URL")

# Gmail settings
SMTP_EMAIL = get_required_env("SMTP_EMAIL")
SMTP_PASSWORD = get_required_env("SMTP_PASSWORD")
ALERT_EMAIL = get_required_env("ALERT_EMAIL")

# Monitor settings
REQUEST_TIMEOUT_SECONDS = int(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "30")
)

SEND_EXISTING_ON_FIRST_RUN = (
    os.getenv("SEND_EXISTING_ON_FIRST_RUN", "false").lower()
    == "true"
)