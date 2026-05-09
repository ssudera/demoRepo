import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd

# Assuming 'service' object is already authenticated and available from previous cells.
# If 'service' is not defined, please run the Gmail authentication cell first.

def get_header_value(headers, name):
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return 'N/A'

# Create widgets
num_messages_input = widgets.IntText(
    value=10,
    description='Number of Messages:',
    disabled=False,
    min=1,
    max=100
)

fetch_button = widgets.Button(
    description='Fetch Emails',
    button_style='success',
    tooltip='Click to fetch emails'
)

output_area = widgets.Output()

def on_fetch_button_clicked(b):
    with output_area:
        clear_output()
        num_to_fetch = num_messages_input.value
        print(f"Fetching {num_to_fetch} latest messages...")

        try:
            results = service.users().messages().list(userId="me", maxResults=num_to_fetch).execute()
            messages_raw = results.get("messages", [])

            message_data = []

            if not messages_raw:
                print("No messages found.")
                return

            for msg_raw in messages_raw:
                msg = service.users().messages().get(userId="me", id=msg_raw["id"]).execute()
                headers = msg['payload']['headers']
                sender = get_header_value(headers, 'From')
                subject = get_header_value(headers, 'Subject')

                message_data.append({
                    'Sender': sender,
                    'Subject': subject,
                    'Snippet': msg.get('snippet', 'No snippet available')
                })

            df_messages_ui = pd.DataFrame(message_data)
            display(df_messages_ui)
            print(f"Successfully fetched and displayed {len(df_messages_ui)} messages.")

        except Exception as e:
            print(f"An error occurred: {e}")

# Attach the event handler to the button
fetch_button.on_click(on_fetch_button_clicked)

# Display the widgets
display(num_messages_input, fetch_button, output_area)
