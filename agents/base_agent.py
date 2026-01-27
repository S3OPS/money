"""
Base Agent class for all specialized agents
Provides common functionality for task execution and reporting
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for all task agents"""
    
    def __init__(self, name: str, description: str):
        """
        Initialize the agent
        
        Args:
            name: Agent identifier name
            description: Brief description of the agent's purpose
        """
        self.name = name
        self.description = description
        self.tasks_completed: List[Dict[str, Any]] = []
        self.tasks_pending: List[Dict[str, Any]] = []
        self.started_at: datetime = None
        self.completed_at: datetime = None
    
    @abstractmethod
    def analyze(self) -> List[Dict[str, Any]]:
        """
        Analyze the codebase and identify tasks
        
        Returns:
            List of task dictionaries with 'name', 'description', 'priority', 'file'
        """
        pass
    
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific task
        
        Args:
            task: Task dictionary from analyze()
            
        Returns:
            Result dictionary with 'success', 'message', 'changes'
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Run the agent to analyze and execute all tasks
        
        Returns:
            Summary of all completed tasks
        """
        self.started_at = datetime.now()
        
        # Analyze and get tasks
        self.tasks_pending = self.analyze()
        
        results = []
        for task in self.tasks_pending[:]:  # Copy to allow modification
            result = self.execute(task)
            if result.get('success', False):
                self.tasks_completed.append(task)
                self.tasks_pending.remove(task)
            results.append({
                'task': task,
                'result': result
            })
        
        self.completed_at = datetime.now()
        
        return self.get_report()
    
    def get_report(self) -> Dict[str, Any]:
        """
        Generate a summary report of the agent's work
        
        Returns:
            Report dictionary with statistics and details
        """
        return {
            'agent_name': self.name,
            'description': self.description,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'tasks_completed': len(self.tasks_completed),
            'tasks_pending': len(self.tasks_pending),
            'completed_tasks': self.tasks_completed,
            'pending_tasks': self.tasks_pending,
            'success_rate': (
                len(self.tasks_completed) / (len(self.tasks_completed) + len(self.tasks_pending))
                if (len(self.tasks_completed) + len(self.tasks_pending)) > 0 else 1.0
            )
        }
    
    def get_status(self) -> str:
        """Get a human-readable status string"""
        total = len(self.tasks_completed) + len(self.tasks_pending)
        completed = len(self.tasks_completed)
        return f"{self.name}: {completed}/{total} tasks completed"
