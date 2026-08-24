"use client";

import React from 'react';

interface OverviewMetricsProps {
  kpis: any | null;
  highRiskCount?: number;
}

export default function OverviewMetrics({ kpis, highRiskCount = 26 }: OverviewMetricsProps) {
  if (!kpis) return null;

  return (
    <div className="bg-[#FFFDF5] border-4 border-black p-4 shadow-[8px_8px_0px_0px_#000000] font-['Space_Grotesk',sans-serif]">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 divide-y md:divide-y-0 md:divide-x-4 divide-black">
        {/* Metric 1 */}
        <div className="p-2 space-y-1">
          <span className="text-[11px] font-black text-black uppercase tracking-wider block bg-[#C4B5FD] px-2 py-0.5 border-2 border-black inline-block font-mono">
            MONITORED MPs
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-black text-black tracking-tight">{kpis.total_mp_records}</span>
            <span className="text-xs font-bold text-black uppercase font-mono">RECORDS</span>
          </div>
          <span className="text-[10px] font-bold text-black block font-mono">389 Baseline (₹14.70 Cr)</span>
        </div>

        {/* Metric 2 */}
        <div className="p-2 md:pl-6 space-y-1">
          <span className="text-[11px] font-black text-black uppercase tracking-wider block bg-[#FFD93D] px-2 py-0.5 border-2 border-black inline-block font-mono">
            TOTAL ALLOCATION
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-black text-black tracking-tight">₹{kpis.total_allocation_crores}</span>
            <span className="text-xs font-bold text-black uppercase font-mono">Cr</span>
          </div>
          <span className="text-[10px] font-bold text-black block font-mono">₹83,06,21,04,294.53</span>
        </div>

        {/* Metric 3 */}
        <div className="p-2 md:pl-6 space-y-1">
          <span className="text-[11px] font-black text-black uppercase tracking-wider block bg-white px-2 py-0.5 border-2 border-black inline-block font-mono">
            STATES & UTs
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-black text-black tracking-tight">{kpis.unique_states_count}</span>
            <span className="text-xs font-bold text-black uppercase font-mono">REGIONS</span>
          </div>
          <span className="text-[10px] font-bold text-black block font-mono">542 Constituencies</span>
        </div>

        {/* Metric 4 */}
        <div className="p-2 md:pl-6 space-y-1">
          <span className="text-[11px] font-black text-black uppercase tracking-wider block bg-[#FFD93D] px-2 py-0.5 border-2 border-black inline-block font-mono">
            ANOMALY SIGNALS
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-black text-black tracking-tight">45</span>
            <span className="text-xs font-bold text-black uppercase font-mono">OUTLIERS</span>
          </div>
          <span className="text-[10px] font-bold text-black block font-mono">Isolation Forest + LOF</span>
        </div>

        {/* Metric 5 */}
        <div className="p-2 md:pl-6 space-y-1">
          <span className="text-[11px] font-black text-white uppercase tracking-wider block bg-[#FF6B6B] px-2 py-0.5 border-2 border-black inline-block font-mono">
            HIGH PRIORITY
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-black text-[#FF6B6B] tracking-tight">{highRiskCount}</span>
            <span className="text-xs font-bold text-black uppercase font-mono">ACTION REQ</span>
          </div>
          <span className="text-[10px] font-bold text-black block font-mono">1 Critical Data Null</span>
        </div>
      </div>
    </div>
  );
}
