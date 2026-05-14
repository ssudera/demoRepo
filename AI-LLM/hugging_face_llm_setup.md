# 🤗 Hugging Face LLM Setup Guide (Free Tier)

This guide will help you set up a Hugging Face LLM using LangChain with the OpenAI-compatible router.

---

## 📌 Step 1: Create a Hugging Face Account

1. Go to: https://huggingface.co  
2. Click on Sign Up  
3. Complete registration and login  

---

## 🔑 Step 2: Generate API Key (Access Token)

1. Go to: https://huggingface.co/settings/tokens  
2. Click on "New token"  
3. Configure:
   - Name: llm-access-token  
   - Role: Read  
4. Click Generate  
5. Copy the token  

⚠️ Important: Never expose this token in public repositories.

---

## 📦 Step 3: Install Required Libraries

```bash
pip install langchain-openai python-dotenv
```

---

## 📁 Step 4: Setup Environment Variables

Create a `.env` file:

```env
HF_API_KEY=your_huggingface_token_here
```

---

## 🧠 Step 5: Choose a Free Model

Recommended models:

- openai/gpt-oss-20b  
- meta-llama/Llama-3.1-8B-Instruct  
- mistralai/Mistral-7B-Instruct-v0.3  

---

## ⚙️ Step 6: Configure LLM in Python

Create `app.py`:

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_API_KEY"),
    model="openai/gpt-oss-20b"
)

response = llm.invoke("What is the capital of France?")
print(response.content)
```

---

## ▶️ Step 7: Run the Application

```bash
python app.py
```

Expected output:

The capital of France is Paris.

---

## 🚨 Common Issues

401 Unauthorized → Check API key  
402 Payment Required → Free quota exceeded  
Model errors → Try another model  

---

## 🚀 You're Ready!

You now have a working Hugging Face LLM setup 🎉
