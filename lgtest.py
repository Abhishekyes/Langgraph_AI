import os
import logging
import requests
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.memory.buffer import ConversationBufferMemory
from langgraph.graph import StateGraph, END
from langchain.llms.base import LLM

load_dotenv()
TOKEN = os.getenv("EURON_API_TOKEN")
if not TOKEN:
    raise EnvironmentError("Missing EURON_API_TOKEN in .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("interaction_log.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MODEL_CATALOG = {
    "gpt-4.1-nano": "creative content",
    "gpt-4.1-mini": "lightweight creative",
    "llama-3.3-70b": "deep reasoning",
    "llama-4-scout": "fast factual",
    "llama-4-maverick": "multimodal",
    "deepseek-r1-distilled": "code / logic",
    "gemini-2.5-pro-exp": "professional",
    "gemini-2.0-flash": "fast answers",
    "gemini-2.0-flash-001": "enhanced flash",
    "qwen-qwq-32b": "dialogue",
    "mistral-saba-24b": "summarization"
}

SIMILAR_MODELS = {
    "gpt-4.1-nano": ["gpt-4.1-mini"],
    "gpt-4.1-mini": ["gpt-4.1-nano"],
    "llama-3.3-70b": ["llama-4-scout"],
    "llama-4-scout": ["llama-3.3-70b"],
    "llama-4-maverick": ["qwen-qwq-32b"],
    "deepseek-r1-distilled": ["gemini-2.0-flash"],
    "gemini-2.5-pro-exp": ["gemini-2.0-flash-exp"],
    "gemini-2.0-flash": ["gemini-2.0-flash-001"],
    "qwen-qwq-32b": ["llama-4-maverick"],
    "mistral-saba-24b": ["gpt-4.1-mini"]
}

def select_model(prompt: str) -> str:
    prompt = prompt.lower()
    if any(word in prompt for word in ["poem", "story", "creative"]):
        return "gpt-4.1-nano"
    if any(word in prompt for word in ["quick", "fast", "simple"]):
        return "gemini-2.0-flash"
    if any(word in prompt for word in ["summarize", "rewrite"]):
        return "mistral-saba-24b"
    if any(word in prompt for word in ["code", "debug", "logic"]):
        return "deepseek-r1-distilled"
    if any(word in prompt for word in ["image", "multimodal"]):
        return "llama-4-maverick"
    if any(word in prompt for word in ["compare", "analyze"]):
        return "llama-3.3-70b"
    if any(word in prompt for word in ["conversation", "chat"]):
        return "qwen-qwq-32b"
    if any(word in prompt for word in ["professional", "business"]):
        return "gemini-2.5-pro-exp"
    if any(word in prompt for word in ["scout", "brief"]):
        return "llama-4-scout"
    return "gpt-4.1-mini"

class EuronLLM(LLM, BaseModel):
    api_url: str = "https://api.euron.one/api/v1/euri/alpha/chat/completions"
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    token: str = Field(default_factory=lambda: os.getenv("EURON_API_TOKEN"))

    @property
    def _llm_type(self) -> str:
        return "euron_custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        selected_model = self.model or select_model(prompt)
        attempted_models = [selected_model] + SIMILAR_MODELS.get(selected_model, [])
        logger.info(f"Trying models in order: {attempted_models}")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        for model in attempted_models:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            for attempt in range(3):
                try:
                    logger.info(f"Attempt {attempt + 1} with model: {model}")
                    response = requests.post(self.api_url, headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    content = (
                        data.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                        .strip()
                    )
                    if content:
                        logger.info(f"✅ Success using model: {model}")
                        self.model = model
                        return content
                    logger.warning("Empty content received. Retrying...")
                except Exception as e:
                    logger.error(f"❌ Attempt {attempt + 1} failed with model {model}: {e}")
        return "[Failed after trying all similar models]"

def build_graph():
    memory = ConversationBufferMemory(return_messages=True)

    def model_selector_node(state: dict):
        state["model"] = select_model(state["prompt"])
        return state

    def llm_call_node(state: dict):
        llm = EuronLLM(model=state["model"])
        prompt = PromptTemplate.from_template("{input}")
        chain = prompt | llm
        result = chain.invoke({"input": state["prompt"]})
        state["response"] = result
        state["model"] = llm.model
        state["memory"] = memory
        return state

    workflow = StateGraph(state_schema=dict)
    workflow.add_node("select_model", RunnableLambda(model_selector_node))
    workflow.add_node("call_llm", RunnableLambda(llm_call_node))
    workflow.set_entry_point("select_model")
    workflow.add_edge("select_model", "call_llm")
    workflow.add_edge("call_llm", END)

    return workflow.compile(), memory

if __name__ == "__main__":
    app, memory = build_graph()

    while True:
        user_input = input("🧠 Enter your prompt (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            print("👋 Conversation ended.")
            break
        if not user_input:
            continue

        result = app.invoke({"prompt": user_input})
        response_text = result.get("response", {}).get("text") or result.get("response", "[No response text]")

        logger.info(f"Prompt: {user_input} | Model: {result.get('model')} | Response: {response_text}")

        print("\n📊 Prompt Summary")
        print("────────────────────────────")
        print(f"🧠 Prompt      : {user_input}")
        print(f"🤖 Model Used  : {result.get('model')}")
        print("────────────────────────────")
        print("🗨️ Response")
        print("────────────────────────────")
        print(response_text)
        print("────────────────────────────")
