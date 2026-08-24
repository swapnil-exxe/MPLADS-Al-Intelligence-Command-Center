import random
from typing import List, Dict, Any, Optional

DISCLOSURE_LABEL = "DEMO SIMULATION — NOT DERIVED FROM OFFICIAL MPLADS DATA"

class DemoDataService:
    """
    Isolated Demo Simulation Layer for project-level features (work descriptions, physical progress,
    contractor networks, duplicate works) required for UI demonstration.
    
    STRICT COMPLIANCE:
    - Never combined with official MoSPI allocation totals or MP rankings.
    - Every returned record contains explicit disclosure metadata.
    """
    
    CATEGORIES = ["Sanitation & Water", "Roads & Bridges", "School Infrastructure", "Healthcare Facilities", "Community Halls", "Solar Street Lighting"]
    AGENCIES = ["Public Works Department (PWD)", "District Rural Development Agency (DRDA)", "Municipal Corporation", "Zilla Parishad", "Irrigation Division"]
    CONTRACTORS = [
        "Apex Infrastructure Pvt Ltd",
        "National Civil Construction Corp",
        "Vanguard Developers",
        "Bharat Infra Projects",
        "Sunlight Earthworks Ltd",
        "Om Sai Construction Agency"
    ]
    
    def __init__(self):
        self.demo_projects: List[Dict[str, Any]] = []
        self._generate_demo_dataset()
        
    def _generate_demo_dataset(self):
        random.seed(42)
        categories = self.CATEGORIES
        agencies = self.AGENCIES
        contractors = self.CONTRACTORS
        
        # Create 100 isolated demo projects
        for i in range(1, 101):
            p_id = f"PRJ_DEMO_{str(i).zfill(3)}"
            cost = random.choice([2500000, 5000000, 7500000, 10000000, 15000000, 25000000, 50000000])
            exp = int(cost * random.uniform(0.1, 1.1))
            prog = random.randint(10, 100)
            
            # Anomaly & Fraud Pattern Flagging
            is_duplicate = (i in [14, 15, 42, 43, 78])
            is_cost_overrun = (exp > cost)
            is_contractor_conc = (contractor_name := random.choice(contractors)) == "Apex Infrastructure Pvt Ltd" and (i % 3 == 0)
            
            risk_pts = 0
            risk_factors = []
            if is_duplicate:
                risk_pts += 45
                risk_factors.append("Duplicate Work Description Detected across adjacent sanctions")
            if is_cost_overrun:
                risk_pts += 35
                risk_factors.append(f"Expenditure (₹{exp/1e5:.1f}L) exceeds Sanctioned Limit (₹{cost/1e5:.1f}L)")
            if is_contractor_conc:
                risk_pts += 25
                risk_factors.append(f"High Contractor Concentration ({contractor_name} holds >30% sector allocation)")
            if prog < 30 and exp > (cost * 0.7):
                risk_pts += 30
                risk_factors.append(f"Physical Progress Lag ({prog}% completion vs {int(exp/cost*100)}% funds disbursed)")
                
            risk_score = min(risk_pts, 98)
            risk_level = "CRITICAL" if risk_score >= 80 else ("HIGH" if risk_score >= 60 else ("MEDIUM" if risk_score >= 30 else "LOW"))
            
            self.demo_projects.append({
                "project_id": p_id,
                "work_title": f"Construction of {random.choice(categories)} at Sector-{random.randint(1, 12)}",
                "category": random.choice(categories),
                "sanctioned_amount_inr": cost,
                "expenditure_amount_inr": exp,
                "physical_progress_pct": prog,
                "implementing_agency": random.choice(agencies),
                "contractor_name": contractor_name,
                "sanction_date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "simulated_risk_score": risk_score,
                "simulated_risk_level": risk_level,
                "simulated_risk_factors": risk_factors,
                "is_demo_simulation": True,
                "disclosure_notice": DISCLOSURE_LABEL
            })

    def get_demo_projects(self, category: Optional[str] = None, risk_level: Optional[str] = None) -> List[Dict[str, Any]]:
        res = self.demo_projects
        if category and category.lower() != "all":
            res = [p for p in res if p['category'].lower() == category.lower()]
        if risk_level and risk_level.lower() != "all":
            res = [p for p in res if p['simulated_risk_level'].lower() == risk_level.lower()]
        return res

    def get_demo_project_by_id(self, p_id: str) -> Optional[Dict[str, Any]]:
        for p in self.demo_projects:
            if p['project_id'] == p_id:
                return p
        return None

    def get_demo_fraud_graph(self) -> Dict[str, Any]:
        """Returns entity relationship graph nodes and edges for demo fraud detection view."""
        nodes = [
            {"id": "CONTRACTOR_01", "label": "Apex Infrastructure Pvt Ltd", "type": "Contractor", "risk": "HIGH"},
            {"id": "CONTRACTOR_02", "label": "National Civil Corp", "type": "Contractor", "risk": "LOW"},
            {"id": "AGENCY_01", "label": "PWD Division 4", "type": "ImplementingAgency", "risk": "MEDIUM"},
            {"id": "PROJECT_14", "label": "PRJ_DEMO_014 (Water Tank)", "type": "Project", "risk": "CRITICAL"},
            {"id": "PROJECT_15", "label": "PRJ_DEMO_015 (Water Pipe)", "type": "Project", "risk": "CRITICAL"},
            {"id": "PROJECT_42", "label": "PRJ_DEMO_042 (Road Patch)", "type": "Project", "risk": "HIGH"}
        ]
        edges = [
            {"source": "CONTRACTOR_01", "target": "PROJECT_14", "relation": "Awarded To", "alert": "Duplicate Work Cluster"},
            {"source": "CONTRACTOR_01", "target": "PROJECT_15", "relation": "Awarded To", "alert": "Duplicate Work Cluster"},
            {"source": "CONTRACTOR_01", "target": "PROJECT_42", "relation": "Awarded To", "alert": "75% Tender Share"},
            {"source": "AGENCY_01", "target": "PROJECT_14", "relation": "Sanctioned By", "alert": "Same Officer Approval"},
            {"source": "AGENCY_01", "target": "PROJECT_15", "relation": "Sanctioned By", "alert": "Same Officer Approval"}
        ]
        return {
            "nodes": nodes,
            "edges": edges,
            "is_demo_simulation": True,
            "disclosure_notice": DISCLOSURE_LABEL
        }

demo_data_service = DemoDataService()
