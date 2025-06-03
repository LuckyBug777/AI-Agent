# AI Agent

A sophisticated AI assistant with memory capabilities, tool integration, and conversational interface.

## Features

- 🧠 **Persistent Memory**: Remembers conversations and context across sessions
- 🛠️ **Tool Integration**: Can perform file operations, calculations, system commands, and more
- 💬 **Natural Conversation**: Intuitive chat interface with rich formatting
- ⚙️ **Configurable**: Customizable settings via environment variables or config files
- 🎨 **Rich UI**: Beautiful terminal interface with colors and formatting

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   - Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key
   - Or set the environment variable: `export OPENAI_API_KEY=your_key_here`

## Usage

### Basic Usage

```bash
python main.py
```

### Command Line Options

```bash
python main.py --help
```

Options:
- `--config`: Specify a custom configuration file
- `--model`: Override the OpenAI model to use
- `--quiet`: Suppress the welcome message

### Interactive Commands

Once the agent is running, you can use these commands:

- `/help` - Show available commands
- `/memory` - Show memory statistics  
- `/clear` - Clear conversation memory
- `/tools` - List available tools
- `/quit` - Exit the conversation

## Available Tools

The AI agent comes with several built-in tools:

1. **File Manager**: Read, write, and list files
   - Example: "Read the contents of myfile.txt"
   - Example: "Write 'Hello World' to test.txt"

2. **Calculator**: Perform mathematical calculations
   - Example: "Calculate 2 + 2 * 3"
   - Example: "What's the square root of 144?"

3. **System Commands**: Execute system commands
   - Example: "Run the command 'ls -la'"
   - Example: "Show me the current directory"

4. **Web Search**: Search the web (requires API integration)
   - Example: "Search for Python tutorials"

## Configuration

You can configure the agent using environment variables in the `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
AGENT_MODEL=gpt-4o-mini
MAX_TOKENS=2000
TEMPERATURE=0.7

# Agent Settings
AGENT_NAME=AIAssistant

# Memory Settings
MEMORY_FILE=agent_memory.json
MAX_MEMORY_ENTRIES=100
```

## Example Conversations

### Basic Chat
```
🧑 You: Hello! What can you do?

🤖 AIAssistant: Hello! I'm an advanced AI assistant with several capabilities:

1. **Conversational AI**: I can chat naturally and remember our conversation
2. **File Operations**: I can read, write, and manage files
3. **Calculations**: I can perform mathematical calculations
4. **System Commands**: I can execute system commands safely
5. **Memory**: I remember our conversations across sessions

What would you like to do today?
```

### Using Tools
```
🧑 You: Calculate the area of a circle with radius 5

🤖 AIAssistant: I'll calculate the area of a circle with radius 5 for you.

Tool Result:
Result: 78.53981633974483

The area of a circle with radius 5 is approximately 78.54 square units.
The formula used is: Area = π × r² = π × 5² = π × 25 ≈ 78.54
```

### File Operations
```  
🧑 You: Create a file called hello.txt with the content "Hello, World!"

🤖 AIAssistant: I'll create the file for you.

Tool Result:
Successfully wrote to hello.txt

Perfect! I've created the file `hello.txt` with the content "Hello, World!". The file has been saved successfully.
```

## Project Structure

```
ai_agent/
├── main.py           # Entry point and CLI interface
├── ai_agent.py       # Main AI agent class
├── memory.py         # Memory management system
├── tools.py          # Tool definitions and manager
├── requirements.txt  # Python dependencies
├── .env             # Environment configuration
└── README.md        # This file
```

## Extending the Agent

### Adding New Tools

To add a new tool, create a class that inherits from the `Tool` base class:

```python
from tools import Tool

class MyCustomTool(Tool):
    def name(self) -> str:
        return "my_tool"
    
    def description(self) -> str:
        return "Description of what my tool does"
    
    def execute(self, **kwargs) -> str:
        # Implement your tool logic here
        return "Tool result"

# Add to the tool manager
agent.tool_manager.add_tool(MyCustomTool())
```

### Customizing Memory

The memory system can be extended by modifying the `Memory` class in `memory.py`. You can add features like:
- Semantic search through memories
- Memory categorization
- Advanced context retrieval

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for OpenAI API calls

## Security Notes

- The system command tool has basic safety measures but should be used carefully
- File operations are restricted to the current directory and subdirectories
- API keys should be kept secure and not shared

## Troubleshooting

### Common Issues

1. **Missing API Key**: Make sure your OpenAI API key is set in the `.env` file
2. **Module Not Found**: Run `pip install -r requirements.txt` to install dependencies  
3. **Permission Errors**: Make sure you have write permissions for memory files

### Error Messages

The agent provides helpful error messages for common issues. If you encounter problems:

1. Check your API key configuration
2. Verify all dependencies are installed
3. Ensure you have proper file permissions
4. Check the console output for detailed error information

## License

This project is open source. Feel free to modify and extend it for your needs.

## Contributing

Contributions are welcome! Some areas for improvement:
- Additional tools and integrations
- Enhanced memory capabilities
- Better error handling
- Web interface
- Multi-language support
