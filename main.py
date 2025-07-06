import os
import sys
from chatbot import Chatbot

os.environ["OPENAI_API_KEY"] = ""

def main():
    """
    Main entry point for the chatbot application.
    """
    # Ensure the data directory exists
    os.makedirs("Data", exist_ok=True)
    
    try:
        # Instantiate the chatbot.
        # This will check for the OPENAI_API_KEY environment variable.
        print("Initializing chatbot...")
        bot = Chatbot()
        
        # Start the interactive chat interface
        bot.chat_interface()
        
    except ValueError as ve:
        # This catches the specific error for a missing API key.
        print(f"\nConfiguration Error: {ve}")
        print("Please make sure you have set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
        
    except ImportError as ie:
        # Catches errors if a dependency is missing
        print(f"\nImport Error: {ie}")
        print("Please ensure all required packages are installed by running:")
        print("pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        # Catches any other unexpected errors during startup
        print(f"\nAn unexpected fatal error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
