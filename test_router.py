from router import route_and_respond
from classifier import classify_intent

message="How do I sort a list in python"
intent=classify_intent(message)
response=route_and_respond(
    message,intent
)
print("Intent:",intent)
print("Response:\n")
print(response)