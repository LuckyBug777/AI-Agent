import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class Memory:
    """Memory system for the AI agent to store and retrieve conversation history and context."""
    
    def __init__(self, memory_file: str = "agent_memory.json", max_entries: int = 100):
        self.memory_file = memory_file
        self.max_entries = max_entries
        self.memories = self._load_memories()
    
    def _load_memories(self) -> List[Dict[str, Any]]:
        """Load memories from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_memories(self) -> None:
        """Save memories to file."""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def add_memory(self, user_input: str, agent_response: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Add a new memory entry."""
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": agent_response,
            "context": context or {}
        }
        
        self.memories.append(memory_entry)
        
        # Keep only the most recent entries
        if len(self.memories) > self.max_entries:
            self.memories = self.memories[-self.max_entries:]
        
        self._save_memories()
    
    def get_recent_memories(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get recent memories for context."""
        return self.memories[-count:] if self.memories else []
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search memories by keyword."""
        query_lower = query.lower()
        matching_memories = []
        
        for memory in reversed(self.memories):
            if (query_lower in memory['user_input'].lower() or 
                query_lower in memory['agent_response'].lower()):
                matching_memories.append(memory)
                if len(matching_memories) >= limit:
                    break
        
        return matching_memories
    
    def clear_memories(self) -> None:
        """Clear all memories."""
        self.memories = []
        self._save_memories()
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of stored memories."""
        if not self.memories:
            return {"total_memories": 0, "oldest": None, "newest": None}
        
        return {
            "total_memories": len(self.memories),
            "oldest": self.memories[0]["timestamp"],
            "newest": self.memories[-1]["timestamp"]
        }
