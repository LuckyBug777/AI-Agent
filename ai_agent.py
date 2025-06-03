import os
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from memory import Memory
from tools import ToolManager

class AIAgent:
    """Advanced AI Agent with memory, tools, and conversation capabilities."""
    
    def __init__(self, config_file: Optional[str] = None):
        # Load environment variables
        load_dotenv()
        
        # Initialize console for rich output
        self.console = Console()
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY') or self.config.get('openai_api_key')
        )
        
        # Initialize components
        self.memory = Memory(
            memory_file=self.config.get('memory_file', 'agent_memory.json'),
            max_entries=self.config.get('max_memory_entries', 100)
        )
        self.tool_manager = ToolManager()
        
        # Agent personality and behavior
        self.system_prompt = self._create_system_prompt()
        
        # Conversation state
        self.conversation_active = True
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or environment variables."""
        config = {
            'agent_name': os.getenv('AGENT_NAME', 'AIAssistant'),
            'model': os.getenv('AGENT_MODEL', 'gpt-4o-mini'),
            'max_tokens': int(os.getenv('MAX_TOKENS', '2000')),
            'temperature': float(os.getenv('TEMPERATURE', '0.7')),
            'memory_file': os.getenv('MEMORY_FILE', 'agent_memory.json'),
            'max_memory_entries': int(os.getenv('MAX_MEMORY_ENTRIES', '100'))
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        
        return config
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the AI agent."""
        tools_description = self.tool_manager.get_tool_descriptions()
        
        return f"""You are {self.config['agent_name']}, an advanced AI assistant with access to tools and memory.

Your capabilities include:
1. Remembering previous conversations and context
2. Using tools to perform various tasks
3. Providing helpful, accurate, and engaging responses

Available Tools:
{tools_description}

When you need to use a tool, format your response like this:
TOOL_USE: tool_name
PARAMETERS: {{"parameter": "value"}}

Guidelines:
- Be helpful, informative, and engaging
- Use tools when appropriate to accomplish tasks
- Remember context from previous conversations
- Ask clarifying questions when needed
- Provide step-by-step explanations for complex tasks

Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _extract_tool_usage(self, response: str) -> tuple[Optional[str], Optional[Dict[str, Any]], str]:
        """Extract tool usage from agent response."""
        tool_pattern = r'TOOL_USE:\s*(\w+)\s*PARAMETERS:\s*(\{.*?\})'
        match = re.search(tool_pattern, response, re.DOTALL)
        
        if match:
            tool_name = match.group(1)
            try:
                parameters = json.loads(match.group(2))
                # Remove tool usage from response
                clean_response = re.sub(tool_pattern, '', response, flags=re.DOTALL).strip()
                return tool_name, parameters, clean_response
            except json.JSONDecodeError:
                return None, None, response
        
        return None, None, response
    
    def _get_context_messages(self) -> List[Dict[str, str]]:
        """Get conversation context from memory."""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add recent memories for context
        recent_memories = self.memory.get_recent_memories(5)
        for memory in recent_memories:
            messages.append({"role": "user", "content": memory["user_input"]})
            messages.append({"role": "assistant", "content": memory["agent_response"]})
        
        return messages
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response."""
        try:
            # Get conversation context
            messages = self._get_context_messages()
            messages.append({"role": "user", "content": user_input})
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=messages,
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature']
            )
            
            agent_response = response.choices[0].message.content
            
            # Check for tool usage
            tool_name, parameters, clean_response = self._extract_tool_usage(agent_response)
            
            final_response = clean_response
            
            # Execute tool if needed
            if tool_name and parameters:
                tool_result = self.tool_manager.execute_tool(tool_name, **parameters)
                final_response += f"\n\nTool Result:\n{tool_result}"
            
            # Store in memory
            self.memory.add_memory(
                user_input=user_input,
                agent_response=final_response,
                context={"tool_used": tool_name, "timestamp": datetime.now().isoformat()}
            )
            
            return final_response
            
        except Exception as e:
            error_response = f"I encountered an error: {str(e)}"
            self.memory.add_memory(user_input, error_response)
            return error_response
    
    def display_response(self, response: str) -> None:
        """Display response with rich formatting."""
        self.console.print(Panel(
            Markdown(response),
            title=f"[bold blue]{self.config['agent_name']}[/bold blue]",
            border_style="blue"
        ))
    
    def display_welcome(self) -> None:
        """Display welcome message."""
        welcome_text = f"""
# Welcome to {self.config['agent_name']}! 🤖

I'm your AI assistant with advanced capabilities including:
- 🧠 **Memory**: I remember our conversations
- 🛠️ **Tools**: I can perform various tasks for you
- 💬 **Natural Conversation**: Just talk to me naturally!

**Available Commands:**
- `/help` - Show available commands
- `/memory` - Show memory statistics
- `/clear` - Clear conversation memory
- `/tools` - List available tools
- `/quit` - Exit the conversation

What would you like to do today?
        """
        
        self.console.print(Panel(
            Markdown(welcome_text),
            title="[bold green]AI Agent[/bold green]",
            border_style="green"
        ))
    
    def handle_command(self, command: str) -> str:
        """Handle special commands."""
        command = command.lower().strip()
        
        if command == '/help':
            return """
**Available Commands:**
- `/help` - Show this help message
- `/memory` - Show memory statistics
- `/clear` - Clear conversation memory
- `/tools` - List available tools
- `/quit` - Exit the conversation

**Tool Usage:**
You can ask me to use tools naturally, like:
- "Calculate 2 + 2"
- "Read the file example.txt"
- "List files in the current directory"
- "Run the command 'ls -la'"
            """
        
        elif command == '/memory':
            memory_summary = self.memory.get_memory_summary()
            return f"""
**Memory Statistics:**
- Total memories: {memory_summary['total_memories']}
- Oldest entry: {memory_summary['oldest'] or 'N/A'}
- Newest entry: {memory_summary['newest'] or 'N/A'}
            """
        
        elif command == '/clear':
            self.memory.clear_memories()
            return "Memory cleared! Starting fresh conversation."
        
        elif command == '/tools':
            return f"**Available Tools:**\n{self.tool_manager.get_tool_descriptions()}"
        
        elif command == '/quit':
            self.conversation_active = False
            return "Goodbye! Thanks for using the AI Agent."
        
        else:
            return f"Unknown command: {command}. Type '/help' for available commands."
    
    def start_conversation(self) -> None:
        """Start the interactive conversation loop."""
        self.display_welcome()
        
        while self.conversation_active:
            try:
                # Get user input
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    response = self.handle_command(user_input)
                    self.display_response(response)
                else:
                    # Process normal input
                    response = self.process_input(user_input)
                    self.display_response(response)
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Conversation interrupted. Goodbye![/yellow]")
                break
            except EOFError:
                self.console.print("\n[yellow]Goodbye![/yellow]")
                break

if __name__ == "__main__":
    agent = AIAgent()
    agent.start_conversation()
