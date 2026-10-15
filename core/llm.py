import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
MODEL_NAME=openai/gpt-oss-20b
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY missing. Check your .env file."
    )

if not MODEL_NAME:
    raise ValueError(
        "MODEL_NAME missing. Check your .env file."
    )

llm = ChatGroq(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    temperature=0,
)


def test_llm() -> None:
    response = llm.invoke(
        "Explain multi-agent AI in two simple sentences."
    )

    print("\n===== LLM RESPONSE =====\n")
    print(response.content)


if __name__ == "__main__":
    test_llm()
