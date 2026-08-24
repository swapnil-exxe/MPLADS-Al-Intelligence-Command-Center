'use client';

import React from 'react';
import { Thermometer, Droplets, Wind, Sun, Compass, Gauge } from 'lucide-react';

interface MetricBarProps {
  weather: any;
  locationName: string;
}

export const MetricBar: React.FC<MetricBarProps> = ({ weather, locationName }) => {
  if (!weather) return null;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 shadow-lg backdrop-blur-md">
      <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <span className="text-lg">📍</span>
          <h2 className="text-base font-semibold text-white">{locationName}</h2>
          <span className="text-xs text-slate-400">Live Weather Metrics</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          Verified Open-Meteo Data
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 text-xs">
        {/* Temp */}
        <div className="bg-slate-800/60 border border-slate-700/50 p-2.5 rounded-lg flex items-center gap-2.5">
          <div className="p-2 bg-amber-500/10 text-amber-400 rounded-md">
            <Thermometer className="w-4 h-4" />
          </div>
          <div>
            <div className="text-slate-400 text-[10px]">Temperature</div>
            <div className="text-sm font-bold text-white">{weather.temperature}°C</div>
            <div className="text-[10px] text-slate-400">Feels {weather.feels_like}°C</div>
          </div>
        </div>

        {/* Humidity */}
        <div className="bg-slate-800/60 border border-slate-700/50 p-2.5 rounded-lg flex items-center gap-2.5">
          <div className="p-2 bg-blue-500/10 text-blue-400 rounded-md">
            <Droplets className="w-4 h-4" />
          </div>
          <div>
            <div className="text-slate-400 text-[10px]">Humidity</div>
            <div className="text-sm font-bold text-white">{weather.humidity}%</div>
            <div className="text-[10px] text-slate-400">Rain {weather.precipitation} mm</div>
          </div>
        </div>

        {/* Wind */}
        <div className="bg-slate-800/60 border border-slate-700/50 p-2.5 rounded-lg flex items-center gap-2.5">
          <div className="p-2 bg-cyan-500/10 text-cyan-400 rounded-md">
            <Wind className="w-4 h-4" />
          </div>
          <div>
            <div className="text-slate-400 text-[10px]">Wind Speed</div>
            <div className="text-sm font-bold text-white">{weather.wind_speed} km/h</div>
            <div className="text-[10px] text-slate-400">Dir {weather.wind_direction}°</div>
          </div>
        </div>

        {/* UV Index */}
        <div className="bg-slate-800/60 border border-slate-700/50 p-2.5 rounded-lg flex items-center gap-2.5">
          <div className="p-2 bg-purple-500/10 text-purple-400 rounded-md">
            <Sun className="w-4 h-4" />
          </div>
          <div>
            <div className="text-slate-400 text-[10px]">UV Index</div>
            <div className="text-sm font-bold text-white">{weather.uv_index}</div>
            <div className="text-[10px] text-purple-400">Moderate</div>
          </div>
        </div>

        {/* Pressure */}
        <div className="bg-slate-800/60 border border-slate-700/50 p-2.5 rounded-lg flex items-center gap-2.5">
          <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-md">
            <Gauge className="w-4 h-4" />
          </div>
          <div>
            <div className="text-slate-400 text-[10px]">Air Pressure</div>
            <div className="text-sm font-bold text-white">{weather.pressure} hPa</div>
            <div className="text-[10px] text-slate-400">Surface level</div>
          </div>
        </div>

        {/* Soil Moisture */}
        <div className="bg-slate-800/60 border border-slate-700/50 p-2.5 rounded-lg flex items-center gap-2.5">
          <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-md">
            <Compass className="w-4 h-4" />
          </div>
          <div>
            <div className="text-slate-400 text-[10px]">Soil Moisture</div>
            <div className="text-sm font-bold text-white">{(weather.soil_moisture * 100).toFixed(0)}%</div>
            <div className="text-[10px] text-slate-400">Top 7cm soil</div>
          </div>
        </div>
      </div>
    </div>
  );
};
