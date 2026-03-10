from google import genai 
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found")
client=genai.Client(api_key=api_key)

CLASSIFIER_PROMPT = """
You are an intent classification system.

Your task is to analyze the user's message and classify it into ONE of the following intents:

code – questions about programming, debugging, algorithms, or software development.

data – questions about datasets, statistics, SQL queries, numbers, or data analysis.

writing – requests for feedback on text, improving clarity, tone, or structure.

career – questions about jobs, resumes, interviews, or career advice.

unclear – if the user's intent cannot be determined.

Return ONLY a JSON object with this structure:

{
 "intent": "code | data | writing | career | unclear",
 "confidence": float between 0.0 and 1.0
}

Do not include any explanation.
Return only valid JSON.
"""
def classify_intent(message:str):
    prompt=f"""
        {CLASSIFIER_PROMPT}
    User message:
    {message}
   """
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(response.text)
    return response.text
