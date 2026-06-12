import os

from flask import Flask, jsonify, request

from app.agent.graph import app_graph

app = Flask(__name__)


@app.get("/")
def health():
    return jsonify({"status": "ok", "message": "Card replacement LangGraph agent is ready."})


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message", "")

    result = app_graph.invoke({
        "user_input": user_input,
        "collected_info": {},
        "conversation_history": [],
    })

    return jsonify({"response": result.get("final_response", ""), "state": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True, host="0.0.0.0", port=port)
