"use client";

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from '../../components/Header';
import SidebarNav from '../../components/SidebarNav';
import AIWatch from '../../components/AIWatch';
import AnomalyMatrix from '../../components/AnomalyMatrix';
import InvestigationWorkspace from '../../components/InvestigationWorkspace';

import { API_BASE, apiFetch } from '../../lib/api';

function RiskContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get('q') || "";
  const [searchQuery, setSearchQuery] = useState<string>(initialQuery);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [selectedMP, setSelectedMP] = useState<any | null>(null);

  useEffect(() => {
    apiFetch('/api/risk/anomalies')
      .then(res => res.json())
      .then(data => setAnomalies(data.anomalies || []))
      .catch(() => {});
  }, []);

  const highRiskCount = anomalies.filter(a => a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL').length;

  return (
    <div className="flex flex-col min-h-screen bg-[#FFFDF5] text-black font-['Space_Grotesk',sans-serif] selection:bg-[#FFD93D]">
      <Header
        activeTab="risk"
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />
      <div className="flex flex-1 overflow-hidden">
        <SidebarNav activeTab="risk" highRiskCount={highRiskCount} />
        <main className="flex-1 p-6 overflow-y-auto max-h-[calc(100vh-57px)] space-y-6">
          <div className="bg-[#FFD93D] border-4 border-black p-5 shadow-[6px_6px_0px_0px_#000] font-mono">
            <h1 className="text-xl font-black text-black uppercase tracking-tight">RISK INTELLIGENCE & ALLOCATION ANOMALIES</h1>
            <p className="text-xs font-bold text-black mt-1">
              Multi-variate statistical anomaly scores derived from official MoSPI allocation records using Isolation Forest & Tukey IQR Outlier Detector.
            </p>
          </div>
          <AIWatch anomalies={anomalies} onSelectMP={(mp) => setSelectedMP(mp)} />
          <AnomalyMatrix
            mps={anomalies}
            onSelectMP={(mp) => setSelectedMP(mp)}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
          />
        </main>
      </div>
      {selectedMP && <InvestigationWorkspace mp={selectedMP} onClose={() => setSelectedMP(null)} />}
    </div>
  );
}

export default function RiskPage() {
  return (
    <Suspense fallback={<div className="p-4 font-mono font-bold text-xs">Loading Risk Intelligence...</div>}>
      <RiskContent />
    </Suspense>
  );
}
