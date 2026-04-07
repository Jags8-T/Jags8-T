"""Tests for the simple chat agent."""

from agents import ChatAgent, data_ingestion


def test_chat_agent_pass_rate():
    results = data_ingestion.load_sample_results()
    agent = ChatAgent(results)
    response = agent.answer("What is the pass rate?")
    assert "50%" in response


def test_chat_agent_unknown_query():
    results = data_ingestion.load_sample_results()
    agent = ChatAgent(results)
    response = agent.answer("How many unicorns?")
    assert "pass rate" in response.lower()

