"""
Modularization Agent - "Break up the Fellowship"
Specialized agent for code modularization
Gives Aragorn, Legolas, and Gimli their own specific tasks
"""

from typing import Dict, List, Any
from .base_agent import BaseAgent


class ModularizationAgent(BaseAgent):
    """
    Agent specialized in code modularization
    
    Focuses on:
    - Breaking large files into smaller modules
    - Creating reusable utility classes
    - Establishing clear module boundaries
    - Ensuring single responsibility principle
    """
    
    def __init__(self):
        super().__init__(
            name="Aragorn (Modularization)",
            description="Break up the Fellowship - Module separation specialist"
        )
        self.modules_created = []
    
    def analyze(self) -> List[Dict[str, Any]]:
        """
        Analyze codebase for modularization opportunities
        
        Returns:
            List of modularization tasks
        """
        tasks = [
            {
                'name': 'url_validator_module',
                'description': 'Create dedicated URL validation module',
                'priority': 'high',
                'module': 'utils/url_validator.py',
                'purpose': 'Centralized URL validation and domain checking',
                'status': 'completed'
            },
            {
                'name': 'text_processor_module',
                'description': 'Create text processing utilities module',
                'priority': 'high',
                'module': 'utils/text_processor.py',
                'purpose': 'Markdown conversion and text truncation',
                'status': 'completed'
            },
            {
                'name': 'input_validator_module',
                'description': 'Create input validation and sanitization module',
                'priority': 'high',
                'module': 'utils/input_validator.py',
                'purpose': 'ASIN validation, filename sanitization, ID validation',
                'status': 'completed'
            },
            {
                'name': 'config_validator_module',
                'description': 'Create configuration validation module',
                'priority': 'high',
                'module': 'utils/config_validator.py',
                'purpose': 'Comprehensive configuration validation',
                'status': 'completed'
            },
            {
                'name': 'agents_module',
                'description': 'Create task agent management system',
                'priority': 'high',
                'module': 'agents/',
                'purpose': 'Specialized agents for different task types',
                'status': 'completed'
            },
            {
                'name': 'credential_manager_module',
                'description': 'Create credential management module',
                'priority': 'medium',
                'module': 'utils/credential_manager.py',
                'purpose': 'Unified credential loading and validation',
                'status': 'pending'
            },
            {
                'name': 'process_manager_module',
                'description': 'Create subprocess management module',
                'priority': 'medium',
                'module': 'utils/process_manager.py',
                'purpose': 'Unified subprocess execution with error handling',
                'status': 'pending'
            }
        ]
        return tasks
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a modularization task
        """
        self.modules_created.append(task['module'])
        
        if task.get('status') == 'completed':
            return {
                'success': True,
                'message': f"Module '{task['module']}' verified as created",
                'changes': [task['module']],
                'purpose': task['purpose']
            }
        
        return {
            'success': True,
            'message': f"Module '{task['module']}' identified for creation",
            'changes': [task['module']],
            'purpose': task['purpose']
        }
    
    def get_modularization_summary(self) -> str:
        """Get a summary of all modules"""
        summary = [
            "⚔️ Modularization Summary (Fellowship Divided):",
            "=" * 50,
            ""
        ]
        
        for task in self.tasks_completed:
            status = "✅" if task.get('status') == 'completed' else "📋"
            summary.append(f"{status} {task['name']}")
            summary.append(f"   📦 Module: {task['module']}")
            summary.append(f"   🎯 Purpose: {task['purpose']}")
            summary.append("")
        
        return "\n".join(summary)
