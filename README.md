# 🚀 EURI LangGraph AI – Prompt-Aware Model Evaluation Framework

> **Author:** Abhishek
> **Role:** Data Scientist | ML Engineer | Automation Specialist  
> **Contact:** vvabhi2776@gmail.com  
> **GitHub:** [github.com/Abhishekyes](https://github.com/Abhishekyes)

---

## 📌 Overview

**EURI LangGraph AI** is a minimal, intelligent, and fully-automated framework that uses **LangGraph** and **LangChain** to dynamically route prompts to the best model from a custom API (Euron), retry intelligently, and log structured results for benchmarking or QA purposes.

This project demonstrates real-world usage of LLM orchestration with fallback logic, logging, and prompt-aware decision-making — all in just **2 Python files**.

---

## 📁 Project Structure

```bash
📦 euri-langgraph-ai/
├── lgtest.py             # LangGraph-based prompt router and LLM logic
├── newtest.py            # Batch runner to test multiple prompts and save to CSV
├── .env                  # Stores Euron API token
└── README.md             # Project documentation


## ⚙️ Key Features

✅ **Prompt-Aware Model Routing**  
→ Selects the best-suited model based on prompt type.

✅ **Retry Logic with Similar Models**  
→ Retries using fallback models if the response is empty or an error occurs.

✅ **CSV-Based Logging**  
→ Automatically stores results with model name, status, timestamp, and trimmed response.

✅ **Minimalistic and Clean**  
→ Only two files needed to run the full stack: one for routing, one for testing.

✅ **Interactive + Batch Modes**  
→ Supports both one-by-one manual prompt testing and automated prompt suite testing.

✅ **Logs All Activity**  
→ Everything is written to both terminal and `interaction_log.txt`.

---

## 🔧 Technologies Used

| Library / Tool    | Purpose                                       |
|-------------------|-----------------------------------------------|
| **Python 3.12+**   | Core programming language                     |
| **langgraph**      | Graph-based state control flow                |
| **langchain**      | Prompt templating and LLM chaining            |
| **dotenv**         | Secure token management                       |
| **requests**       | API communication with Euron endpoint         |
| **pydantic**       | Model validation for custom LLM interface     |
| **csv**            | Log structured results for test output        |
| **logging**        | Tracks system logs (file + console)           |

---

## 🧠 Prompt Routing Logic

Each prompt is evaluated for keywords and routed to the best-matched model:

| Keyword(s)              | Routed Model            | Use Case Example                          |
|--------------------------|--------------------------|--------------------------------------------|
| `"story"`, `"poem"`      | `gpt-4.1-nano`           | Creative generation                        |
| `"fast"`, `"quick"`      | `gemini-2.0-flash`       | Quick facts, summaries                     |
| `"summarize"`, `"rewrite"` | `mistral-saba-24b`     | Document or article summarization          |
| `"debug"`, `"code"`      | `deepseek-r1-distilled`  | Programming and logic prompts              |
| `"professional"`, `"email"` | `gemini-2.5-pro-exp` | Business/professional communications       |
| `"chat"`, `"conversation"` | `qwen-qwq-32b`         | Character dialogues or roleplays           |
| `"image"`, `"visual"`    | `llama-4-maverick`       | Image descriptions and visual prompts      |
| **Fallback/Default**     | `gpt-4.1-mini`           | Default lightweight responder              |

---

## 📊 CSV Output Sample

> File: `model_test_results.csv`

| Test# | Prompt                          | Model Used      | Response (First 300 chars)       | Status      | Timestamp              |
|-------|----------------------------------|------------------|----------------------------------|-------------|-------------------------|
| 1     | Write a story about a robot     | gpt-4.1-nano     | Once upon a time...              | ✅ Success  | 2025-04-20 16:42:46     |
| 2     | What’s the capital of Argentina?| gpt-4.1-mini     | The capital is Buenos Aires.     | ✅ Success  | 2025-04-20 16:42:49     |

---

## 🚀 How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/euri-langgraph-ai.git
cd euri-langgraph-ai

2️⃣ Set Up Environment
Create a .env file in the project root with your Euron API token:

env
Copy
Edit
EURON_API_TOKEN=your_actual_token_here
⚠️ Never commit your .env file — keep it secret!

3️⃣ Install Required Libraries
Install all required packages using pip:

bash
Copy
Edit
pip install langgraph langchain python-dotenv pydantic requests
4️⃣ Run Interactive Prompt Mode
bash
Copy
Edit
python lgtest.py
This will allow you to type prompts manually in the terminal. The best model is selected and the response is shown instantly.

5️⃣ Run Batch Prompt Testing
bash
Copy
Edit
python newtest.py
This script will:

Run predefined prompts

Use model routing and retry logic

Save results to model_test_results.csv

🧩 Unique Advantages
✅ Just 2 files power the full system
✅ Fully model-agnostic routing and fallback
✅ CSV logging for reporting and QA
✅ Terminal-based or batch execution
✅ Easy to scale into an API or SaaS tool

🔐 Security
🔒 Your API key is stored safely in .env

⚠️ Ensure .env is added to .gitignore to avoid leaking credentials

📈 Potential Add-ons
 Add FastAPI or Flask API endpoints

 Add a user feedback column to the CSV

 Add support for OpenAI, Claude, or Mistral

 Visualize model routing with LangGraph UI

 Integrate with Slack/Telegram as a chatbot

👨‍💻 Author
Abhishek V.
📧 vvabhi2776@gmail.com
🔗 GitHub – abhishek-vv
💼 Data Scientist | ML & Cloud Developer

