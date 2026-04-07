"""Tests for the simple chat agent."""

from agents import ChatAgent, data_ingestion


def test_chat_agent_pass_rate():
    results = data_ingestion.load_sample_results()
    agent = ChatAgent(results)
    response = agent.answer("What is the pass rate?")
    assert "62%" in response


def test_chat_agent_summary():
    results = data_ingestion.load_sample_results()
    agent = ChatAgent(results)
    response = agent.answer("Give KPI summary")
    assert "Processed 8 tests" in response


def test_chat_agent_unknown_query():
    results = data_ingestion.load_sample_results()
    agent = ChatAgent(results)
    response = agent.answer("How many unicorns?")
    assert "pass rate" in response.lower()
