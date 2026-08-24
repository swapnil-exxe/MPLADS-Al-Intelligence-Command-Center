"use client";

import React, { useState } from 'react';
import { MapPin, Info, ShieldAlert, Users, IndianRupee, ChevronRight } from 'lucide-react';

interface IndiaRiskMapProps {
  stateAnalytics: any[];
  onSelectState: (stateName: string) => void;
}

export default function IndiaRiskMap({ stateAnalytics, onSelectState }: IndiaRiskMapProps) {
  const [hoveredState, setHoveredState] = useState<any | null>(null);

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-gray-800">
        <div>
          <div className="flex items-center space-x-2">
            <MapPin className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-white tracking-wide">INDIA STATE ALLOCATION & RISK MAP</h2>
          </div>
          <p className="text-xs text-gray-400 mt-0.5">
            Geographic distribution of official MP allocations across 36 States & Union Territories.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono bg-gray-900 px-3 py-1.5 rounded-lg border border-gray-800">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
          <span className="text-gray-300">36 States/UTs Active</span>
        </div>
      </div>

      {/* Main Grid: Interactive State Table / Cards + Detail Inspector */}
      <div className="mt-4 grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* State Rankings Grid (2 Cols) */}
        <div className="lg:col-span-2 space-y-2 max-h-[380px] overflow-y-auto pr-1">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {stateAnalytics.map((st) => {
              const hasAnomaly = st.deviating_allocation_count > 0 || st.missing_mp_count > 0;
              const cardBg = hasAnomaly ? 'bg-gray-900/90 border-gray-800 hover:border-indigo-600' : 'bg-gray-900/50 border-gray-800/60 hover:border-gray-700';

              return (
                <div
                  key={st.state}
                  onMouseEnter={() => setHoveredState(st)}
                  onClick={() => onSelectState(st.state)}
                  className={`p-3 rounded-lg border transition-all cursor-pointer flex flex-col justify-between ${cardBg}`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-xs text-white tracking-wide">{st.state}</span>
                    <span className="text-[10px] font-mono bg-indigo-950 text-indigo-300 px-1.5 py-0.5 rounded border border-indigo-800/60">
                      {st.mp_count} MPs
                    </span>
                  </div>

                  <div className="mt-2 flex items-baseline justify-between">
                    <span className="text-sm font-bold font-mono text-emerald-400">
                      ₹{st.total_allocation_crores} Cr
                    </span>
                    <span className="text-[10px] text-gray-400 font-mono">
                      Avg: ₹{(st.mean_allocation_inr / 1e7).toFixed(2)} Cr
                    </span>
                  </div>

                  {/* Anomaly Indicator Pill */}
                  <div className="mt-2 flex items-center justify-between text-[10px] font-mono pt-2 border-t border-gray-800/60">
                    <span className="text-gray-400">Baseline 14.7Cr: {st.baseline_14_7cr_count}</span>
                    {st.deviating_allocation_count > 0 ? (
                      <span className="text-amber-400 font-bold">
                        {st.deviating_allocation_count} Deviating
                      </span>
                    ) : (
                      <span className="text-emerald-400">Standard</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected / Hovered State Intelligence Panel */}
        <div className="bg-gray-900/90 border border-indigo-900/60 rounded-xl p-4 flex flex-col justify-between">
          {hoveredState ? (
            <div className="space-y-4">
              <div className="border-b border-gray-800 pb-3">
                <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-400 font-mono">
                  State Deep-Dive Analysis
                </span>
                <h3 className="text-lg font-bold text-white mt-0.5">{hoveredState.state}</h3>
                <p className="text-xs text-gray-400 font-mono">Official MoSPI Dataset Breakdown</p>
              </div>

              <div className="space-y-2.5 font-mono text-xs">
                <div className="flex justify-between items-center bg-gray-950 p-2 rounded border border-gray-800">
                  <span className="text-gray-400">Total MPs Monitored</span>
                  <span className="font-bold text-white">{hoveredState.mp_count} MPs</span>
                </div>
                <div className="flex justify-between items-center bg-gray-950 p-2 rounded border border-gray-800">
                  <span className="text-gray-400">Total Ingested Allocation</span>
                  <span className="font-bold text-emerald-400">₹{hoveredState.total_allocation_crores} Cr</span>
                </div>
                <div className="flex justify-between items-center bg-gray-950 p-2 rounded border border-gray-800">
                  <span className="text-gray-400">Average Allocation / MP</span>
                  <span className="font-bold text-indigo-300">₹{(hoveredState.mean_allocation_inr / 1e7).toFixed(2)} Cr</span>
                </div>
                <div className="flex justify-between items-center bg-gray-950 p-2 rounded border border-gray-800">
                  <span className="text-gray-400">Standard Baseline (14.7Cr)</span>
                  <span className="font-bold text-blue-300">{hoveredState.baseline_14_7cr_count} MPs</span>
                </div>
                <div className="flex justify-between items-center bg-gray-950 p-2 rounded border border-gray-800">
                  <span className="text-gray-400">Deviating Allocations</span>
                  <span className="font-bold text-amber-400">{hoveredState.deviating_allocation_count} MPs</span>
                </div>
              </div>

              <button
                onClick={() => onSelectState(hoveredState.state)}
                className="w-full mt-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2 px-3 rounded-lg text-xs transition-colors flex items-center justify-center space-x-1.5"
              >
                <span>Filter MPs for {hoveredState.state}</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500 space-y-2">
              <MapPin className="w-8 h-8 text-gray-600 mx-auto stroke-1" />
              <p className="text-xs">Hover over any state card to inspect state-level financial breakdown.</p>
            </div>
          )}

          <div className="mt-4 pt-3 border-t border-gray-800 text-[10px] text-gray-500 font-mono flex items-center space-x-1">
            <Info className="w-3 h-3 text-gray-400 shrink-0" />
            <span>State metrics calculated strictly from official dataset</span>
          </div>
        </div>
      </div>
    </div>
  );
}
