# newtest.py (Final version - dynamic user input, unlimited prompts)

import time
import csv
from datetime import datetime
from pathlib import Path
from lgtest import build_graph

def run_tests():
    app, _ = build_graph()
    output_path = Path("model_test_results.csv")

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Test#", "Prompt", "Model Used", "Response (First 300 chars)", "Status", "Timestamp"])

        print("\n🚀 Enter prompts manually (type 'exit' to finish)...\n")
        test_counter = 1  # Start counting prompts

        while True:
            user_prompt = input(f"🧠 Enter Prompt {test_counter} (Text or Image Description): ").strip()

            if user_prompt.lower() == "exit":
                print(f"\n👋 Session Completed: {test_counter - 1} prompts tested.")
                break

            if not user_prompt:
                print("⚠️ Empty input skipped. Please type something.")
                continue

            try:
                result = app.invoke({"prompt": user_prompt})
                model_used = result.get("model", "Unknown")
                response_text = result.get("response", {}).get("text", "[No response text]")

                short_response = response_text.replace("\n", " ").replace("\r", "")[:300]
                if len(response_text) > 300:
                    short_response += "..."

                status = "✅ Success"
            except Exception as e:
                model_used = "ERROR"
                short_response = str(e).replace("\n", " ")
                status = "❌ Failed"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([test_counter, user_prompt, model_used, short_response, status, timestamp])
            file.flush()

            print(f"\n🤖 Model Used: {model_used}")
            print(f"🗨️  Response : {short_response}")
            print("────────────────────────────────────────────\n")
            time.sleep(1)

            test_counter += 1   

if __name__ == "__main__":
    run_tests()

