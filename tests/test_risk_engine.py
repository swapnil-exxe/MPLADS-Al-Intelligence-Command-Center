import pytest
from app.core.risk_engine import calculate_weather_risk

def test_risk_calculation_normal():
    w_data = {"temperature": 28.0, "wind_speed": 10.0, "soil_moisture": 0.4, "rain": 0.0}
    f_data = {"hourly": [{"precipitation": 0.0, "wind_speed": 10.0} for _ in range(24)]}
    res = calculate_weather_risk(w_data, f_data, 19.0760, 72.8777)
    
    assert res["risk_level"] in ["LOW", "MODERATE"]
    assert "overall_score" in res

def test_risk_calculation_extreme_puri():
    # Puri has an active Red alert in IMD feed simulation
    w_data = {"temperature": 26.0, "wind_speed": 50.0, "soil_moisture": 0.8, "rain": 25.0}
    f_data = {"hourly": [{"precipitation": 12.0, "wind_speed": 65.0} for _ in range(24)]}
    res = calculate_weather_risk(w_data, f_data, 19.8135, 85.8312)
    
    assert res["risk_level"] == "EXTREME"
    assert res["is_emergency"] is True
