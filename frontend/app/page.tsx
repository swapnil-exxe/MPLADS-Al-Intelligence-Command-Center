'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { EmergencyOverlay } from '@/components/EmergencyOverlay';
import { MetricBar } from '@/components/MetricBar';
import { RiskMeter } from '@/components/RiskMeter';
import { WeatherMap } from '@/components/WeatherMap';
import { HourlyForecastCard } from '@/components/HourlyForecastCard';
import { DailyForecastCard } from '@/components/DailyForecastCard';
import { ChatContainer } from '@/components/ChatContainer';
import { fetchCurrentWeather, fetchForecast, fetchRiskAssessment, sendChatMessage } from '@/lib/api';

export default function Home() {
  const [language, setLanguage] = useState<string>('en');
  const [location, setLocation] = useState({ name: 'Mumbai', lat: 19.0760, lon: 72.8777 });
  const [weather, setWeather] = useState<any>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [riskData, setRiskData] = useState<any>(null);
  const [isEmergencySimulated, setIsEmergencySimulated] = useState<boolean>(false);

  // Initial Data Ingestion
  useEffect(() => {
    loadWeatherData(location.lat, location.lon, location.name);
  }, [location]);

  const loadWeatherData = async (lat: number, lon: number, name: string) => {
    const w = await fetchCurrentWeather(lat, lon, name);
    const f = await fetchForecast(lat, lon, 7);
    const r = await fetchRiskAssessment(lat, lon);

    if (w) setWeather(w);
    if (f) setForecast(f);
    if (r) setRiskData(r);
  };

  const handleMapClick = async (lat: number, lon: number) => {
    // Reverse geocode or update location
    const newLoc = { name: `Location (${lat.toFixed(2)}, ${lon.toFixed(2)})`, lat, lon };
    setLocation(newLoc);
  };

  const handleSendMessage = async (msg: string) => {
    const res = await sendChatMessage(msg, language, location);
    if (res && res.weather) {
      setWeather(res.weather);
    }
    if (res && res.forecast) {
      setForecast(res.forecast);
    }
    if (res && res.risk) {
      setRiskData(res.risk);
    }
    return res;
  };

  const toggleSimulateEmergency = () => {
    if (!isEmergencySimulated) {
      // Simulate Puri cyclone emergency location
      setLocation({ name: "Puri", lat: 19.8135, lon: 85.8312 });
      setIsEmergencySimulated(true);
    } else {
      setLocation({ name: "Mumbai", lat: 19.0760, lon: 72.8777 });
      setIsEmergencySimulated(false);
    }
  };

  const isEmergencyActive = isEmergencySimulated || (riskData && riskData.is_emergency);

  return (
    <main className={`min-h-screen transition-colors duration-500 pb-10 ${
      isEmergencyActive ? 'bg-slate-950 border-t-4 border-red-600' : 'bg-slate-950'
    }`}>
      <Header
        language={language}
        setLanguage={setLanguage}
        isEmergency={isEmergencyActive}
        onSimulateEmergency={toggleSimulateEmergency}
      />

      <div className="max-w-7xl mx-auto px-4 pt-4 space-y-4">
        {/* Dynamic Emergency Command Banner */}
        <EmergencyOverlay
          isEmergency={isEmergencyActive}
          riskData={riskData}
          locationName={location.name}
        />

        {/* Top Weather Metrics Bar */}
        <MetricBar weather={weather} locationName={location.name} />

        {/* Main Grid Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Left Column: Interactive GIS Map & Risk Meter & Forecasts (7 cols) */}
          <div className="lg:col-span-7 space-y-4">
            <WeatherMap location={location} onMapClick={handleMapClick} />
            <RiskMeter riskData={riskData} />
            <HourlyForecastCard hourly={forecast?.hourly || []} />
            <DailyForecastCard daily={forecast?.daily || []} />
          </div>

          {/* Right Column: Conversational AI Chat Window (5 cols) */}
          <div className="lg:col-span-5">
            <div className="sticky top-4">
              <ChatContainer language={language} onSendMessage={handleSendMessage} />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
