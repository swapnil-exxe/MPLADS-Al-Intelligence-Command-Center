import pytest
from app.core.rag_engine import search_knowledge_base

def test_rag_pesticide_query():
    docs = search_knowledge_base("Is it safe to spray pesticides on cotton crop?")
    assert len(docs) > 0
    assert docs[0]["category"] == "Agriculture"

def test_rag_cyclone_query():
    docs = search_knowledge_base("Cyclone safety guidelines for fishermen")
    assert len(docs) > 0
    assert docs[0]["category"] == "Disaster Safety"
