# build-your-first-ai-agent-workshop
# Google Colab Setup

## 1. Prerequisites

Before starting, ensure you have:

-   A Google account
-   Access to Google Colab
-   A Gemini API Key

## 2. Generate a Free Gemini API Key

1.  Open Google AI Studio\
    https://aistudio.google.com

2.  Click **Get API Key**

3.  Create a new API key.

4.  Copy the key.

Example:

    AIzaSyxxxxxxxxxxxxxxxx

## 3. Open Google Colab

Open:

https://colab.research.google.com

Create a **new notebook**.

Rename it:

    talk_to_llm.ipynb

## 4. Install Required Libraries

Run this in the **first Colab cell**.

``` python
!pip install -q langchain langchain_core langchain-google-genai
```

This installs:

-   LangChain
-   Langchain Core
-   Gemini integration package
