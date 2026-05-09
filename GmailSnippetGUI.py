import pandas as pd
import os
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )

    # Change redirect_uri to 'urn:ietf:wg:oauth:2.0:oob' for out-of-band flow
    # This is suitable for environments like Colab where a local web server
    # cannot easily receive redirects.
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

    # Manual Authorization Flow for headless environments
    # 1. Get the authorization URL
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    print(f"Please go to this URL and authorize access:\n{auth_url}\n")

    # 2. Prompt user to paste the authorization code
    # The user should copy the *code* from the success page in their browser.
    authorization_code = input(
        "After authorizing, you will see an authorization code. Paste it here:\n"
    ).strip()

    # 3. Exchange the authorization code for credentials
    # Use the 'code' parameter with the authorization_code directly.
    flow.fetch_token(code=authorization_code)
    creds = flow.credentials

    return build("gmail", "v1", credentials=creds)

service = gmail_service()

# -----------------------------
# List the latest 10 emails
# -----------------------------
results = service.users().messages().list(userId="me", maxResults=10).execute()
messages = results.get("messages", [])

for msg in messages:
    m = service.users().messages().get(userId="me", id=msg["id"]).execute()
    print("ID:", msg["id"])
    print("Snippet:", m.get("snippet"))
    print("-" * 40)

## Fetch Message and display

def get_header_value(headers, name):
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return 'N/A'

# num_messages_to_fetch = int(input("Enter the number of latest messages you want to list: "))
num_messages_to_fetch = 50
# List the latest N emails
results = service.users().messages().list(userId="me", maxResults=num_messages_to_fetch).execute()
messages_raw = results.get("messages", [])

message_data = []

for msg_raw in messages_raw:
    # Get full message details
    msg = service.users().messages().get(userId="me", id=msg_raw["id"]).execute()

    # Extract sender and subject from headers
    headers = msg['payload']['headers']
    sender = get_header_value(headers, 'From')
    subject = get_header_value(headers, 'Subject')

    message_data.append({
        'Sender': sender,
        'Subject': subject,
        'Snippet': msg.get('snippet', 'No snippet available')
    })

# Create a pandas DataFrame and display it
df_messages = pd.DataFrame(message_data)
display(df_messages)
