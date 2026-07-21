import re

from models import Job


# Internship terms must appear in the job title
INTERNSHIP_PATTERNS = [
    r"\bintern\b",
    r"\binternship\b",
    r"\bco[\s-]?op\b",
    r"\bstudent developer\b",
    r"\bstudent engineer\b",
    r"\bnew grad(?:uate)?\b",
]


# Technical terms must also appear in the title
TECH_TITLE_PATTERNS = [
    r"\bsoftware\b",
    r"\bdeveloper\b",
    r"\bdevelopment\b",
    r"\bengineer\b",
    r"\bengineering\b",
    r"\bmachine learning\b",
    r"\bartificial intelligence\b",
    r"\bai\b",
    r"\bdata science\b",
    r"\bdata scientist\b",
    r"\bdata engineer\b",
    r"\bbackend\b",
    r"\bback-end\b",
    r"\bfrontend\b",
    r"\bfront-end\b",
    r"\bfull stack\b",
    r"\bfull-stack\b",
    r"\bdevops\b",
    r"\bcloud\b",
    r"\bsecurity\b",
    r"\bcybersecurity\b",
    r"\bsystems\b",
    r"\bautomation\b",
    r"\bquality assurance\b",
    r"\bqa\b",
    r"\bresearch engineer\b",
    r"\bcomputer science\b",
    r"\bmobile\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bembedded\b",
    r"\bfirmware\b",
    r"\bcompiler\b",
    r"\bplatform\b",
    r"\binfrastructure\b",
]


# Reject clearly non-technical roles
EXCLUDED_TITLE_PATTERNS = [
    r"\bmarketing\b",
    r"\bproduct marketing\b",
    r"\brecruiter\b",
    r"\brecruiting\b",
    r"\btalent acquisition\b",
    r"\bhuman resources\b",
    r"\bhr\b",
    r"\bsales\b",
    r"\baccounting\b",
    r"\bfinance\b",
    r"\bfinancial\b",
    r"\bbusiness development\b",
    r"\bbusiness analyst\b",
    r"\boperations\b",
    r"\bcommunications\b",
    r"\blegal\b",
    r"\bcustomer success\b",
    r"\bgraphic design\b",
    r"\bcontent\b",
    r"\bconsulting\b",
    r"\bstrategy\b",
    r"\bprogram manager\b",
    r"\bproject manager\b",
    r"\bproduct manager\b",
]


# Reject senior or leadership roles
SENIOR_TITLE_PATTERNS = [
    r"\bsenior\b",
    r"\bstaff\b",
    r"\bprincipal\b",
    r"\blead\b",
    r"\bmanager\b",
    r"\bdirector\b",
    r"\barchitect\b",
    r"\bvice president\b",
    r"\bvp\b",
    r"\bhead of\b",
]


CANADA_LOCATIONS = [
    "canada",
    "remote - canada",
    "remote canada",
    "toronto",
    "mississauga",
    "brampton",
    "vancouver",
    "victoria",
    "montreal",
    "ottawa",
    "calgary",
    "edmonton",
    "waterloo",
    "kitchener",
    "hamilton",
    "markham",
    "oakville",
    "quebec",
    "halifax",
    "winnipeg",
    "saskatoon",
    "regina",
    "ontario",
    "british columbia",
    "alberta",
    "manitoba",
    "saskatchewan",
    "nova scotia",
    "new brunswick",
    "newfoundland",
    "prince edward island",
]


US_LOCATIONS = [
    "united states",
    "united states of america",
    "usa",
    "u.s.",
    "u.s.a.",
    "remote - us",
    "remote us",
    "remote - united states",
    "new york",
    "san francisco",
    "seattle",
    "boston",
    "chicago",
    "austin",
    "los angeles",
    "san diego",
    "washington, dc",
    "washington dc",
    "palo alto",
    "mountain view",
    "sunnyvale",
    "santa clara",
    "redmond",
    "bellevue",
    "atlanta",
    "dallas",
    "houston",
    "denver",
    "miami",
    "phoenix",
    "portland",
    "philadelphia",
    "california",
    "texas",
    "massachusetts",
]


CANADA_PROVINCE_PATTERN = re.compile(
    r"(?:^|,\s*)"
    r"(?:ON|BC|AB|QC|MB|SK|NS|NB|NL|PE|YT|NT|NU)"
    r"(?:,|$|\s)",
    flags=re.IGNORECASE,
)


US_STATE_PATTERN = re.compile(
    r"(?:^|,\s*)"
    r"(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|"
    r"KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|"
    r"ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)"
    r"(?:,|$|\s)",
    flags=re.IGNORECASE,
)


def matches_any_pattern(
    text: str,
    patterns: list[str],
) -> bool:
    # Check whether any regex pattern matches the text
    return any(
        re.search(pattern, text, flags=re.IGNORECASE)
        for pattern in patterns
    )


def is_canada_or_us_location(location: str | None) -> bool:
    # Reject jobs without a clear location
    if not location:
        return False

    normalized_location = location.strip().lower()

    # Match common Canadian and US location names
    if any(
        value in normalized_location
        for value in CANADA_LOCATIONS + US_LOCATIONS
    ):
        return True

    # Match province and state abbreviations
    if CANADA_PROVINCE_PATTERN.search(location):
        return True

    if US_STATE_PATTERN.search(location):
        return True

    return False


def is_relevant_job(job: Job) -> bool:
    title = job.title.strip()

    # Reject non-technical roles
    if matches_any_pattern(
        title,
        EXCLUDED_TITLE_PATTERNS,
    ):
        return False

    # Reject senior and leadership roles
    if matches_any_pattern(
        title,
        SENIOR_TITLE_PATTERNS,
    ):
        return False

    # Require internship wording in the title
    if not matches_any_pattern(
        title,
        INTERNSHIP_PATTERNS,
    ):
        return False

    # Require a technical term in the title
    if not matches_any_pattern(
        title,
        TECH_TITLE_PATTERNS,
    ):
        return False

    # Only accept Canada and US postings
    if not is_canada_or_us_location(job.location):
        return False

    return True