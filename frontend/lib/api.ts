export interface WeatherLocation {
  name: string;
  lat: number;
  lon: number;
}

const API_BASE = 'http://127.0.0.1:8001/api/v1';

export async function fetchCurrentWeather(lat: number, lon: number, locationName: string = "Mumbai") {
  try {
    const res = await fetch(`${API_BASE}/weather/current?lat=${lat}&lon=${lon}&location_name=${encodeURIComponent(locationName)}`);
    if (!res.ok) throw new Error("Failed to fetch weather");
    return await res.json();
  } catch (err) {
    console.error("fetchCurrentWeather error:", err);
    return null;
  }
}

export async function fetchForecast(lat: number, lon: number, days: number = 7) {
  try {
    const res = await fetch(`${API_BASE}/weather/forecast?lat=${lat}&lon=${lon}&days=${days}`);
    if (!res.ok) throw new Error("Failed to fetch forecast");
    return await res.json();
  } catch (err) {
    console.error("fetchForecast error:", err);
    return null;
  }
}

export async function fetchRiskAssessment(lat: number, lon: number) {
  try {
    const res = await fetch(`${API_BASE}/risk/assess?lat=${lat}&lon=${lon}`);
    if (!res.ok) throw new Error("Failed to fetch risk");
    return await res.json();
  } catch (err) {
    console.error("fetchRiskAssessment error:", err);
    return null;
  }
}

export async function sendChatMessage(message: string, language: string, location: { name: string, lat: number, lon: number }) {
  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, language, location })
    });
    if (!res.ok) throw new Error("Failed to send chat");
    return await res.json();
  } catch (err) {
    console.error("sendChatMessage error:", err);
    return null;
  }
}
