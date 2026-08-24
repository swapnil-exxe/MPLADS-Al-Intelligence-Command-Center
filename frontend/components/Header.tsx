'use client';

import React from 'react';
import { CloudLightning, Volume2, Globe, ShieldAlert, Sparkles } from 'lucide-react';

interface HeaderProps {
  language: string;
  setLanguage: (lang: string) => void;
  isEmergency: boolean;
  onSimulateEmergency: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  language,
  setLanguage,
  isEmergency,
  onSimulateEmergency
}) => {
  return (
    <header className={`border-b transition-colors duration-500 px-4 py-3 ${
      isEmergency ? 'bg-emergency-900 border-red-600' : 'bg-slate-900/90 border-slate-800'
    }`}>
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
        {/* Brand Title */}
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-xl ${isEmergency ? 'bg-red-600 animate-pulse' : 'bg-sky-500/20 text-sky-400 border border-sky-500/30'}`}>
            <CloudLightning className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">WEATHERGPT</h1>
              <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-sky-500/20 text-sky-300 border border-sky-500/30">
                SIH26068
              </span>
            </div>
            <p className="text-xs text-slate-400">Conversational AI Weather Intelligence & Decision Support</p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* Emergency Simulator Toggle Button */}
          <button
            onClick={onSimulateEmergency}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              isEmergency
                ? 'bg-red-600 hover:bg-red-700 text-white animate-bounce'
                : 'bg-slate-800 hover:bg-slate-700 text-red-400 border border-red-500/30'
            }`}
          >
            <ShieldAlert className="w-4 h-4" />
            {isEmergency ? 'EMERGENCY MODE ACTIVE' : 'Simulate Disaster Mode'}
          </button>

          {/* Language Selector */}
          <div className="flex items-center gap-1.5 bg-slate-800/80 border border-slate-700 rounded-lg px-2.5 py-1 text-xs">
            <Globe className="w-4 h-4 text-slate-400" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer font-medium"
            >
              <option value="en">English</option>
              <option value="hi">हिंदी (Hindi)</option>
              <option value="mr">मराठी (Marathi)</option>
            </select>
          </div>
        </div>
      </div>
    </header>
  );
};
