import os

from dotenv import load_dotenv

load_dotenv()


def _secret(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = _secret("GROQ_API_KEY")