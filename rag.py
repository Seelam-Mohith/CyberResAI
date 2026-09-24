import time

import sys

from langchain_openai import ChatOpenAI

import config
from utils.retriever import get_retriever
from utils.query import optimize_query
from prompt import build_qa_prompt

def get_llm():
    return ChatOpenAI(
        model="openai/gpt-oss-120b",
        api_key=config.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        timeout=90,
        max_retries=2,
        temperature=0.2,
        max_tokens=2048
    )

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                parts.append(part.get("text", ""))
            else:
                text = getattr(part, "text", "")
                if text:
                    parts.append(text)
        return "\n".join(p for p in parts if p)
    return str(content)

def answer_question(question, k=10, max_attempts=5):
    retriever = get_retriever(k=k)
    docs = retriever.invoke(optimize_query(question))

    context = [doc.page_content for doc in docs]
    messages = build_qa_prompt(question, context)

    llm = get_llm()

    last_error = None
    for attempt in range(max_attempts):
        try:
            response = llm.invoke(messages)
            break
        except Exception as e:
            last_error = e
            message = str(e)
            if not any(code in message for code in ("503", "504", "500", "429", "UNAVAILABLE", "DEADLINE", "RESOURCE_EXHAUSTED", "INTERNAL", "GATEWAY")):
                raise
            if attempt == max_attempts - 1:
                raise RuntimeError(
                    f"LLM API unavailable after {max_attempts} attempts (rate limit / high demand). "
                    "Try again in a few seconds.") from last_error
            time.sleep(2 ** (attempt + 1))
    else:
        raise RuntimeError(
            f"LLM API unavailable after {max_attempts} attempts (rate limit / high demand). "
            "Try again in a few seconds.") from last_error

    sources = sorted({doc.metadata.get("source") for doc in docs if doc.metadata.get("source")})

    return {
        "answer": extract_text(response.content),
        "sources": sources,
    }

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    result = answer_question("How does an attacker dump credentials?")

    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")