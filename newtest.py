import time
import csv
from datetime import datetime
from pathlib import Path
from lgtest import build_graph

TEST_CASES = [
    "Write a short story about a robot falling in love with a human.",
    "What's the capital of Argentina?",
    "Write a formal email to schedule a performance review.",
    "Summarize this: Artificial Intelligence is transforming industries.",
    "Fix this Python code: for i in range(5) print(i)",
    "Pretend you're Iron Man chatting with Captain America.",
    "Analyze the economic impact of AI in healthcare.",
    "Describe an image of a lion wearing sunglasses surfing a wave.",
    "Generate a REST API in Flask to manage products in an inventory.",
    "Explain the difference between SQL JOIN types with examples.",
    "Write a Dockerfile to deploy a FastAPI app with Uvicorn.",
    "Give me a shell script to monitor disk usage and alert if over 80%.",
    "Draft a project status update email for a delayed software sprint.",
    "Write a professional resume summary for a Python backend developer.",
    "Generate Python unit tests for a login function with pytest.",
    "Write an SQL query to get the top 5 products with the highest sales last month."
]

def run_tests():
    app, _ = build_graph()
    output_path = Path("model_test_results.csv")

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Test#", "Prompt", "Model Used", "Response (First 300 chars)", "Status", "Timestamp"])

        print("\n🚀 Running Full Model Functionality Test...\n")

        for i, prompt in enumerate(TEST_CASES, 1):
            print(f"🔹 Test {i}: {prompt}")
            try:
                result = app.invoke({"prompt": prompt})
                model_used = result.get("model", "Unknown")
                response = result.get("response", "[No response text]").replace("\n", " ").replace("\r", "")
                short_response = response[:300] + ("..." if len(response) > 300 else "")
                status = "✅ Success"
            except Exception as e:
                model_used = "ERROR"
                short_response = str(e).replace("\n", " ")
                status = "❌ Failed"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([i, prompt, model_used, short_response, status, timestamp])
            file.flush()

            print(f"🤖 Model Used: {model_used}")
            print(f"🗨️  Response : {short_response}")
            print("────────────────────────────────────────────")
            time.sleep(1)

if __name__ == "__main__":
    run_tests()
