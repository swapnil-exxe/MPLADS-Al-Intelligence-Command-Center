'use client';

import React from 'react';
import { Clock, CloudRain } from 'lucide-react';

interface HourlyProps {
  hourly: any[];
}

export const HourlyForecastCard: React.FC<HourlyProps> = ({ hourly }) => {
  if (!hourly || hourly.length === 0) return null;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 shadow-lg backdrop-blur-md">
      <div className="flex items-center gap-2 mb-3 border-b border-slate-800 pb-2">
        <Clock className="w-4 h-4 text-sky-400" />
        <h3 className="text-sm font-semibold text-white">24-Hour Forecast Timeline</h3>
      </div>

      <div className="flex gap-2.5 overflow-x-auto pb-2 scrollbar-thin">
        {hourly.slice(0, 16).map((item, idx) => (
          <div
            key={idx}
            className="flex-shrink-0 w-20 bg-slate-800/60 border border-slate-700/50 rounded-lg p-2 text-center text-xs"
          >
            <div className="text-slate-400 font-medium text-[11px]">{item.time}</div>
            <div className="my-1 text-base">
              {item.rain_prob > 50 ? '🌧️' : item.rain_prob > 20 ? '⛅' : '☀️'}
            </div>
            <div className="font-bold text-white text-sm">{item.temperature}°C</div>
            <div className="flex items-center justify-center gap-0.5 text-[10px] text-sky-400 mt-1">
              <CloudRain className="w-3 h-3" />
              <span>{item.rain_prob}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
