import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import pandas as pd
import datetime
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://router.huggingface.co/v1",
    #api_key="Your LLM KEY",
    model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
    max_tokens=500
)


# Assuming 'service' object is already authenticated and available from previous cells.
# If 'service' is not defined, please run the Gmail authentication cell first.

def get_header_value(headers, name):
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return 'N/A'

# Create widgets

pagination_Header = widgets.HTML(
    value="<h2 style='text-align: center; color: #1a73e8; font-family: sans-serif;'>📧 Gmail Snippet Fetcher: Your Email Quick View</h2>",
    placeholder='',
    description='',
)
pagination_select = widgets.Dropdown(
    options=[10,15,20,25, 50, 100],
    value=10,
    description='Show Messages:',
    disabled=False,
)

category_select = widgets.Dropdown(
    options=['All', 'Primary', 'Social', 'Updates', 'Promotions', 'Forums'],
    value='All',
    description='Category:',
    disabled=False,
)

start_date_picker = widgets.DatePicker(
    description='Start Date',
    disabled=False,
    value=datetime.date.today() - datetime.timedelta(days=7) # Default to 7 days ago
)

end_date_picker = widgets.DatePicker(
    description='End Date',
    disabled=False,
    value=datetime.date.today() # Default to today
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
        num_to_fetch = pagination_select.value
        selected_category = category_select.value
        start_date = start_date_picker.value
        end_date = end_date_picker.value

        query_parts = []
        if selected_category != 'All':
            query_parts.append(f"category:{selected_category.lower()}")
        
        if start_date:
            query_parts.append(f"after:{start_date.strftime('%Y/%m/%d')}")
        if end_date:
            # Gmail API 'before' is exclusive, so add one day to include the entire end_date
            exclusive_end_date = end_date + datetime.timedelta(days=1)
            query_parts.append(f"before:{exclusive_end_date.strftime('%Y/%m/%d')}")

        query = ' '.join(query_parts)

        print(f"Fetching {num_to_fetch} latest messages from category: {selected_category}, between {start_date} and {end_date}...")

        try:
            results = service.users().messages().list(userId="me", maxResults=num_to_fetch, q=query).execute()
            messages_raw = results.get("messages", [])

            message_data = []

            if not messages_raw:
                print("No messages found.")
                return

            for msg_raw in messages_raw:
                msg = service.users().messages().get(userId="me", id=msg_raw["id"]).execute()
                headers = msg['payload']['headers']
                # sender = get_header_value(headers, 'From')
                # subject = get_header_value(headers, 'Subject')

                message_data.append({
                    # 'Sender': sender,
                    # 'Subject': subject,
                    'Gmail Summary': msg.get('snippet', 'No snippet available') # Renamed header
                })

            df_messages_ui = pd.DataFrame(message_data)

            # Add vertical scroll if more than 20 records
            # if len(df_messages_ui) >= 20:
            #     display(HTML(df_messages_ui.to_html().replace('<thead>', '<thead style="text-align: left;">').replace('<th>', '<th style="text-align: left;">') + '<style>table {width: 100%; border-collapse: collapse;}'
            #                    'th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}'
            #                    'th {background-color: #f2f2f2;}</style>'))
            #     display(HTML(f'<div style="max-height: 400px; overflow-y: auto;">{df_messages_ui.to_html(index=False)}</div>'))
            # else:
            #     display(df_messages_ui)

            print(f"Successfully fetched and displayed {len(df_messages_ui)} messages.")

            # Summarization logic using the LLM
            if 'llm' in globals(): # Check if llm is globally available
                print("\n--- AI Summaries of Fetched Emails ---")
                summaries_list = []
                for idx, summary_text in enumerate(df_messages_ui['Gmail Summary']):
                    # Limit the input to LLM to avoid token limits for very long snippets
                    short_summary_text = summary_text[:1000] # Take first 1000 characters
                    try:
                        # Assuming llm is a ChatGoogleGenerativeAI instance from an earlier cell.
                        llm_response = llm.invoke(
                            f"Summarize the following email snippet in a concise sentence:\n{short_summary_text}"
                        )
                        summaries_list.append(f"{idx + 1}. {llm_response.content}")
                    except Exception as llm_e:
                        summaries_list.append(f"{idx + 1}. Error summarizing: {llm_e}")
                
                for summary_item in summaries_list:
                    print(summary_item)
            else:
                print("LLM not available for summarization. Please ensure the LLM initialization cell is run.")

        except Exception as e:
            print(f"An error occurred: {e}")

# Attach the event handler to the button
fetch_button.on_click(on_fetch_button_clicked)

# Display the widgets
display(pagination_Header,pagination_select, category_select, start_date_picker, end_date_picker, fetch_button, output_area)
