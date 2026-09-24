import re

INTENT_PREFIXES = [
    "what are the mitigation strategies for",
    "what are the mitigation strategy for",
    "what are the mitigations for",
    "what are the prevention strategies for",
    "what are the detection strategies for",
    "what are the best practices for",
    "what is the mitigation for",
    "what is the prevention for",
    "what is the detection for",
    "what is the",
    "what are the",
    "what is",
    "what are",
    "how can an attacker",
    "how do attackers",
    "how does an attacker",
    "how can i",
    "how do i",
    "how to prevent",
    "how to mitigate",
    "how to detect",
    "how to stop",
    "how to avoid",
    "how to defend against",
    "how to",
    "give me the mitigation for",
    "give me the prevention for",
    "give me the detection for",
    "give me the best practices for",
    "give me mitigation for",
    "give the mitigation for",
    "give mitigation for",
    "give me",
    "give",
    "can you explain",
    "can you tell me",
    "can you",
    "could you please",
    "could you",
    "do you know",
    "please explain",
    "please",
    "explain",
    "describe",
    "tell me about",
    "tell me",
    "mitigation strategies for",
    "mitigation strategy for",
    "mitigations for",
    "mitigation for",
    "prevention of",
    "prevention for",
    "detection of",
    "detection for",
    "recommendations for",
    "recommendation for",
    "best practices for",
    "strategies for",
    "for",
]

def optimize_query(question):
    cleaned = question.strip().strip("?.")
    original = cleaned

    changed = True
    while changed:
        changed = False
        lowered = cleaned.lower()
        for prefix in INTENT_PREFIXES:
            if lowered.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                changed = True
                break

    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ?.")

    if len(cleaned.split()) < 2:
        return original

    return cleaned