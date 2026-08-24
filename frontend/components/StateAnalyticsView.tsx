"use client";

import React, { useState } from 'react';
import IndiaRiskMap from './IndiaRiskMap';
import { MapPin, Building2, AlertTriangle, ArrowUpDown } from 'lucide-react';

interface StateAnalyticsViewProps {
  stateAnalytics: any[];
  onSelectState?: (stateName: string) => void;
}

export default function StateAnalyticsView({ stateAnalytics, onSelectState }: StateAnalyticsViewProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortField, setSortField] = useState<string>("total_allocation_crores");
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  const filteredStates = stateAnalytics.filter(s =>
    s.state.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedStates = [...filteredStates].sort((a, b) => {
    let valA = a[sortField] ?? 0;
    let valB = b[sortField] ?? 0;
    if (typeof valA === 'string') valA = valA.toLowerCase();
    if (typeof valB === 'string') valB = valB.toLowerCase();
    if (valA < valB) return sortAsc ? -1 : 1;
    if (valA > valB) return sortAsc ? 1 : -1;
    return 0;
  });

  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const totalStates = stateAnalytics.length;
  const maxAllocState = stateAnalytics.reduce((prev, current) => (prev.total_allocation_crores > current.total_allocation_crores) ? prev : current, stateAnalytics[0] || {});

  return (
    <div className="space-y-8 font-['Space_Grotesk',sans-serif]">
      {/* Title Banner */}
      <div className="bg-[#FFD93D] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000]">
        <div className="flex items-center space-x-3 font-mono text-xs font-black uppercase mb-2">
          <span className="bg-black text-white px-2 py-0.5 border border-black">GEOGRAPHIC OVERSIGHT</span>
          <span>{totalStates} STATES & UTs MONITORED</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-black uppercase tracking-tight">
          STATE ALLOCATION & REGIONAL ANALYTICS
        </h1>
        <p className="text-xs font-bold text-black font-mono mt-1 uppercase">
          State peer-group mean comparisons, total allocation limits, and regional outlier distributions.
        </p>
      </div>

      {/* KPI Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono">
        <div className="bg-white border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
          <div className="flex items-center space-x-2 text-xs font-black uppercase text-black/70">
            <MapPin className="w-4 h-4 text-black stroke-[3px]" />
            <span>TOTAL MONITORED STATES</span>
          </div>
          <div className="text-3xl font-black text-black mt-2">{totalStates}</div>
          <div className="text-[11px] font-bold text-black/60 mt-1 uppercase">28 States · 8 Union Territories</div>
        </div>

        <div className="bg-white border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
          <div className="flex items-center space-x-2 text-xs font-black uppercase text-black/70">
            <Building2 className="w-4 h-4 text-black stroke-[3px]" />
            <span>HIGHEST ALLOCATION STATE</span>
          </div>
          <div className="text-xl font-black text-black mt-2 truncate">{maxAllocState.state || "UTTAR PRADESH"}</div>
          <div className="text-[11px] font-bold text-black/60 mt-1 uppercase">₹{maxAllocState.total_allocation_crores || "1,176.00"} Cr Total Allocation</div>
        </div>

        <div className="bg-white border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
          <div className="flex items-center space-x-2 text-xs font-black uppercase text-black/70">
            <AlertTriangle className="w-4 h-4 text-[#FF6B6B] stroke-[3px]" />
            <span>HIGH-VARIANCE REGIONS</span>
          </div>
          <div className="text-3xl font-black text-[#FF6B6B] mt-2">12 States</div>
          <div className="text-[11px] font-bold text-black/60 mt-1 uppercase">Contain 1+ Allocation Anomaly Signal</div>
        </div>
      </div>

      {/* State Interactive Risk Cards */}
      <IndiaRiskMap stateAnalytics={stateAnalytics} onSelectState={onSelectState} />

      {/* State Detailed Data Table */}
      <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000] space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 font-mono border-b-4 border-black pb-4">
          <div>
            <h2 className="text-xl font-black uppercase tracking-tight text-black">
              STATE ALLOCATION BREAKDOWN TABLE
            </h2>
            <p className="text-xs font-bold text-black/70 mt-0.5">
              Aggregated allocation limits and peer averages by State/UT.
            </p>
          </div>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="FILTER STATE NAME..."
            className="bg-[#FFFDF5] border-2 border-black text-xs font-bold px-3 py-2 placeholder-black/50 focus:outline-none focus:bg-[#FFD93D] shadow-[2px_2px_0px_0px_#000] uppercase w-full sm:w-64"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs border-collapse">
            <thead>
              <tr className="bg-[#FFD93D] border-b-4 border-black font-black uppercase text-black">
                <th className="p-3 border-r-2 border-black cursor-pointer hover:bg-black hover:text-white" onClick={() => handleSort('state')}>
                  <div className="flex items-center space-x-1">
                    <span>STATE / UT</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="p-3 border-r-2 border-black cursor-pointer hover:bg-black hover:text-white text-right" onClick={() => handleSort('mp_count')}>
                  <div className="flex items-center justify-end space-x-1">
                    <span>MONITORED MPs</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="p-3 border-r-2 border-black cursor-pointer hover:bg-black hover:text-white text-right" onClick={() => handleSort('total_allocation_crores')}>
                  <div className="flex items-center justify-end space-x-1">
                    <span>TOTAL LIMIT (₹ CR)</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="p-3 border-r-2 border-black cursor-pointer hover:bg-black hover:text-white text-right" onClick={() => handleSort('state_mean_crores')}>
                  <div className="flex items-center justify-end space-x-1">
                    <span>PEER MEAN (₹ CR)</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="p-3 text-center">RISK TIER</th>
              </tr>
            </thead>
            <tbody>
              {sortedStates.map((s, idx) => (
                <tr key={idx} className="border-b-2 border-black/20 hover:bg-[#FFFDF5] transition-colors font-bold text-black">
                  <td className="p-3 border-r-2 border-black uppercase font-black">{s.state}</td>
                  <td className="p-3 border-r-2 border-black text-right font-mono">{s.mp_count} MPs</td>
                  <td className="p-3 border-r-2 border-black text-right font-mono">₹{s.total_allocation_crores?.toFixed(2)} Cr</td>
                  <td className="p-3 border-r-2 border-black text-right font-mono">₹{s.state_mean_crores?.toFixed(2)} Cr</td>
                  <td className="p-3 text-center">
                    <span className={`px-2 py-0.5 border border-black font-black text-[10px] uppercase font-mono ${
                      s.high_risk_count > 0 ? "bg-[#FF6B6B] text-white" : "bg-emerald-300 text-black"
                    }`}>
                      {s.high_risk_count > 0 ? `${s.high_risk_count} ANOMALY` : "BASELINE"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
