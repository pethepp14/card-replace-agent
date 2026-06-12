from typing import Dict

from app.agent.tools import classify_issue_tool, create_case_tool, validate_request_tool


def classify_issue(state: Dict) -> Dict:
    classification = classify_issue_tool(state.get("user_input", ""))

    collected_info = dict(state.get("collected_info", {}))
    if classification.get("card_last4"):
        collected_info["card_last4"] = classification["card_last4"]

    issue_type = classification.get("issue_type", "unknown")
    missing_fields = []

    if not collected_info.get("card_last4"):
        missing_fields.append("card_last4")

    if issue_type == "stolen" and not collected_info.get("police_report"):
        missing_fields.append("police_report")

    state["issue_type"] = issue_type
    state["collected_info"] = collected_info
    state["missing_fields"] = missing_fields
    state["tool_results"] = {"classification": classification}
    state["status"] = "collecting" if missing_fields else "ready_to_submit"
    state["conversation_history"] = state.get("conversation_history", []) + [
        f"Detected issue type: {issue_type}"
    ]

    if missing_fields:
        state["final_response"] = (
            "I can help with that. Please share the last 4 digits of the card and, if this is a stolen card, confirm whether a police report is available."
        )
    return state


def collect_missing_fields(state: Dict) -> Dict:
    missing_fields = state.get("missing_fields", [])
    if "card_last4" in missing_fields:
        state["final_response"] = "Please provide the last 4 digits of the card to continue."
    elif "police_report" in missing_fields:
        state["final_response"] = "For a stolen card, please confirm whether a police report was filed."
    else:
        state["final_response"] = "I have the information needed to continue."

    state["status"] = "collecting"
    return state


def validate_request(state: Dict) -> Dict:
    validation = validate_request_tool(state.get("issue_type", "unknown"), state.get("collected_info", {}))
    state["tool_results"] = {**state.get("tool_results", {}), "validation": validation}

    if validation["is_valid"]:
        state["status"] = "ready_to_submit"
        state["final_response"] = validation["message"]
    else:
        state["status"] = "needs_follow_up"
        state["final_response"] = validation["message"]

    return state


def finalize_case(state: Dict) -> Dict:
    case = create_case_tool(state.get("issue_type", "unknown"), state.get("collected_info", {}))
    state["case_id"] = case["case_id"]
    state["status"] = "completed"
    state["final_response"] = case["message"]
    state["tool_results"] = {**state.get("tool_results", {}), "case": case}
    return state
