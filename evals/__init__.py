"""
Evals Module
-------------

Evaluation suite for AgentOS agents. Demonstrates three eval types:

- **AccuracyEval**: Does the agent produce the correct answer?
- **AgentAsJudgeEval**: Is the response high-quality by LLM judgment?
- **ReliabilityEval**: Does the agent call the expected tools?

Top-level evals (this module) test cross-agent concerns like accuracy, quality,
and reliability. Per-agent evals (``agents/<name>/evals/``) test agent-specific
behavior with dedicated test cases using the same Agno eval framework.

Run all evals:
    python -m evals
"""

from dataclasses import dataclass

from evals.accuracy import dash_accuracy_eval, scout_accuracy_eval
from evals.quality import scout_quality_eval, seek_quality_eval


@dataclass
class TestCase:
    """A test case for evaluating an agent.

    Shared across per-agent eval suites (Guard, Relay, Sentinel, etc.).
    """

    question: str
    expected_strings: list[str]
    expected_tools: list[str]
    category: str


__all__ = [
    "TestCase",
    "dash_accuracy_eval",
    "scout_accuracy_eval",
    "scout_quality_eval",
    "seek_quality_eval",
]
