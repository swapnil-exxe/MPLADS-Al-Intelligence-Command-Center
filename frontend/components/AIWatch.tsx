"use client";

import React, { useState } from 'react';
import { ArrowUpRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface AIWatchProps {
  anomalies: any[];
  onSelectMP: (mp: any) => void;
}

export default function AIWatch({ anomalies, onSelectMP }: AIWatchProps) {
  const [riskFilter, setRiskFilter] = useState<string>("ALL");

  const filtered = anomalies.filter(item => {
    if (riskFilter === "ALL") return item.risk_level === 'HIGH' || item.risk_level === 'CRITICAL' || item.risk_level === 'MEDIUM';
    return item.risk_level === riskFilter;
  });

  const highPriorityCount = anomalies.filter(a => a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL').length;
  const criticalCount = anomalies.filter(a => a.risk_level === 'CRITICAL').length;
  const mediumCount = anomalies.filter(a => a.risk_level === 'MEDIUM').length;

  return (
    <div className="space-y-6 font-['Space_Grotesk',sans-serif]">
      {/* NEO-BRUTALIST HERO STRUCTURAL PANEL */}
      <div className="bg-black text-white border-4 border-black p-8 shadow-[12px_12px_0px_0px_#FFD93D] relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 relative z-10 font-mono">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <span className="w-3 h-3 rounded-full bg-[#FFD93D] border border-black animate-pulse"></span>
              <span className="text-xs font-black text-[#FFD93D] tracking-widest uppercase bg-black px-2 py-0.5 border border-[#FFD93D]">
                AI WATCH · SYSTEM MONITORING ACTIVE
              </span>
            </div>
            
            <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight leading-none uppercase font-sans">
              45 <span className="bg-[#FFD93D] text-black px-2 py-0.5 border-2 border-white inline-block -rotate-1">ANOMALY</span> SIGNALS DETECTED
            </h2>
            
            <p className="text-xs text-gray-300 max-w-2xl leading-relaxed font-sans font-medium">
              Isolation Forest and LOF statistical density models continuously screen 543 MP entitlement limits against the standard ₹14.70 Cr baseline and state peer distributions.
            </p>

            <div className="flex items-center space-x-4 text-xs font-bold pt-1">
              <span className="bg-[#FF6B6B] text-black px-2 py-1 border border-white">Isolation Forest ✓</span>
              <span className="bg-[#C4B5FD] text-black px-2 py-1 border border-white">Local Outlier Factor ✓</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 shrink-0 font-mono">
            <div className="text-left md:text-right border-l-4 md:border-l-0 md:border-r-4 border-white pl-4 md:pl-0 md:pr-6 space-y-1">
              <span className="text-xs text-gray-300 uppercase block font-black">HIGH PRIORITY</span>
              <span className="text-3xl font-black text-[#FF6B6B]">{highPriorityCount} CASES</span>
            </div>

            <button
              onClick={() => {
                if (filtered.length > 0) onSelectMP(filtered[0]);
              }}
              className="bg-[#FF6B6B] hover:bg-white text-black text-xs font-black px-6 py-4 border-4 border-white shadow-[4px_4px_0px_0px_#FFD93D] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all flex items-center space-x-2 uppercase font-sans tracking-wide"
            >
              <span>INVESTIGATE HIGH-RISK CASES</span>
              <ArrowUpRight className="w-5 h-5 stroke-[4px]" />
            </button>
          </div>
        </div>
      </div>

      {/* Stream Header & Filter Pills */}
      <div className="flex items-center justify-between pt-2 border-b-4 border-black pb-3">
        <span className="text-xs font-black font-mono text-black uppercase tracking-wider">
          LIVE ANOMALY STREAM ({filtered.length} FLAGGED)
        </span>

        <div className="flex items-center space-x-2 text-xs font-black font-mono">
          <button
            onClick={() => setRiskFilter("ALL")}
            className={`px-3 py-1.5 border-2 border-black transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              riskFilter === "ALL" ? "bg-[#FFD93D] text-black shadow-[3px_3px_0px_0px_#000]" : "bg-white text-black hover:bg-gray-100"
            }`}
          >
            ALL ({anomalies.filter(a=>a.risk_level!=='LOW').length})
          </button>
          <button
            onClick={() => setRiskFilter("CRITICAL")}
            className={`px-3 py-1.5 border-2 border-black transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              riskFilter === "CRITICAL" ? "bg-[#FF6B6B] text-white shadow-[3px_3px_0px_0px_#000]" : "bg-white text-[#FF6B6B] hover:bg-red-50"
            }`}
          >
            CRITICAL ({criticalCount})
          </button>
          <button
            onClick={() => setRiskFilter("HIGH")}
            className={`px-3 py-1.5 border-2 border-black transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              riskFilter === "HIGH" ? "bg-[#FF6B6B] text-black shadow-[3px_3px_0px_0px_#000]" : "bg-white text-rose-600 hover:bg-rose-50"
            }`}
          >
            HIGH ({highPriorityCount - criticalCount})
          </button>
          <button
            onClick={() => setRiskFilter("MEDIUM")}
            className={`px-3 py-1.5 border-2 border-black transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              riskFilter === "MEDIUM" ? "bg-[#FFD93D] text-black shadow-[3px_3px_0px_0px_#000]" : "bg-white text-amber-800 hover:bg-amber-50"
            }`}
          >
            MEDIUM ({mediumCount})
          </button>
        </div>
      </div>

      {/* Stream Items List */}
      <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
        <AnimatePresence mode="popLayout">
          {filtered.slice(0, 10).map((item) => (
            <motion.div
              key={item.mp_id}
              layout
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.15 }}
              onClick={() => onSelectMP(item)}
              className="group bg-white hover:bg-[#FFD93D] border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000] hover:shadow-[8px_8px_0px_0px_#000] transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none"
            >
              <div className="space-y-1 font-mono">
                <div className="flex items-center space-x-3">
                  <span className={`text-[10px] font-black px-2 py-0.5 border border-black uppercase tracking-wider ${
                    item.risk_level === 'CRITICAL' ? 'bg-[#FF6B6B] text-white' :
                    item.risk_level === 'HIGH' ? 'bg-[#FF6B6B] text-black' :
                    'bg-[#FFD93D] text-black'
                  }`}>
                    {item.risk_level} · RISK {item.risk_score}
                  </span>

                  <span className="text-base font-black text-black group-hover:underline uppercase font-sans">
                    {item.mp_name}
                  </span>
                </div>

                <div className="text-xs text-black font-bold flex items-center space-x-2">
                  <span>{item.constituency}</span>
                  <span>·</span>
                  <span>{item.state}</span>
                  <span>·</span>
                  <span className="bg-white px-1.5 py-0.2 border border-black font-black">
                    {item.allocated_amount_crores ? `₹${item.allocated_amount_crores} Cr` : "ALLOCATION MISSING"}
                  </span>
                </div>

                {item.evidence_breakdown && item.evidence_breakdown.length > 0 && (
                  <p className="text-xs text-black pt-0.5 truncate max-w-2xl font-sans font-medium">
                    Evidence: <span className="font-bold">{item.evidence_breakdown[0].description}</span>
                  </p>
                )}
              </div>

              <div className="flex items-center space-x-3 shrink-0 font-mono text-xs font-bold text-black">
                <span className="hidden md:inline bg-white px-2 py-0.5 border border-black">{item.algorithms_triggered.join(", ")}</span>
                <div className="p-2 bg-black group-hover:bg-[#FF6B6B] text-white rounded-none border border-black transition-colors">
                  <ArrowUpRight className="w-4 h-4 stroke-[3px]" />
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
