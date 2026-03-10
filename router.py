from prompts import PROMPTS
from classifier import client

def route_and_respond(message:str,intent_data:dict):
    intent=intent_data.get("intent")
    confidence=intent_data.get("confidence")
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
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    return response.text
