from app.agent.graph import app_graph


def test_graph_returns_response():
    result = app_graph.invoke({
        "user_input": "My card is broken and the last 4 digits are 4821.",
        "collected_info": {"card_last4": "4821"},
        "conversation_history": [],
    })

    assert isinstance(result, dict)
    assert "final_response" in result
