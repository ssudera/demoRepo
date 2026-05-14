# Groq API Setup Guide for LangChain Demo

This guide explains how to create and configure a **Groq API key** and
use it with a simple **LangChain LLM demo** in Google Colab.

The goal is to run a working LLM example quickly with minimal setup.

------------------------------------------------------------------------

# 1. Prerequisites

Before starting, make sure you have:

-   A Google account
-   Access to Google Colab
-   A web browser
-   Basic familiarity with Python

------------------------------------------------------------------------

# 2. Create a Groq Account

1.  Open the Groq developer console in your browser.

https://console.groq.com

2.  Click **Sign Up**.

3.  You can register using:

    -   Google login
    -   GitHub login
    -   Email + password

4.  Once registered, log in to the console.

------------------------------------------------------------------------

# 3. Generate a Groq API Key

After logging in:

1.  Navigate to the **API Keys** section.

2.  Click **Create API Key**.

3.  A new key will be generated.

Example key format:

    gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

4.  Copy the key and store it safely.

⚠️ Important: Treat the API key like a password. Do not share it
publicly.

------------------------------------------------------------------------

# 4. Open Google Colab

Open Google Colab:

https://colab.research.google.com

Create a **New Notebook**.

Rename the notebook:

    groq_langchain_demo.ipynb

------------------------------------------------------------------------

# 5. Install Required Libraries

Run the following command in the **first Colab cell**.

``` python
!pip install -q langchain langchain-groq
```

This installs:

-   LangChain framework
-   Groq integration package

------------------------------------------------------------------------

# 6. Add Your Groq API Key in Code

Paste your API key directly inside the notebook.

Example:

``` python
import os

os.environ["GROQ_API_KEY"] = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxx"
```

------------------------------------------------------------------------

# 7. Initialize the Groq Model

Create a LangChain LLM instance.

``` python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)
```

Recommended models:

-   llama-3.1-8b-instant (fastest)
-   llama-3.1-70b-versatile
-   mixtral-8x7b-32768

------------------------------------------------------------------------

# 8. Run Your First Prompt

Now test the model.

``` python
prompt = "Write a short email requesting leave from my manager."

response = llm.invoke(prompt)

print(response.content)
```

If everything is configured correctly, you should see a generated email.

------------------------------------------------------------------------

# 9. Example Full Demo Script

``` python
!pip install -q langchain langchain-groq

import os
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "gsk_xxxxxxxxxxxxxxxxx"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

prompt = "Write an email to my supervisor requesting leave."

response = llm.invoke(prompt)

print(response.content)
```

------------------------------------------------------------------------

##. Troubleshooting

## Invalid API Key

Ensure:

-   The key begins with `gsk_`
-   There are no extra spaces
-   The key is copied correctly

------------------------------------------------------------------------

## Module Not Found Error

Run the install command again:

    !pip install langchain langchain-groq

------------------------------------------------------------------------

## Rate Limits

If you hit rate limits:

-   Wait a few seconds
-   Retry the request

------------------------------------------------------------------------

