"""
##Script function and purpose: Unit tests for logos.core.agent module.

Tests the Agent dataclass functionality including creation, properties, and memory optimization.
"""

import pytest
from logos.core.agent import Agent


##Function purpose: Test Agent dataclass creation with all fields
def test_agent_creation():
    """
    ##Function purpose: Verify Agent can be created with all required fields.
    """
    ##Action purpose: Create agent with all fields
    agent = Agent(
        name="The Architect",
        desc="Structure and scaffolding",
        group="A",
        base_prompt="Base prompt",
        activation_prompt="Activation prompt",
        purpose="Design system structure"
    )
    
    ##Condition purpose: Verify all fields are set correctly
    assert agent.name == "The Architect"
    assert agent.desc == "Structure and scaffolding"
    assert agent.group == "A"
    assert agent.base_prompt == "Base prompt"
    assert agent.activation_prompt == "Activation prompt"
    assert agent.purpose == "Design system structure"


##Function purpose: Test full_prompt property
def test_agent_full_prompt():
    """
    ##Function purpose: Verify full_prompt property combines base and activation prompts.
    """
    ##Action purpose: Create agent with separate prompts
    agent = Agent(
        name="Test Agent",
        desc="Test",
        group="A",
        base_prompt="Base: ",
        activation_prompt="Activation",
        purpose="Test"
    )
    
    ##Condition purpose: Verify full_prompt combines both
    assert agent.full_prompt == "Base: Activation"


##Function purpose: Test Agent with slots optimization
def test_agent_slots():
    """
    ##Function purpose: Verify Agent uses __slots__ for memory optimization.
    """
    ##Action purpose: Create agent instance
    agent = Agent(
        name="Test",
        desc="Test",
        group="A",
        base_prompt="",
        activation_prompt="",
        purpose=""
    )
    
    ##Condition purpose: Verify slots are used (no __dict__ attribute)
    assert not hasattr(agent, '__dict__')


##Function purpose: Test Agent type validation
def test_agent_type_hints():
    """
    ##Function purpose: Verify Agent fields accept correct types.
    """
    ##Action purpose: Create agent with string fields
    agent = Agent(
        name="Test",
        desc="Description",
        group="B",
        base_prompt="Base",
        activation_prompt="Activation",
        purpose="Purpose"
    )
    
    ##Condition purpose: Verify all fields are strings
    assert isinstance(agent.name, str)
    assert isinstance(agent.desc, str)
    assert isinstance(agent.group, str)
    assert isinstance(agent.base_prompt, str)
    assert isinstance(agent.activation_prompt, str)
    assert isinstance(agent.purpose, str)
