from llm import ContentProcessor
import sys

def display_welcome():
    """Display welcome message and instructions."""
    print("Content Analysis Chat System")
    print("=" * 50)

def setup_content(url):
    """Fetch and validate scraped content via webscraper.get_content()."""
    try:
        import webscraper
        content = webscraper.get_content(url)
        if not content or len(content.strip()) < 10:
            print("Invalid content returned by webscraper.get_content()")
            return None
        return content
    except Exception as e:
        print(f"webscraper.get_content() failed: {e}")
        return None

def handle_user_input(user_input, processor, context):
    """Process user commands and questions."""
    if user_input is None:
        return True

    trimmed = user_input.strip()
    if not trimmed:
        print("Please enter a question or command")
        return True

    lowered = trimmed.lower()
    # commands are checked in lowercase, but preserve original question
    if lowered == "quit":
        return False
    elif lowered == "history":
        show_conversation_history(processor)
    elif lowered == "clear":
        processor.clear_history()
        print("History cleared")
    else:
        process_question(trimmed, processor, context)
    return True

def show_conversation_history(processor):
    """Display recent conversation history."""
    history = processor.get_recent_history()
    if not history:
        print("No conversation history available")
        return

    print("\nRecent History:")
    for idx, item in enumerate(history, 1):
        if item["type"] == "summary":
            print(f"{idx}. [SUMMARY] {item['content']}")
        else:
            print(f"{idx}. [Q] {item['question']}")
            print(f" [A] {item['answer']}")

def process_question(question, processor, context):
    """Generate and display answer to user question."""
    print("Thinking...")
    answer = processor.answer_question(question, context)
    print(f"{answer}")

def main():
    """Main chat loop."""
    display_welcome()

    context = setup_content()

    if not context:
        sys.exit(1)

    print(f"Content loaded ({len(context)} characters)")
    print("\nGenerating summary now...")

    processor = ContentProcessor()
    summary = processor.summarize_content(context)
    print(f"{summary}")

    print("\nReady! Commands: 'quit', 'history', 'clear'")
    print("-" * 50)

    should_continue = True
    while should_continue:
        try:
            user_input = input("\nYou: ")
            should_continue = handle_user_input(user_input, processor, context)
        except KeyboardInterrupt:
            print("\nThanks for using the Content Analysis Chat System!")
            break
        except Exception as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()