import sys

from rag import answer_question

EXIT_COMMANDS = {"quit", "exit", "q"}

def main():
    sys.stdout.reconfigure(encoding="utf-8")

    print("CyberResAI - Cybersecurity Defense Assistant (RAG)")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            question = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue

        if question.lower() in EXIT_COMMANDS:
            break

        try:
            result = answer_question(question)
        except Exception as e:
            print(f"\nError: {e}")
            continue

        print("\nAnswer:")
        print(result["answer"])

        if result["sources"]:
            print("\nSources:")
            for source in result["sources"]:
                print(f"- {source}")
        print()

if __name__ == "__main__":
    main()