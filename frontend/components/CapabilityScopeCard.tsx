"use client";

import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function CapabilityScopeCard() {
  return (
    <div className="bg-[#FFFDF5] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000] font-['Space_Grotesk',sans-serif] space-y-4">
      <div className="flex items-center justify-between pb-3 border-b-4 border-black">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-black stroke-[3px]" />
          <span className="font-black text-black uppercase tracking-wider text-xs">
            SYSTEM CAPABILITY & EXTENSIBLE ARCHITECTURE SCOPE
          </span>
        </div>
        <span className="text-[10px] font-black text-black bg-[#FFD93D] px-2 py-0.5 border border-black uppercase font-mono">
          ANALYTICAL HONESTY ENFORCED
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Column 1: Today */}
        <div className="bg-white border-2 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-2">
          <span className="text-xs font-black text-black uppercase tracking-wider block bg-[#FFD93D] px-2 py-0.5 border border-black inline-block">
            WHAT WE CAN DETECT TODAY (REAL DATA)
          </span>
          <ul className="space-y-2 text-black text-xs font-bold font-sans">
            <li className="flex items-baseline space-x-2">
              <span className="text-emerald-600 font-black">✓</span>
              <span>Allocation limit outliers & non-standard amounts</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="text-emerald-600 font-black">✓</span>
              <span>Baseline divergence against standard ₹14.70 Cr entitlement</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="text-emerald-600 font-black">✓</span>
              <span>State & UT peer-group distribution anomalies</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="text-emerald-600 font-black">✓</span>
              <span>Isolation Forest & LOF statistical anomaly signals</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="text-emerald-600 font-black">✓</span>
              <span>Data completeness audit (missing records & seat succession)</span>
            </li>
          </ul>
        </div>

        {/* Column 2: Additional Data */}
        <div className="bg-white border-2 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-2">
          <span className="text-xs font-black text-black uppercase tracking-wider block bg-[#C4B5FD] px-2 py-0.5 border border-black inline-block">
            WHAT ADDITIONAL DATA ENABLES (EXTENSIBLE)
          </span>
          <ul className="space-y-2 text-black text-xs font-bold font-sans">
            <li className="flex items-baseline space-x-2">
              <span className="font-black text-black">○</span>
              <span>Project expenditure anomalies (Requires work release dataset)</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="font-black text-black">○</span>
              <span>Contractor networks & tender concentration (Requires GeM database)</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="font-black text-black">○</span>
              <span>PFMS payment transaction dates (Requires PFMS ledger)</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="font-black text-black">○</span>
              <span>Physical progress % & geotagged completion certificates</span>
            </li>
            <li className="flex items-baseline space-x-2">
              <span className="font-black text-black">○</span>
              <span>Duplicate work descriptions across adjacent sanctions</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
