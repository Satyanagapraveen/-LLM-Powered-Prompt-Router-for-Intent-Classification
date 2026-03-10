import json


def log_route(intent_data, user_message, final_response):
    """
    Logs the routing decision and final response to a JSONL file.
    """

    log_entry = {
        "intent": intent_data.get("intent"),
        "confidence": intent_data.get("confidence"),
        "user_message": user_message,
        "final_response": final_response
    }

    with open("route_log.jsonl", "a") as file:
        file.write(json.dumps(log_entry) + "\n")