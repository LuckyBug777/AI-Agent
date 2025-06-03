#!/usr/bin/env python3
"""
AI Agent - Advanced AI Assistant with Memory and Tools

This script provides a command-line interface to interact with an AI agent
that has memory capabilities and can use various tools.
"""

import sys
import argparse
from ai_agent import AIAgent

def main():
    parser = argparse.ArgumentParser(description="AI Agent - Advanced AI Assistant")
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--model', type=str, help='OpenAI model to use')
    parser.add_argument('--quiet', action='store_true', help='Suppress welcome message')
    
    args = parser.parse_args()
    
    try:
        # Create and configure agent
        agent = AIAgent(config_file=args.config)
        
        # Override model if specified
        if args.model:
            agent.config['model'] = args.model
        
        # Start conversation
        if not args.quiet:
            print("Starting AI Agent...")
        
        agent.start_conversation()
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting AI Agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
