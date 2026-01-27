#!/usr/bin/env python3
"""
Unit tests for agent modules
"""

import sys
from agents import (
    BaseAgent,
    OptimizationAgent,
    RefactoringAgent,
    ModularizationAgent,
    SecurityAgent,
    EnhancementAgent
)
from agents.orchestrator import AgentOrchestrator


def test_optimization_agent():
    """Test optimization agent"""
    print("🧪 Testing OptimizationAgent...")
    
    try:
        agent = OptimizationAgent()
        
        # Check agent properties
        if agent.name != "Gandalf (Optimization)":
            print(f"   ❌ Wrong agent name: {agent.name}")
            return False
        
        # Run analysis
        tasks = agent.analyze()
        if not tasks or len(tasks) == 0:
            print("   ❌ No tasks returned from analysis")
            return False
        
        # Run agent
        report = agent.run()
        if report['tasks_completed'] == 0:
            print("   ❌ No tasks completed")
            return False
        
        # Get summary
        summary = agent.get_optimization_summary()
        if "Great Eagles" not in summary:
            print("   ❌ Summary missing expected content")
            return False
        
        print("   ✅ OptimizationAgent working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ OptimizationAgent error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_refactoring_agent():
    """Test refactoring agent"""
    print("🧪 Testing RefactoringAgent...")
    
    try:
        agent = RefactoringAgent()
        
        # Check agent properties
        if agent.name != "Samwise (Refactoring)":
            print(f"   ❌ Wrong agent name: {agent.name}")
            return False
        
        # Run agent
        report = agent.run()
        if report['tasks_completed'] == 0:
            print("   ❌ No tasks completed")
            return False
        
        # Get summary
        summary = agent.get_refactoring_summary()
        if "Camp Organized" not in summary:
            print("   ❌ Summary missing expected content")
            return False
        
        print("   ✅ RefactoringAgent working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ RefactoringAgent error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modularization_agent():
    """Test modularization agent"""
    print("🧪 Testing ModularizationAgent...")
    
    try:
        agent = ModularizationAgent()
        
        # Check agent properties
        if agent.name != "Aragorn (Modularization)":
            print(f"   ❌ Wrong agent name: {agent.name}")
            return False
        
        # Run agent
        report = agent.run()
        if report['tasks_completed'] == 0:
            print("   ❌ No tasks completed")
            return False
        
        # Get summary
        summary = agent.get_modularization_summary()
        if "Fellowship Divided" not in summary:
            print("   ❌ Summary missing expected content")
            return False
        
        print("   ✅ ModularizationAgent working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ ModularizationAgent error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_security_agent():
    """Test security agent"""
    print("🧪 Testing SecurityAgent...")
    
    try:
        agent = SecurityAgent()
        
        # Check agent properties
        if agent.name != "Legolas (Security)":
            print(f"   ❌ Wrong agent name: {agent.name}")
            return False
        
        # Run agent
        report = agent.run()
        if report['tasks_completed'] == 0:
            print("   ❌ No tasks completed")
            return False
        
        # Get summary
        summary = agent.get_security_summary()
        if "Ranks Inspected" not in summary:
            print("   ❌ Summary missing expected content")
            return False
        
        # Check for fixed vulnerabilities
        if len(agent.vulnerabilities_fixed) == 0:
            print("   ❌ No vulnerabilities marked as fixed")
            return False
        
        print("   ✅ SecurityAgent working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ SecurityAgent error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_enhancement_agent():
    """Test enhancement agent"""
    print("🧪 Testing EnhancementAgent...")
    
    try:
        agent = EnhancementAgent()
        
        # Check agent properties
        if agent.name != "Gimli (Enhancement)":
            print(f"   ❌ Wrong agent name: {agent.name}")
            return False
        
        # Run agent
        report = agent.run()
        if report['tasks_completed'] == 0:
            print("   ❌ No tasks completed")
            return False
        
        # Get summary
        summary = agent.get_enhancement_summary()
        if "Fellowship Leveled Up" not in summary:
            print("   ❌ Summary missing expected content")
            return False
        
        print("   ✅ EnhancementAgent working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ EnhancementAgent error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_orchestrator():
    """Test agent orchestrator"""
    print("🧪 Testing AgentOrchestrator...")
    
    try:
        orchestrator = AgentOrchestrator()
        
        # Check all agents are loaded
        if len(orchestrator.agents) != 5:
            print(f"   ❌ Wrong number of agents: {len(orchestrator.agents)}")
            return False
        
        # Run all agents (suppress output)
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            report = orchestrator.run_all_agents()
        finally:
            sys.stdout = old_stdout
        
        # Check report
        if report['total_tasks_completed'] == 0:
            print("   ❌ No tasks completed")
            return False
        
        if report['overall_success_rate'] < 0.5:
            print(f"   ❌ Low success rate: {report['overall_success_rate']:.1%}")
            return False
        
        print("   ✅ AgentOrchestrator working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ AgentOrchestrator error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_text_processor_extract_heading():
    """Test the new extract_heading method"""
    print("🧪 Testing TextProcessor.extract_heading...")
    
    try:
        from utils import TextProcessor
        
        # Test with valid heading
        markdown = "# Hello World\n\nSome content here"
        heading = TextProcessor.extract_heading(markdown)
        if heading != "Hello World":
            print(f"   ❌ Wrong heading extracted: {heading}")
            return False
        
        # Test with ## heading
        markdown = "## Second Level\n\nContent"
        heading = TextProcessor.extract_heading(markdown)
        if heading != "Second Level":
            print(f"   ❌ Wrong heading extracted: {heading}")
            return False
        
        # Test with no heading
        markdown = "No heading here"
        heading = TextProcessor.extract_heading(markdown, "Default")
        if heading != "Default":
            print(f"   ❌ Default not returned: {heading}")
            return False
        
        # Test with empty string
        heading = TextProcessor.extract_heading("", "Empty Default")
        if heading != "Empty Default":
            print(f"   ❌ Empty default not returned: {heading}")
            return False
        
        print("   ✅ TextProcessor.extract_heading working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ TextProcessor.extract_heading error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run agent tests"""
    print("=" * 60)
    print("🧪 RUNNING AGENT MODULE TESTS")
    print("=" * 60)
    print()
    
    tests = [
        ("OptimizationAgent", test_optimization_agent),
        ("RefactoringAgent", test_refactoring_agent),
        ("ModularizationAgent", test_modularization_agent),
        ("SecurityAgent", test_security_agent),
        ("EnhancementAgent", test_enhancement_agent),
        ("AgentOrchestrator", test_orchestrator),
        ("TextProcessor.extract_heading", test_text_processor_extract_heading),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   💥 Unexpected error: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL AGENT TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
