import re

from models import Job


# Temporary filter switches. These can be changed later without touching the
# connector or email logic.
INCLUDE_STUDENT_ROLES = True
INCLUDE_NEW_GRAD_ROLES = False
INCLUDE_US_LOCATIONS = False


# Internship or co-op terms must appear in the job title.
INTERNSHIP_PATTERNS = [
    r"\bintern\b",
    r"\binternships?\b",
    r"\bco[\s-]?op\b",
]


STUDENT_ROLE_PATTERNS = [
    r"\bstudent developer\b",
    r"\bstudent engineer\b",
    r"\bstudent researcher\b",
    r"\bstudent opportunities\b",
    r"\b(?:contract student worker|student contract worker|student worker)\b",
]


NEW_GRAD_PATTERNS = [
    r"\bnew grad(?:uate)?\b",
    r"\bcollege grad(?:uate)?\b",
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
    r"\bbusiness intelligence\b",
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
    r"\btechnical\b",
    r"\bcopilot\b",
    r"\bquality assurance\b",
    r"\bqa\b",
    r"\bresearch engineer\b",
    r"\bresearch scientist\b",
    r"\bcomputer science\b",
    r"\bmobile\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bembedded\b",
    r"\bfirmware\b",
    r"\bcompiler\b",
    r"\bplatform\b",
    r"\binfrastructure\b",
    r"\bnetworks?\b",
]


# Reject clearly non-technical roles
EXCLUDED_TITLE_PATTERNS = [
    r"\bmarketing\b",
    r"\bproduct marketing\b",
    r"\bproduct management\b",
    r"\bproduct manager\b",
    r"\bproduct specialist\b",
    r"\brecruiter\b",
    r"\brecruiting\b",
    r"\btalent acquisition\b",
    r"\bhuman resources\b",
    r"\bhr\b",
    r"\bsales\b",
    r"\baccounting\b",
    r"\baudit\b",
    r"\btax\b",
    r"\bcpa\b",
    r"\bactuarial\b",
    r"\btechnology risk\b",
    r"\bgovernance,? risk and compliance\b",
    r"\bfinance\b",
    r"\bfinancial\b",
    r"\bbanker\b",
    r"\bbanking\b",
    r"\bmortgage\b",
    r"\bsecuritization\b",
    r"\bcredit risk\b",
    r"\bbusiness development\b",
    r"\bbusiness analyst\b",
    r"\b(?:business|sales|people|revenue|marketing) operations\b",
    r"\bcommunications\b",
    r"\blegal\b",
    r"\bcustomer success\b",
    r"\bgraphic design\b",
    r"\bproduct design(?:er)?\b",
    r"\bdeployment strategist\b",
    r"\bcontent\b",
    r"\bconsulting\b",
    r"\bstrategy\b",
    r"\bdeal advisory\b",
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
    "americas",
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
    "alabama",
    "alaska",
    "arizona",
    "arkansas",
    "colorado",
    "connecticut",
    "delaware",
    "florida",
    "hawaii",
    "idaho",
    "indiana",
    "iowa",
    "kansas",
    "kentucky",
    "louisiana",
    "maine",
    "maryland",
    "michigan",
    "minnesota",
    "mississippi",
    "missouri",
    "montana",
    "nebraska",
    "nevada",
    "new hampshire",
    "new jersey",
    "new mexico",
    "north carolina",
    "north dakota",
    "ohio",
    "oklahoma",
    "pennsylvania",
    "rhode island",
    "south carolina",
    "south dakota",
    "tennessee",
    "utah",
    "vermont",
    "virginia",
    "west virginia",
    "wisconsin",
    "wyoming",
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

    # Greenhouse may abbreviate the Dutch province Noord-Holland as NH,
    # which otherwise collides with the US abbreviation for New Hampshire.
    if re.search(
        r"(?:^|;\s*)(?:amsterdam|haarlem|hilversum|hoofddorp|alkmaar),\s*nh(?:;|$)",
        normalized_location,
    ):
        return False

    # An explicit ISO country suffix takes precedence over ambiguous
    # city/region names such as Victoria, Australia.
    country_suffix = re.search(
        r",\s*([a-z]{3})$",
        normalized_location,
    )
    if country_suffix:
        return country_suffix.group(1) in {"can", "usa"}

    # Explicit foreign country names take precedence over state/province
    # words embedded earlier in the location, such as Baja California.
    if re.search(
        r",\s*(?:mexico|israel)$",
        normalized_location,
    ):
        return False

    # SuccessFactors may abbreviate Slovakia as SK, which otherwise looks
    # like Saskatchewan. Slovak postcodes use a numeric "123 45" format.
    if re.search(r",\s*sk,\s*\d{3}\s+\d{2}$", normalized_location):
        return False

    # Some ATS feeds return ISO alpha-2 country codes. Reject a bare
    # foreign code, or a foreign suffix that cannot be a Canadian
    # province or US state.
    alpha_two_suffix = re.search(
        r"(?:^|[,;]\s*)([a-z]{2})$",
        normalized_location,
    )
    if alpha_two_suffix:
        code = alpha_two_suffix.group(1)
        north_american_region_codes = {
            "ab", "ak", "al", "ar", "az", "bc", "ca", "co", "ct",
            "dc", "de", "fl", "ga", "hi", "ia", "id", "il", "in",
            "ks", "ky", "la", "ma", "mb", "md", "me", "mi", "mn",
            "mo", "ms", "mt", "nb", "nc", "nd", "ne", "nh", "nj",
            "nl", "nm", "ns", "nt", "nu", "nv", "ny", "oh", "ok",
            "on", "or", "pa", "pe", "qc", "ri", "sc", "sd", "sk",
            "tn", "tx", "ut", "va", "vt", "wa", "wi", "wv", "wy",
            "yt",
        }
        if normalized_location == code:
            return code in {"ca", "us"}
        if code in {"ca", "us"}:
            return True
        if code not in north_american_region_codes:
            return False

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


def is_canadian_location(location: str | None) -> bool:
    """Return whether a location is clearly in Canada."""
    if not location:
        return False

    normalized_location = location.strip().lower()

    # Explicit ISO country suffixes take precedence over ambiguous names.
    country_suffix = re.search(r",\s*([a-z]{3})$", normalized_location)
    if country_suffix:
        return country_suffix.group(1) == "can"

    # Do not mistake Slovakia's SK code and postcode for Saskatchewan.
    if re.search(r",\s*sk,\s*\d{3}\s+\d{2}$", normalized_location):
        return False

    has_canadian_name = any(
        value in normalized_location
        for value in CANADA_LOCATIONS
    )
    has_canadian_province = bool(CANADA_PROVINCE_PATTERN.search(location))

    alpha_two_suffix = re.search(
        r"(?:^|[,;]\s*)([a-z]{2})$",
        normalized_location,
    )
    if alpha_two_suffix:
        code = alpha_two_suffix.group(1)
        if code == "us":
            return False
        if code == "ca":
            # A trailing CA normally means California unless another part of
            # the location clearly identifies Canada.
            return (
                normalized_location == "ca"
                or has_canadian_name
                or has_canadian_province
            )

    if has_canadian_name or has_canadian_province:
        return True

    return False


def is_relevant_job(job: Job) -> bool:
    title = job.title.strip()
    technical_text = " ".join(
        value
        for value in (title, job.description or "")
        if value
    )

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

    eligible_role_patterns = list(INTERNSHIP_PATTERNS)
    if INCLUDE_STUDENT_ROLES:
        eligible_role_patterns.extend(STUDENT_ROLE_PATTERNS)
    if INCLUDE_NEW_GRAD_ROLES:
        eligible_role_patterns.extend(NEW_GRAD_PATTERNS)

    # Require enabled early-career wording in the title.
    if not matches_any_pattern(
        title,
        eligible_role_patterns,
    ):
        return False

    # Require a technical term in the title
    if not matches_any_pattern(
        technical_text,
        TECH_TITLE_PATTERNS,
    ):
        return False

    # Canada-only is the temporary default; US roles can be restored with the
    # switch at the top of this file.
    location_is_allowed = is_canadian_location(job.location)
    if INCLUDE_US_LOCATIONS:
        location_is_allowed = is_canada_or_us_location(job.location)
    if not location_is_allowed:
        return False

    return True
