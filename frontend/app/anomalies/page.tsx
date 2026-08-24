"use client";

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import SidebarNav from '../../components/SidebarNav';
import AnomalyMatrix from '../../components/AnomalyMatrix';
import InvestigationWorkspace from '../../components/InvestigationWorkspace';

import { API_BASE } from '../../lib/api';

export default function AnomaliesPage() {
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [selectedMP, setSelectedMP] = useState<any | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/risk/anomalies`)
      .then(res => res.json())
      .then(data => setAnomalies(data.anomalies || []))
      .catch(() => {});
  }, []);

  const highRiskCount = anomalies.filter(a => a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL').length;

  return (
    <div className="flex flex-col min-h-screen bg-[#FFFDF5] text-black font-['Space_Grotesk',sans-serif]">
      <Header activeTab="anomalies" setActiveTab={() => {}} />
      <div className="flex flex-1 overflow-hidden">
        <SidebarNav activeTab="anomalies" setActiveTab={() => {}} highRiskCount={highRiskCount} />
        <main className="flex-1 p-6 overflow-y-auto max-h-[calc(100vh-57px)] space-y-6">
          <div className="bg-[#FFD93D] border-4 border-black p-5 shadow-[6px_6px_0px_0px_#000] font-mono">
            <h1 className="text-xl font-black text-black uppercase tracking-tight">ALLOCATION ANOMALIES STREAM</h1>
            <p className="text-xs font-bold text-black mt-1">
              Evaluated against national baseline limit (₹14.70 Cr) and state peer distributions.
            </p>
          </div>
          <AnomalyMatrix mps={anomalies} onSelectMP={(mp) => setSelectedMP(mp)} />
        </main>
      </div>
      {selectedMP && <InvestigationWorkspace mp={selectedMP} onClose={() => setSelectedMP(null)} />}
    </div>
  );
}
