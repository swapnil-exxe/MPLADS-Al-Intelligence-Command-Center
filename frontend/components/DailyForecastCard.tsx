'use client';

import React from 'react';
import { Calendar, CloudRain } from 'lucide-react';

interface DailyProps {
  daily: any[];
}

export const DailyForecastCard: React.FC<DailyProps> = ({ daily }) => {
  if (!daily || daily.length === 0) return null;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 shadow-lg backdrop-blur-md">
      <div className="flex items-center gap-2 mb-3 border-b border-slate-800 pb-2">
        <Calendar className="w-4 h-4 text-sky-400" />
        <h3 className="text-sm font-semibold text-white">7-Day Weather Outlook</h3>
      </div>

      <div className="space-y-2 text-xs">
        {daily.slice(0, 7).map((day, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between bg-slate-800/40 border border-slate-700/30 p-2 rounded-lg"
          >
            <div className="w-24 font-medium text-slate-300">
              {idx === 0 ? 'Today' : idx === 1 ? 'Tomorrow' : day.date}
            </div>
            <div className="text-base">
              {day.rain_prob > 50 ? '🌧️ Rain' : day.rain_prob > 20 ? '⛅ Partly Cloudy' : '☀️ Sunny'}
            </div>
            <div className="flex items-center gap-1 text-sky-400">
              <CloudRain className="w-3 h-3" />
              <span>{day.rain_prob}% ({day.rain_sum}mm)</span>
            </div>
            <div className="font-semibold text-white">
              {day.temp_max}° / <span className="text-slate-400">{day.temp_min}°C</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
