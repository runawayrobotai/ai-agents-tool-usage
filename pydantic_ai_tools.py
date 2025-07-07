import os
import re
import json
from colorama import Fore, Style, init
from pydantic_ai import Agent
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize colorama
init()

# Read the API key
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

def print_colored(agent_name, text):
    """Print colored text based on the agent/speaker."""
    agent_colors = {
        "Assistant": Fore.CYAN,
        "User": Fore.GREEN,
        "System": Fore.YELLOW,
    }
    color = agent_colors.get(agent_name, Fore.WHITE)
    print(color + f"{agent_name}: {text}" + Style.RESET_ALL)

# Create agent with tools
# agent = Agent("anthropic:claude-3-5-sonnet-latest")
agent = Agent(
    "anthropic:claude-3-5-sonnet-latest",
    system_prompt="""You are a helpful AI assistant with access to date-related tools. 
    
    You should:
    - Answer general questions normally and conversationally
    - Use the available date tools when users ask about dates, weekdays, or week information
    - Be friendly and helpful with all types of questions
    
    The tools available to you are for date calculations, but you can discuss any topic the user wants to talk about."""
)

@agent.tool_plain
def get_monday(date_str: str) -> str:
    """
    Returns the date of the Monday of the week containing the given date.
    
    Args:
        date_str: The input date as a string in YYYY-MM-DD format
        
    Returns:
        str: The date of the Monday of that week in YYYY-MM-DD format
    """
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        monday = date - timedelta(days=date.weekday())
        return monday.strftime('%Y-%m-%d')
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

@agent.tool_plain
def get_current_date() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return datetime.now().strftime('%Y-%m-%d')

@agent.tool_plain
def get_week_info(date_str: str) -> str:
    """Get comprehensive week information for a given date including all days of the week."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        monday = date - timedelta(days=date.weekday())
        
        week_days = []
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i in range(7):
            day = monday + timedelta(days=i)
            week_days.append(f"{day_names[i]}: {day.strftime('%Y-%m-%d')}")
        
        return f"Week containing {date_str}:\n" + "\n".join(week_days)
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

@agent.tool_plain
def get_day_of_week(date_str: str) -> str:
    """Get the day of the week for a given date."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f"{date_str} is a {day_names[date.weekday()]}"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

def show_welcome():
    """Display welcome message and instructions."""
    print_colored("System", "🤖 Claude Chat with Date Tools")
    print_colored("System", "=" * 50)
    print_colored("System", "Available commands:")
    print_colored("System", "- Ask any question")
    print_colored("System", "- Ask about Monday dates (e.g., 'What date is Monday of the week containing 2025-07-08?')")
    print_colored("System", "- Ask for current date or week information")
    print_colored("System", "- Type '/bye' to exit")
    print_colored("System", "- Type '/help' for more commands")
    print_colored("System", "=" * 50)

def show_help():
    """Display help information."""
    print_colored("System", "Available commands:")
    print_colored("System", "- '/bye', '/exit', '/quit' - Exit the chat")
    print_colored("System", "- '/help' - Show this help message")
    print_colored("System", "- '/clear' - Clear conversation history")
    print_colored("System", "\nExample questions:")
    print_colored("System", "- 'What date is Monday of the week containing 2025-07-08?'")
    print_colored("System", "- 'What's today's date?'")
    print_colored("System", "- 'Show me all days of the week for 2025-12-25'")
    print_colored("System", "- 'What day of the week is 2025-07-04?'")
    print_colored("System", "- 'What's the Monday of this week?'")

def main():
    """Main chat loop."""
    show_welcome()
    
    while True:
        try:
            # Get user input
            user_input = input(f"\n{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            # Check for exit command
            if user_input.lower() in ['/bye', '/exit', '/quit']:
                print_colored("System", "👋 Goodbye! Thanks for chatting!")
                break
            
            # Check for help command
            if user_input.lower() == '/help':
                show_help()
                continue
            
            # Check for clear command
            if user_input.lower() == '/clear':
                print_colored("System", "🧹 Conversation history cleared!")
                # Note: In a more advanced implementation, you'd reset the agent's message history
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process the user's question with the agent
            print_colored("System", "🤔 Thinking...")
            
            try:
                result = agent.run_sync(user_input)
                print_colored("Assistant", result.output)
                
                # Show if any tools were used (optional debug info)
                if hasattr(result, 'all_messages'):
                    messages = result.all_messages()
                    tool_calls = []
                    for msg in messages:
                        if hasattr(msg, 'parts'):
                            for part in msg.parts:
                                if hasattr(part, 'tool_name'):
                                    tool_calls.append(part.tool_name)
                    
                    if tool_calls:
                        tools_used = ", ".join(set(tool_calls))
                        print_colored("System", f"🔧 Used tools: {tools_used}")
                
            except Exception as e:
                print_colored("System", f"❌ Error: {str(e)}")
                print_colored("System", "Please try rephrasing your question.")
        
        except KeyboardInterrupt:
            print_colored("System", "\n👋 Goodbye! (Ctrl+C pressed)")
            break
        except EOFError:
            print_colored("System", "\n👋 Goodbye! (EOF)")
            break

if __name__ == "__main__":
    # Check if API key is available
    if not anthropic_api_key:
        print_colored("System", "❌ Error: ANTHROPIC_API_KEY not found in environment variables.")
        print_colored("System", "Please make sure your .env file contains: ANTHROPIC_API_KEY=your_api_key_here")
        exit(1)
    
    main()
