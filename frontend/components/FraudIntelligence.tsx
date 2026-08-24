"use client";

import React, { useState, useEffect } from 'react';
import { Network, Database, ShieldAlert, FileText, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';
import { API_BASE } from '../lib/api';

export default function FraudIntelligence() {
  const [anomalies, setAnomalies] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/risk/anomalies`)
      .then(res => res.json())
      .then(data => {
        const highAnomalies = (data.anomalies || []).filter((a: any) => a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL');
        setAnomalies(highAnomalies);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-6 font-['Space_Grotesk',sans-serif]">
      {/* Top Professional Government Status Banner */}
      <div className="bg-[#FFD93D] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000] space-y-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-black text-white border-2 border-black">
            <Network className="w-6 h-6 stroke-[3px]" />
          </div>
          <div>
            <h2 className="text-xl font-black text-black uppercase tracking-tight">RELATIONSHIP & ENTITY NETWORK OVERVIEW</h2>
            <p className="text-xs font-bold text-black font-mono">
              Multi-Entity Relationship Mapping & Source Data Integration Architecture
            </p>
          </div>
        </div>
      </div>

      {/* Main Grid: Data Requirement Notice + Real Statistical High-Risk Signals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Card: Professional Data Integration Status */}
        <div className="bg-white border-4 border-black p-6 shadow-[6px_6px_0px_0px_#000] flex flex-col justify-between space-y-4">
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b-4 border-black">
              <div className="flex items-center space-x-2">
                <Database className="w-5 h-5 text-black stroke-[3px]" />
                <h3 className="font-black text-black text-base uppercase">DATA SOURCE SCOPE & INTEGRATION REQUIREMENTS</h3>
              </div>
              <span className="text-[10px] font-mono font-black bg-[#C4B5FD] text-black border-2 border-black px-2 py-0.5 uppercase">
                GAZETTE SCOPE
              </span>
            </div>

            <div className="bg-[#FFFDF5] p-4 border-2 border-black font-mono text-xs space-y-3">
              <div className="flex items-center space-x-2 text-black font-black uppercase text-xs">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 stroke-[3px]" />
                <span>CONNECTED PRIMARY SOURCE: MoSPI GAZETTE</span>
              </div>
              <p className="text-black font-sans text-xs font-bold leading-relaxed">
                The currently connected production dataset (<strong className="bg-[#FFD93D] px-1 border border-black font-mono">Allocated_Limit_for_Honble_MPs.csv</strong>) contains verified MP-level allocation amounts across all 543 Lok Sabha seats and 36 States/UTs.
              </p>

              <div className="pt-3 border-t-2 border-black space-y-2">
                <div className="flex items-center space-x-2 text-black font-black uppercase text-xs">
                  <Layers className="w-4 h-4 text-amber-600 stroke-[3px]" />
                  <span>REQUIREMENTS FOR VENDOR/CONTRACTOR GRAPH MAPPING</span>
                </div>
                <p className="text-black font-sans text-xs font-bold leading-relaxed">
                  Constructing multi-node entity relationship graphs (contractor clusters, cross-constituency vendor allocations, duplicate work orders) requires ingesting micro-project transaction datasets:
                </p>
                <ul className="list-disc pl-5 space-y-1 font-mono text-[11px] font-bold text-black">
                  <li>MoSPI e-SAKSHI Work Order Registry</li>
                  <li>PFMS (Public Financial Management System) Disbursement Ledger</li>
                  <li>District Nodal Agency Contractor Registrations</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="pt-3 border-t-2 border-black text-[10px] text-black font-mono font-bold flex items-center justify-between">
            <span>NO SIMULATED OR FABRICATED RELATIONSHIPS DISPLAYED</span>
            <span className="bg-black text-white px-2 py-0.5 border border-black uppercase font-mono">
              STRICT GROUND TRUTH ADHERENCE
            </span>
          </div>
        </div>

        {/* Right Card: Genuine High-Divergence Anomaly Signals from PostgreSQL */}
        <div className="bg-white border-4 border-black p-6 shadow-[6px_6px_0px_0px_#000] flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between pb-3 border-b-4 border-black">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-5 h-5 text-black stroke-[3px]" />
                <h3 className="font-black text-black text-base uppercase">STATISTICAL DIVERGENCE SIGNALS ({anomalies.length})</h3>
              </div>
              <span className="text-[10px] font-mono font-black bg-[#FF6B6B] text-white border-2 border-black px-2 py-0.5 uppercase">
                SUPABASE LIVE
              </span>
            </div>

            <div className="mt-4 space-y-3 max-h-[340px] overflow-y-auto pr-1">
              {anomalies.length > 0 ? (
                anomalies.map((a: any) => (
                  <div key={a.mp_id} className="bg-[#FFFDF5] border-2 border-black p-3 space-y-1 font-mono text-xs shadow-[2px_2px_0px_0px_#000]">
                    <div className="flex items-center justify-between font-bold">
                      <span className="font-black text-black">{a.mp_name}</span>
                      <span className={`text-[10px] px-2 py-0.5 border border-black font-black uppercase ${
                        a.risk_level === 'CRITICAL' ? 'bg-[#FF6B6B] text-white' : 'bg-[#FFD93D] text-black'
                      }`}>
                        {a.risk_level} • SCORE {a.risk_score}/100
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-black font-bold">
                      <span>Constituency: {a.constituency} ({a.state})</span>
                      <span className="text-emerald-700 font-bold">
                        {a.allocated_amount_crores ? `₹${a.allocated_amount_crores} Cr` : 'NULL ENTRY'}
                      </span>
                    </div>
                    <div className="text-[10px] text-black font-bold bg-white p-1 border border-black">
                      Signal: {a.signal_type} ({a.multi_method_agreement})
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-4 bg-[#FFFDF5] border-2 border-black text-xs font-mono font-bold text-center">
                  Loading high-divergence signals from Supabase Cloud PostgreSQL...
                </div>
              )}
            </div>
          </div>

          <div className="pt-3 border-t-2 border-black text-[10px] text-black font-mono text-center font-black bg-[#FFD93D] p-2 border-2 border-black uppercase">
            REAL DATA DERIVED DIRECTLY FROM MoSPI GAZETTE & ML PIPELINE
          </div>
        </div>
      </div>
    </div>
  );
}
