'use client';

import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle, Info } from 'lucide-react';

interface RiskMeterProps {
  riskData: any;
}

export const RiskMeter: React.FC<RiskMeterProps> = ({ riskData }) => {
  if (!riskData) return null;

  const score = riskData.overall_score || 0;
  const level = riskData.risk_level || "LOW";
  const factors = riskData.transparent_factors || [];

  let badgeBg = "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
  let barBg = "bg-emerald-500";
  if (level === "MODERATE") {
    badgeBg = "bg-yellow-500/20 text-yellow-300 border-yellow-500/30";
    barBg = "bg-yellow-500";
  } else if (level === "HIGH") {
    badgeBg = "bg-orange-500/20 text-orange-300 border-orange-500/30";
    barBg = "bg-orange-500";
  } else if (level === "EXTREME") {
    badgeBg = "bg-red-600 text-white border-red-500 animate-pulse";
    barBg = "bg-red-600";
  }

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 shadow-lg backdrop-blur-md">
      <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
          <h3 className="text-sm font-semibold text-white">Weather Risk Matrix Engine</h3>
        </div>
        <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold border ${badgeBg}`}>
          {level} RISK ({score}/100)
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-800 rounded-full h-2.5 mb-3 overflow-hidden">
        <div
          className={`h-2.5 rounded-full transition-all duration-700 ${barBg}`}
          style={{ width: `${Math.max(5, score)}%` }}
        ></div>
      </div>

      {/* Categories Breakdown */}
      <div className="grid grid-cols-3 gap-2 text-center text-xs mb-3">
        <div className="bg-slate-800/50 p-2 rounded border border-slate-700/40">
          <div className="text-slate-400 text-[10px]">Flood Risk</div>
          <div className="font-bold text-white">{riskData.category_scores?.flood || 0}</div>
        </div>
        <div className="bg-slate-800/50 p-2 rounded border border-slate-700/40">
          <div className="text-slate-400 text-[10px]">Heatwave Index</div>
          <div className="font-bold text-white">{riskData.category_scores?.heatwave || 0}</div>
        </div>
        <div className="bg-slate-800/50 p-2 rounded border border-slate-700/40">
          <div className="text-slate-400 text-[10px]">Wind / Storm</div>
          <div className="font-bold text-white">{riskData.category_scores?.wind_storm || 0}</div>
        </div>
      </div>

      {/* Transparent Triggers Breakdown */}
      <div className="text-xs">
        <div className="flex items-center gap-1 text-slate-400 mb-1 font-medium">
          <Info className="w-3.5 h-3.5 text-sky-400" />
          Explainable Factor Breakdown:
        </div>
        <ul className="space-y-1">
          {factors.map((factor: string, idx: number) => (
            <li key={idx} className="flex items-start gap-1.5 text-slate-300 text-[11px]">
              <span className="text-amber-400 mt-0.5">•</span>
              <span>{factor}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
