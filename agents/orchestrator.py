"""
Agent Orchestrator - "The Council of Elrond"
Coordinates all specialized agents and generates reports
"""

import json
from typing import Dict, List, Any
from datetime import datetime

from .optimization_agent import OptimizationAgent
from .refactoring_agent import RefactoringAgent
from .modularization_agent import ModularizationAgent
from .security_agent import SecurityAgent
from .enhancement_agent import EnhancementAgent


class AgentOrchestrator:
    """
    Orchestrates all specialized agents
    Runs The Council of Elrond to coordinate the Fellowship's tasks
    """
    
    def __init__(self):
        self.agents = {
            'optimization': OptimizationAgent(),
            'refactoring': RefactoringAgent(),
            'modularization': ModularizationAgent(),
            'security': SecurityAgent(),
            'enhancement': EnhancementAgent()
        }
        self.run_started_at: datetime = None
        self.run_completed_at: datetime = None
        self.reports: Dict[str, Dict[str, Any]] = {}
    
    def run_all_agents(self) -> Dict[str, Any]:
        """
        Run all agents and collect their reports
        
        Returns:
            Comprehensive summary of all agent work
        """
        self.run_started_at = datetime.now()
        
        print("=" * 60)
        print("🏛️  THE COUNCIL OF ELROND")
        print("    Coordinating the Fellowship's Tasks")
        print("=" * 60)
        print()
        
        for agent_name, agent in self.agents.items():
            print(f"🔄 Running {agent.name}...")
            report = agent.run()
            self.reports[agent_name] = report
            print(f"   ✅ {agent.get_status()}")
            print()
        
        self.run_completed_at = datetime.now()
        
        return self.get_comprehensive_report()
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive report of all agent work
        
        Returns:
            Complete summary of the Fellowship's tasks
        """
        total_completed = sum(r['tasks_completed'] for r in self.reports.values())
        total_pending = sum(r['tasks_pending'] for r in self.reports.values())
        
        return {
            'run_started_at': self.run_started_at.isoformat() if self.run_started_at else None,
            'run_completed_at': self.run_completed_at.isoformat() if self.run_completed_at else None,
            'total_tasks_completed': total_completed,
            'total_tasks_pending': total_pending,
            'overall_success_rate': (
                total_completed / (total_completed + total_pending)
                if (total_completed + total_pending) > 0 else 1.0
            ),
            'agent_reports': self.reports
        }
    
    def print_summary(self) -> None:
        """Print a human-readable summary to console"""
        print()
        print("=" * 60)
        print("📊 FELLOWSHIP TASK SUMMARY")
        print("=" * 60)
        print()
        
        # Print each agent's summary
        for agent_name, agent in self.agents.items():
            print(f"{'─' * 60}")
            if agent_name == 'optimization':
                print(agent.get_optimization_summary())
            elif agent_name == 'refactoring':
                print(agent.get_refactoring_summary())
            elif agent_name == 'modularization':
                print(agent.get_modularization_summary())
            elif agent_name == 'security':
                print(agent.get_security_summary())
            elif agent_name == 'enhancement':
                print(agent.get_enhancement_summary())
        
        # Print overall statistics
        print()
        print("=" * 60)
        print("📈 OVERALL STATISTICS")
        print("=" * 60)
        
        report = self.get_comprehensive_report()
        print(f"Total Tasks Completed: {report['total_tasks_completed']}")
        print(f"Total Tasks Pending: {report['total_tasks_pending']}")
        print(f"Overall Success Rate: {report['overall_success_rate']:.1%}")
    
    def save_report(self, filepath: str) -> None:
        """Save the comprehensive report to a JSON file"""
        report = self.get_comprehensive_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Report saved to: {filepath}")


def main():
    """Run the agent orchestrator"""
    orchestrator = AgentOrchestrator()
    orchestrator.run_all_agents()
    orchestrator.print_summary()


if __name__ == "__main__":
    main()
