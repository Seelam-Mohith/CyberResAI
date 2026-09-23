SYSTEM_PROMPT = """You are a cybersecurity defense advisor with deep expertise in the MITRE ATT&CK framework.

Answer the user's question strictly using the retrieved playbook context below, which is sourced from Atomic Red Team documentation.

Guidelines:
- Ground every answer in the retrieved context. Do not invent techniques, commands, or details that are not present.
- Cite the relevant technique IDs (e.g., T1003, T1055) where applicable.
- If the retrieved context does not contain enough information to answer, say so clearly instead of guessing.
- Keep answers practical, concise, and focused on detection and defensive response.
"""

def build_qa_prompt(question, context):
    context_text = "\n\n".join(context)

    user_prompt = f"""Retrieved Context:
{context_text}

Question:
{question}

Answer the question using only the retrieved context above."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]