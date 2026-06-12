from typing import Dict

from langgraph.graph import END, StateGraph

from app.agent.nodes import classify_issue, collect_missing_fields, finalize_case, validate_request
from app.agent.state import AgentState



def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_issue", classify_issue)
    workflow.add_node("collect_missing_fields", collect_missing_fields)
    workflow.add_node("validate_request", validate_request)
    workflow.add_node("finalize_case", finalize_case)

    workflow.set_entry_point("classify_issue")

    workflow.add_conditional_edges(
        "classify_issue",
        lambda state: "collect_missing_fields" if state.get("missing_fields") else "validate_request",
    )

    workflow.add_edge("collect_missing_fields", "validate_request")
    workflow.add_conditional_edges(
        "validate_request",
        lambda state: "finalize_case" if state.get("status") == "ready_to_submit" else END,
    )
    workflow.add_edge("finalize_case", END)

    return workflow.compile()


app_graph = build_graph()


if __name__ == "__main__":
    sample: Dict = {
        "user_input": "My card is stolen and the last 4 digits are 4821.",
        "collected_info": {"card_last4": "4821"},
        "conversation_history": [],
    }
    print(app_graph.invoke(sample))
