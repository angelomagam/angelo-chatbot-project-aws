import json
import boto3

lex_client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    try:
        # Handle GET and POST requests
        if 'httpMethod' in event:
            if event['httpMethod'] == 'GET':
                user_message = event.get('queryStringParameters', {}).get('message', '')
                session_id = event.get('queryStringParameters', {}).get('sessionId', 'default-session')
            elif event['httpMethod'] == 'POST':
                body = event.get('body', '{}')  # Ensure body isn't None
                if isinstance(body, str):  # Convert from string to dict
                    body = json.loads(body)
                user_message = body.get('message', '')
                session_id = body.get('sessionId', 'default-session')

        else:
            user_message = "Hello, how are you?"
            session_id = "test-session"

        if not user_message:
            return {"statusCode": 400, "body": json.dumps({"error": "No message provided."})}

        # Send message to Amazon Lex
        lex_response = lex_client.recognize_text(
            botId="BOT_ID", # Replace with your Bot ID
            botAliasId="ALIAS_ID", # Replace with your Bot Alias ID
            localeId="en_US",
            sessionId=session_id,
            text=user_message
        )

        # Debugging: Print full Lex response
        print("Lex Response:", json.dumps(lex_response, indent=2))

        # Extract bot response message
        bot_messages = lex_response.get('messages', [])
        if bot_messages:
            bot_response = bot_messages[0].get('content', 'I did not understand that.')
        else:
            bot_response = "I did not understand that."

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"response": bot_response, "sessionId": session_id})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
