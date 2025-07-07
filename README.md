# AI Agents Tool Usage

A demonstration project showcasing two different approaches to implementing LLM tool calling with Python. This project compares a simple implementation using the Anthropic Claude API directly versus a more practical approach using the PydanticAI framework.

## 🎯 Project Overview

This project demonstrates how to create AI agents that can use tools to perform date-related calculations. It includes two implementations:

1. **Simple AI Tools** (`simple_ai_tools.py`) - Manual tool calling implementation using the Anthropic Claude API
2. **PydanticAI Tools** (`pydantic_ai_tools.py`) - Streamlined implementation using the PydanticAI framework

Both programs provide identical functionality but showcase different architectural approaches to tool integration.

## ✨ Features

- **Interactive Chat Interface** - Conversational AI that responds to natural language queries
- **Date Tool Functions**:
  - Find the Monday of any given week
  - Get current date
  - Get comprehensive week information (all 7 days)
  - Determine day of the week for any date
- **Colored Terminal Output** - Enhanced user experience with color-coded responses
- **Command System** - Built-in commands for help, clearing history, and exiting
- **Error Handling** - Robust error handling for invalid dates and API issues

## 🔧 Prerequisites

- Python 3.8 or higher
- Anthropic Claude API key
- Terminal/Command prompt access

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/runawayrobotai/ai-agents-tool-usage
cd ai-agents-tool-usage
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install anthropic python-dotenv colorama pydantic-ai
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your Anthropic API key to the `.env` file:

```
ANTHROPIC_API_KEY=your_api_key_here
```

**To get an Anthropic API key:**
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## 🚀 Usage

### Running the Simple AI Tools Version

```bash
python simple_ai_tools.py
```

This version demonstrates manual tool calling implementation with detailed control over the tool execution process.

### Running the PydanticAI Version

```bash
python pydantic_ai_tools.py
```

This version uses the PydanticAI framework for tool integration and cleaner code structure.

### Available Commands

Both programs support the following commands:

- `/help` - Show available commands and example questions
- `/clear` - Clear conversation history
- `/bye`, `/exit`, `/quit` - Exit the program
- `Ctrl+C` - Force exit

### Example Interactions

```
You: What date is Monday of the week containing 2025-07-08?
Assistant: The Monday of the week containing 2025-07-08 is 2025-07-07.

You: What's today's date?
Assistant: Today's date is 2025-01-07.

You: Show me all days of the week for 2025-12-25
Assistant: Week containing 2025-12-25:
Monday: 2025-12-22
Tuesday: 2025-12-23
Wednesday: 2025-12-24
Thursday: 2025-12-25
Friday: 2025-12-26
Saturday: 2025-12-27
Sunday: 2025-12-28

You: What day of the week is 2025-07-04?
Assistant: 2025-07-04 is a Friday
```

## 📋 Dependencies

| Package | Purpose |
|---------|---------|
| `anthropic` | Official Anthropic Claude API client |
| `python-dotenv` | Load environment variables from .env file |
| `colorama` | Cross-platform colored terminal text output |
| `pydantic-ai` | Simplified AI agent framework with tool support |

## 📁 Project Structure

```
ai-agents-tool-usage/
├── simple_ai_tools.py      # Manual tool calling implementation
├── pydantic_ai_tools.py    # PydanticAI framework implementation
├── README.md               # This file
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── requirements.txt        # Python dependencies (optional)
```

### File Descriptions

- **`simple_ai_tools.py`** - Demonstrates manual tool calling with explicit tool definition, execution handling, and conversation management
- **`pydantic_ai_tools.py`** - Shows simplified approach using PydanticAI decorators and automatic tool integration
- **`.env`** - Contains your Anthropic API key

## 🔍 Key Differences Between Implementations

| Aspect | Simple AI Tools | PydanticAI Tools |
|--------|----------------|------------------|
| **Code Complexity** | More verbose, explicit control | Cleaner, more concise |
| **Tool Definition** | Manual JSON schema definition | Decorator-based (@agent.tool_plain) |
| **Tool Execution** | Custom dispatcher function | Automatic handling |
| **Conversation Management** | Manual message history tracking | Built-in conversation handling |
| **Error Handling** | Explicit try-catch blocks | Framework-level error handling |
| **Learning Value** | Shows underlying mechanics | Focuses on business logic |

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Not Found Error**
```
❌ Error: ANTHROPIC_API_KEY not found in environment variables.
```
- Ensure your `.env` file exists in the project root
- Verify the API key is correctly formatted in the `.env` file
- Check that the `.env` file contains: `ANTHROPIC_API_KEY=your_actual_key`

**2. Module Not Found Errors**
```
ModuleNotFoundError: No module named 'anthropic'
```
- Ensure you've activated your virtual environment
- Run `pip install -r requirements.txt` or install packages individually
- Verify you're using the correct Python environment

**3. Invalid Date Format**
- Use YYYY-MM-DD format for all date inputs
- Example: 2025-07-08 (not 07/08/2025 or 8-7-2025)

**4. Connection Issues**
- Check your internet connection
- Verify your API key is valid and has available credits
- Ensure you're not hitting rate limits

## 🎓 Learning Objectives

This project demonstrates:

- **Tool Calling Patterns** - How to implement function calling with LLMs
- **API Integration** - Working with the Anthropic Claude API
- **Framework Comparison** - Manual vs. framework-assisted development
- **Error Handling** - Robust error handling in AI applications
- **User Experience** - Creating interactive command-line applications

## 📚 Additional Resources

- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Python dotenv Documentation](https://python-dotenv.readthedocs.io/)


## 📄 License

This project is open source and available under the [MIT License](LICENSE).
