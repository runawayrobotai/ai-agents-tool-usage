import os
import json
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from dotenv import load_dotenv
import anthropic

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

# Initialize Claude client
client = anthropic.Anthropic(api_key=anthropic_api_key)

# Define the tools that Claude can use
tools = [
    {
        "name": "get_monday",
        "description": "Returns the date of the Monday of the week containing the given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_str": {
                    "type": "string",
                    "description": "The input date as a string in YYYY-MM-DD format"
                }
            },
            "required": ["date_str"]
        }
    },
    {
        "name": "get_current_date",
        "description": "Get the current date in YYYY-MM-DD format.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_week_info",
        "description": "Get comprehensive week information for a given date including all days of the week.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_str": {
                    "type": "string",
                    "description": "The input date as a string in YYYY-MM-DD format"
                }
            },
            "required": ["date_str"]
        }
    },
    {
        "name": "get_day_of_week",
        "description": "Get the day of the week for a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_str": {
                    "type": "string",
                    "description": "The input date as a string in YYYY-MM-DD format"
                }
            },
            "required": ["date_str"]
        }
    }
]

# Tool implementation functions
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

def get_current_date() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return datetime.now().strftime('%Y-%m-%d')

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

def get_day_of_week(date_str: str) -> str:
    """Get the day of the week for a given date."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f"{date_str} is a {day_names[date.weekday()]}"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

# Tool dispatcher - maps tool names to functions
tool_functions = {
    "get_monday": get_monday,
    "get_current_date": get_current_date,
    "get_week_info": get_week_info,
    "get_day_of_week": get_day_of_week
}

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool function and return the result."""
    if tool_name not in tool_functions:
        return f"Unknown tool: {tool_name}"
    
    try:
        func = tool_functions[tool_name]
        # Call function with unpacked arguments
        if tool_input:
            result = func(**tool_input)
        else:
            result = func()
        return str(result)
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"

def chat_with_claude(user_message: str, conversation_history: list) -> tuple:
    """
    Send a message to Claude and handle any tool calls.
    Returns (response_text, tools_used, updated_conversation_history)
    """
    # Add user message to conversation
    messages = conversation_history + [{"role": "user", "content": user_message}]
    
    tools_used = []
    
    try:
        # Make initial request to Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=tools,
            system="""You are a helpful AI assistant with access to date-related tools. 
            
            You should:
            - Answer general questions normally and conversationally
            - Use the available date tools when users ask about dates, weekdays, or week information
            - Be friendly and helpful with all types of questions
            
            The tools available to you are for date calculations, but you can discuss any topic the user wants to talk about."""
        )
        
        # Add Claude's response to conversation
        messages.append({"role": "assistant", "content": response.content})
        
        # Check if Claude wants to use tools
        if response.stop_reason == "tool_use":
            # Process tool calls
            tool_results = []
            
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_id = content_block.id
                    
                    tools_used.append(tool_name)
                    
                    # Execute the tool
                    tool_result = execute_tool(tool_name, tool_input)
                    
                    tool_results.append({
                        "tool_use_id": tool_id,
                        "type": "tool_result",
                        "content": tool_result
                    })
            
            # Send tool results back to Claude
            messages.append({"role": "user", "content": tool_results})
            
            # Get Claude's final response
            final_response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=messages,
                tools=tools
            )
            
            # Extract text response
            response_text = ""
            for content_block in final_response.content:
                if content_block.type == "text":
                    response_text += content_block.text
            
            # Add final response to conversation
            messages.append({"role": "assistant", "content": final_response.content})
            
        else:
            # No tools used, just get the text response
            response_text = ""
            for content_block in response.content:
                if content_block.type == "text":
                    response_text += content_block.text
        
        return response_text, tools_used, messages
        
    except Exception as e:
        return f"Error communicating with Claude: {str(e)}", [], messages

def show_welcome():
    """Display welcome message and instructions."""
    print_colored("System", "🤖 Claude Chat with Date Tools (Simple Version)")
    print_colored("System", "=" * 60)
    print_colored("System", "Available commands:")
    print_colored("System", "- Ask any question")
    print_colored("System", "- Ask about Monday dates (e.g., 'What date is Monday of the week containing 2025-07-08?')")
    print_colored("System", "- Ask for current date or week information")
    print_colored("System", "- Type '/bye' to exit")
    print_colored("System", "- Type '/help' for more commands")
    print_colored("System", "=" * 60)

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
    
    # Initialize conversation history
    conversation_history = []
    
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
                conversation_history = []
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process the user's question with Claude
            print_colored("System", "🤔 Thinking...")
            
            response_text, tools_used, conversation_history = chat_with_claude(user_input, conversation_history)
            
            # Display Claude's response
            print_colored("Assistant", response_text)
            
            # Show which tools were used
            if tools_used:
                tools_list = ", ".join(set(tools_used))
                print_colored("System", f"🔧 Used tools: {tools_list}")
        
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
