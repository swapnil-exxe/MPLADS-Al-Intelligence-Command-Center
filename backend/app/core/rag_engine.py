import json
import os
from typing import List, Dict, Any

KNOWLEDGE_DOCUMENTS = [
    {
        "id": "AGRO-01",
        "topic": "Pesticide Spraying & Rainfall Safety",
        "category": "Agriculture",
        "keywords": ["pesticide", "spray", "cotton", "crops", "rain", "wind", "nashik", "maharashtra"],
        "content": "Agromet Advisory (ICAR/IMD): Do not apply chemical pesticides or fertilizer top-dressing when rain probability exceeds 60% or wind speeds exceed 15 km/h. Rain washes away active ingredients into groundwater, causing crop failure and economic loss. Ideal spraying conditions: Calm morning hours (< 10 km/h wind) with clear skies."
    },
    {
        "id": "AGRO-02",
        "topic": "Cotton Crop Waterlogging Management",
        "category": "Agriculture",
        "keywords": ["cotton", "waterlogging", "heavy rain", "irrigation", "drainage"],
        "content": "Agromet Advisory: In case of heavy rainfall in black cotton soils, open surface drainage channels immediately to drain excess water. Standing water for more than 48 hours causes root hypoxia and fungal rot (damping off)."
    },
    {
        "id": "DISASTER-01",
        "topic": "Flood Evacuation & Emergency Guidelines (NDMA)",
        "category": "Disaster Safety",
        "keywords": ["flood", "evacuation", "emergency", "ndma", "waterlogging", "heavy rainfall"],
        "content": "NDMA Flood Protocol: Move to elevated ground or designated cyclone/flood shelters immediately upon Orange/Red alert. Do not walk or drive through moving water (6 inches of swift water can sweep a person away). Switch off main electrical supply before evacuating."
    },
    {
        "id": "DISASTER-02",
        "topic": "Cyclone & Storm Safety for Fishermen (NDMA)",
        "category": "Disaster Safety",
        "keywords": ["cyclone", "sea", "fishermen", "waves", "wind", "coastal", "ratnagiri", "puri"],
        "content": "NDMA Cyclone Protocol for Marine Sector: When wind speeds exceed 40 km/h or high wave alerts are issued, all fishing trawlers must return to port immediately. Secure boats with double mooring ropes and stay away from sea walls during high tide."
    },
    {
        "id": "CLIMATE-01",
        "topic": "Indian Monsoon Patterns & Rainfall Normals",
        "category": "Climate Information",
        "keywords": ["monsoon", "june", "july", "august", "september", "historical", "rainfall", "climate"],
        "content": "Southwest Monsoon accounts for 75-80% of India's annual rainfall between June and September. Normal seasonal rainfall for India is ~880 mm. Konkan Maharashtra receives over 2500 mm, while central Maharashtra receives 700 mm."
    }
]

def search_knowledge_base(query: str, top_k: int = 2) -> List[Dict[str, Any]]:
    """Simple, high-speed keyword and semantic document retriever for Indian weather domain."""
    query_lower = query.lower()
    query_tokens = set(query_lower.split())
    
    scored_docs = []
    for doc in KNOWLEDGE_DOCUMENTS:
        score = 0
        for kw in doc["keywords"]:
            if kw in query_lower:
                score += 3
        for token in query_tokens:
            if token in doc["content"].lower():
                score += 1
                
        if score > 0:
            scored_docs.append((score, doc))
            
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored_docs[:top_k]]
