import random
import re


ISSUE_KEYWORDS = {
    "stolen": ["stolen", "lost", "taken", "missing"],
    "damaged": ["damaged", "broken", "cracked", "melted", "bent", "damaged card"],
    "broken": ["broken", "chip", "strip", "not working", "unreadable"],
}


def classify_issue_tool(user_input: str) -> dict:
    text = user_input.lower()

    if any(keyword in text for keyword in ISSUE_KEYWORDS["stolen"]):
        issue_type = "stolen"
    elif any(keyword in text for keyword in ISSUE_KEYWORDS["damaged"]):
        issue_type = "damaged"
    else:
        issue_type = "broken" if "broken" in text or "damaged" in text else "unknown"

    last4 = re.search(r"\b(\d{4})\b", user_input)

    return {
        "issue_type": issue_type,
        "card_last4": last4.group(1) if last4 else None,
        "confidence": 0.82 if issue_type != "unknown" else 0.42,
    }


def validate_request_tool(issue_type: str, collected_info: dict) -> dict:
    is_valid = True
    issues = []

    if issue_type == "stolen" and not collected_info.get("police_report"):
        is_valid = False
        issues.append("Please confirm whether a police report is available for the stolen card.")

    if not collected_info.get("card_last4"):
        is_valid = False
        issues.append("Please provide the last 4 digits of the card.")

    if not is_valid:
        return {"is_valid": False, "message": " ".join(issues), "issues": issues}

    return {
        "is_valid": True,
        "message": f"The replacement request looks ready for a {issue_type} card case.",
        "issues": [],
    }


def create_case_tool(issue_type: str, collected_info: dict) -> dict:
    case_id = f"CR-{random.randint(1000, 9999)}"
    return {
        "case_id": case_id,
        "status": "created",
        "message": (
            f"Case {case_id} has been prepared for a {issue_type} card replacement request. "
            f"We will use the provided details: last 4 digits {collected_info.get('card_last4', '****')}"
        ),
    }
