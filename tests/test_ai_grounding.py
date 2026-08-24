import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.ai_investigator import ai_investigator

def test_ai_unsupported_questions():
    unsupported_prompts = [
        "Show projects with contractor X",
        "Show payment anomalies",
        "Show GPS locations",
        "Which project was delayed?"
    ]
    for prompt in unsupported_prompts:
        res = ai_investigator.answer_query(prompt)
        assert res['query_type'] == 'out_of_scope_notice'
        assert "does not contain enough information" in res['answer']

def test_ai_supported_questions():
    supported_prompts = [
        "Why is this MP high risk?",
        "Show the allocation of this MP",
        "Which state has the highest allocation?"
    ]
    for prompt in supported_prompts:
        res = ai_investigator.answer_query(prompt)
        assert res['is_grounded'] is True
        assert len(res['tools_executed']) >= 1
