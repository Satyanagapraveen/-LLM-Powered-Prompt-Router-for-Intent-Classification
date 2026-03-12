from prompts import PROMPTS
from classifier import client
from logger import log_route

CONFIDENCE_THRESHOLD = 0.7
VALID_INTENTS = {"code", "data", "writing", "career"}
def route_and_respond(message:str,intent_data:dict):
    intent=intent_data.get("intent")
    confidence=intent_data.get("confidence")
    if message.startswith("@"):
        parts = message.split(" ", 1)
        override_intent = parts[0][1:]

        if override_intent in VALID_INTENTS:
            intent = override_intent
            confidence = 1.0
            intent_data = {"intent": intent, "confidence": confidence}
            message = parts[1] if len(parts) > 1 else ""


    if confidence is None or confidence < CONFIDENCE_THRESHOLD:
        intent = "unclear"
    if intent == "unclear":
        final_response = (
            "I'm not sure what kind of help you're looking for. "
            "Are you asking about coding, data analysis, writing improvement, "
            "or career advice?"
        )
        log_route(intent_data, message, final_response)
        return final_response
    system_prompt=PROMPTS.get(intent)
    full_prompt=f"""
    {system_prompt}
    user message:
    {message}
   """
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    final_response = response.text
    log_route(intent_data, message, final_response)
    return final_response
