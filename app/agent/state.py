from typing import Dict, List, Optional, TypedDict


class AgentState(TypedDict, total=False):
    user_input: str
    issue_type: str
    collected_info: Dict[str, str]
    missing_fields: List[str]
    status: str
    conversation_history: List[str]
    tool_results: Dict[str, object]
    final_response: str
    case_id: Optional[str]
