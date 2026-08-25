"use client";

import React, { useState, useEffect } from 'react';
import { AlertTriangle, Search, Filter, ArrowUpDown, ArrowUpRight, ExternalLink } from 'lucide-react';

interface AnomalyMatrixProps {
  mps: any[];
  onSelectMP: (mp: any) => void;
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
}

export default function AnomalyMatrix({ mps, onSelectMP, searchQuery = "", setSearchQuery }: AnomalyMatrixProps) {
  const [search, setSearch] = useState(searchQuery);
  const [filterState, setFilterState] = useState("ALL");
  const [outlierOnly, setOutlierOnly] = useState(false);

  useEffect(() => {
    setSearch(searchQuery);
  }, [searchQuery]);

  const handleLocalSearchChange = (val: string) => {
    setSearch(val);
    if (setSearchQuery) setSearchQuery(val);
  };

  const filtered = mps.filter(m => {
    if (filterState !== "ALL" && m.state !== filterState) return false;
    if (outlierOnly && m.is_baseline) return false;
    if (search) {
      const q = search.toLowerCase();
      const mpNameMatch = m.mp_name ? m.mp_name.toLowerCase().includes(q) : false;
      const constMatch = m.constituency ? m.constituency.toLowerCase().includes(q) : false;
      const stateMatch = m.state ? m.state.toLowerCase().includes(q) : false;
      return mpNameMatch || constMatch || stateMatch;
    }
    return true;
  });

  const statesList = Array.from(new Set(mps.map(m => m.state))).sort();

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl space-y-4">
      {/* Header & Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-gray-800">
        <div>
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <h2 className="text-base font-bold text-white tracking-wide">ALLOCATION ANOMALY & RISK MATRIX</h2>
          </div>
          <p className="text-xs text-gray-400 mt-0.5">
            Tabular directory of all 543 MPs with Isolation Forest, LOF, and Z-Score allocation risk evaluation.
          </p>
        </div>

        {/* Search & Filter Bar */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Search Input */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => handleLocalSearchChange(e.target.value)}
              placeholder="Search MP, Constituency..."
              className="bg-gray-900 border border-gray-700 text-xs rounded-lg pl-8 pr-3 py-1.5 text-white focus:outline-none focus:border-indigo-500 font-mono w-56"
            />
          </div>

          {/* State Filter */}
          <select
            value={filterState}
            onChange={(e) => setFilterState(e.target.value)}
            className="bg-gray-900 border border-gray-700 text-xs rounded-lg px-2.5 py-1.5 text-gray-300 focus:outline-none focus:border-indigo-500 font-mono"
          >
            <option value="ALL">All States ({statesList.length})</option>
            {statesList.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>

          {/* Export Action Buttons */}
          <a
            href={`http://localhost:8001/api/exports/csv${filterState !== 'ALL' ? `?state=${filterState}` : ''}`}
            download
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-[11px] font-bold px-2.5 py-1.5 rounded-lg border border-emerald-500 transition-colors flex items-center gap-1"
          >
            EXPORT CSV
          </a>

          <a
            href={`http://localhost:8001/api/exports/excel${filterState !== 'ALL' ? `?state=${filterState}` : ''}`}
            download
            className="bg-indigo-600 hover:bg-indigo-500 text-white font-mono text-[11px] font-bold px-2.5 py-1.5 rounded-lg border border-indigo-500 transition-colors flex items-center gap-1"
          >
            EXPORT EXCEL
          </a>

          {/* Outlier Checkbox */}
          <label className="flex items-center space-x-1.5 text-xs text-gray-300 font-mono bg-gray-900 border border-gray-700 px-2.5 py-1.5 rounded-lg cursor-pointer">
            <input
              type="checkbox"
              checked={outlierOnly}
              onChange={(e) => setOutlierOnly(e.target.checked)}
              className="rounded bg-gray-950 border-gray-700 text-indigo-600 focus:ring-0"
            />
            <span>Deviating Only</span>
          </label>
        </div>
      </div>

      {/* Matrix Table */}
      <div className="overflow-x-auto max-h-[500px]">
        <table className="w-full text-left border-collapse text-xs font-mono">
          <thead className="bg-gray-900 text-gray-400 uppercase tracking-wider text-[10px] sticky top-0 z-10 border-b border-gray-800">
            <tr>
              <th className="py-2.5 px-3">Sr / ID</th>
              <th className="py-2.5 px-3">Hon'ble MP Name</th>
              <th className="py-2.5 px-3">Constituency</th>
              <th className="py-2.5 px-3">State / UT</th>
              <th className="py-2.5 px-3">Allocated Amount</th>
              <th className="py-2.5 px-3">Baseline Variance</th>
              <th className="py-2.5 px-3">Risk Level</th>
              <th className="py-2.5 px-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/60">
            {filtered.slice(0, 100).map((m) => {
              const isMissing = m.is_missing;
              const riskLvl = m.risk_level || (isMissing ? 'CRITICAL' : (m.allocated_amount_crores > 20 ? 'HIGH' : 'LOW'));
              const badgeBg = riskLvl === 'CRITICAL' ? 'bg-red-950 text-red-300 border-red-800' : (riskLvl === 'HIGH' ? 'bg-rose-950 text-rose-300 border-rose-800' : (riskLvl === 'MEDIUM' ? 'bg-amber-950 text-amber-300 border-amber-800' : 'bg-emerald-950 text-emerald-300 border-emerald-800'));

              return (
                <tr
                  key={m.mp_id}
                  onClick={() => onSelectMP(m)}
                  className="hover:bg-gray-900/80 transition-colors cursor-pointer"
                >
                  <td className="py-2.5 px-3 font-semibold text-gray-400">{m.sr_no}</td>
                  <td className="py-2.5 px-3 font-bold text-white">{m.mp_name}</td>
                  <td className="py-2.5 px-3 text-gray-300">
                    {m.constituency}
                    <span className="text-[10px] text-gray-500 ml-1">({m.category})</span>
                  </td>
                  <td className="py-2.5 px-3 text-gray-400">{m.state}</td>
                  <td className="py-2.5 px-3 font-bold text-emerald-400">
                    {m.allocated_amount_crores ? `₹${m.allocated_amount_crores} Cr` : "MISSING DATA"}
                  </td>
                  <td className="py-2.5 px-3">
                    {m.deviation_from_baseline_inr ? (
                      <span className={m.deviation_from_baseline_inr > 0 ? "text-amber-400" : (m.deviation_from_baseline_inr < 0 ? "text-blue-400" : "text-gray-500")}>
                        {m.deviation_from_baseline_inr > 0 ? "+" : ""}
                        ₹{(m.deviation_from_baseline_inr/1e7).toFixed(2)} Cr
                      </span>
                    ) : (
                      <span className="text-red-400">Null Entry</span>
                    )}
                  </td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider ${badgeBg}`}>
                      {riskLvl}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <button className="p-1.5 bg-gray-800 hover:bg-indigo-600 text-gray-300 hover:text-white rounded transition-colors border border-gray-700">
                      <ArrowUpRight className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="pt-3 border-t border-gray-800 flex items-center justify-between text-[11px] text-gray-500 font-mono">
        <span>Showing {Math.min(filtered.length, 100)} of {filtered.length} matched records</span>
        <span className="text-indigo-400 font-bold">Click any row to open full Investigation Workspace</span>
      </div>
    </div>
  );
}
