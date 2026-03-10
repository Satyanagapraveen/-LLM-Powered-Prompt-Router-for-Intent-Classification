from classifier import classify_intent
from router import route_and_respond
def main():

    print("AI Prompt Router")
    print("Type 'exit' to quit.\n")

    while True:

        user_message = input("Enter your message: ")

        if user_message.lower() == "exit":
            break

        intent = classify_intent(user_message)

        response = route_and_respond(user_message, intent)

        print("\nDetected Intent:", intent)
        print("\nResponse:\n")
        print(response)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()