#!/bin/bash
# AI Agent Launcher Script
# This script runs the AI agent with a clean library environment

cd "$(dirname "$0")"

# Clear LD_LIBRARY_PATH to avoid conflicts with system libraries
export LD_LIBRARY_PATH=""

# Run the AI agent
python main.py "$@"
