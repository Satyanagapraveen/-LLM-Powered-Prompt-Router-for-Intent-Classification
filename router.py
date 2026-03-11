from prompts import PROMPTS
from classifier import client
from logger import log_route

CONFIDENCE_THRESHOLD = 0.7
def route_and_respond(message:str,intent_data:dict):
    intent=intent_data.get("intent")
    confidence=intent_data.get("confidence")
    if confidence is None or confidence < CONFIDENCE_THRESHOLD:
        intent = "unclear"
    if intent == "unclear":
        return (
            "I'm not sure what kind of help you're looking for. "
            "Are you asking about coding, data analysis, writing improvement, "
            "or career advice?"
        )
    system_prompt=PROMPTS.get("intent")
    full_prompt=f"""
    {system_prompt}
    user message:
    {message}
   """
    response=client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=full_prompt
    )
    final_response = response.text
    log_route(intent_data, message, final_response)
    return final_response