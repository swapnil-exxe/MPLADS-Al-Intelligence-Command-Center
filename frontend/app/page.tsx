"use client";

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from '../components/Header';
import SidebarNav from '../components/SidebarNav';
import OverviewMetrics from '../components/OverviewMetrics';
import AIWatch from '../components/AIWatch';
import IndiaRiskMap from '../components/IndiaRiskMap';
import AnomalyMatrix from '../components/AnomalyMatrix';
import FraudIntelligence from '../components/FraudIntelligence';
import InvestigationWorkspace from '../components/InvestigationWorkspace';
import AIInvestigatorChat from '../components/AIInvestigatorChat';
import DataSourcesModal from '../components/DataSourcesModal';
import ModelHealthCard from '../components/ModelHealthCard';
import CapabilityScopeCard from '../components/CapabilityScopeCard';
import { motion } from 'framer-motion';

import { API_BASE } from '../lib/api';

function MainContent() {
  const searchParams = useSearchParams();
  const initialTab = searchParams.get('tab') || "overview";
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [kpis, setKpis] = useState<any | null>(null);
  const [stateAnalytics, setStateAnalytics] = useState<any[]>([]);
  const [mps, setMps] = useState<any[]>([]);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [selectedMP, setSelectedMP] = useState<any | null>(null);
  const [showDataSources, setShowDataSources] = useState<boolean>(false);
  const [showModelHealth, setShowModelHealth] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Sync tab from URL if present
  useEffect(() => {
    const tabFromUrl = searchParams.get('tab');
    if (tabFromUrl) {
      setActiveTab(tabFromUrl);
    }
  }, [searchParams]);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [kpiRes, stateRes, mpRes, anomalyRes] = await Promise.all([
          fetch(`${API_BASE}/api/analytics/overview`),
          fetch(`${API_BASE}/api/analytics/states`),
          fetch(`${API_BASE}/api/analytics/mps?limit=600`),
          fetch(`${API_BASE}/api/risk/anomalies`)
        ]);

        if (!kpiRes.ok || !stateRes.ok || !mpRes.ok || !anomalyRes.ok) {
          throw new Error("Failed to fetch data from backend FastAPI endpoints");
        }

        const kpiData = await kpiRes.json();
        const stateData = await stateRes.json();
        const mpData = await mpRes.json();
        const anomalyData = await anomalyRes.json();

        setKpis(kpiData);
        setStateAnalytics(stateData);
        setMps(mpData.mps || []);
        setAnomalies(anomalyData.anomalies || []);
        setError(null);
      } catch (err: any) {
        setError(err.message || "Failed to connect to backend server");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const highRiskCount = anomalies.filter(a => a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL').length;

  return (
    <div className="flex flex-col min-h-screen bg-[#FFFDF5] text-black font-['Space_Grotesk',sans-serif] selection:bg-[#FFD93D] selection:text-black">
      {/* Top Bar Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onOpenDataSources={() => setShowDataSources(true)}
        onOpenModelHealth={() => setShowModelHealth(true)}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar Nav */}
        <SidebarNav
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          highRiskCount={highRiskCount}
        />

        {/* Main Workspace Body */}
        <main className="flex-1 p-8 overflow-y-auto max-h-[calc(100vh-65px)] space-y-8">
          {error && (
            <div className="bg-[#FF6B6B] text-white border-4 border-black p-4 font-mono font-bold text-xs shadow-[4px_4px_0px_0px_#000] flex items-center justify-between">
              <span>⚠️ BACKEND NOTICE: {error}. ENSURE FASTAPI IS RUNNING ON `http://localhost:8001`.</span>
              <button
                onClick={() => window.location.reload()}
                className="bg-black hover:bg-white hover:text-black text-white px-3 py-1 border border-black font-black uppercase"
              >
                RETRY
              </button>
            </div>
          )}

          {/* TAB 1: OVERVIEW */}
          {activeTab === 'overview' && (
            <motion.div 
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.15 }}
              className="space-y-8 max-w-6xl mx-auto"
            >
              {/* HERO TITLE SECTION */}
              <div className="space-y-2 bg-[#FFD93D] p-6 border-4 border-black shadow-[8px_8px_0px_0px_#000]">
                <div className="flex items-center space-x-3 font-mono text-xs font-black text-black uppercase">
                  <span className="bg-black text-white px-2 py-0.5 border border-black">MoSPI · DIID</span>
                  <span>543 MP RECORDS</span>
                  <span>·</span>
                  <span>36 STATES / UTs</span>
                </div>
                
                <h1 className="text-4xl sm:text-5xl font-black text-black uppercase tracking-tight leading-none">
                  MPLADS INTELLIGENCE
                </h1>
                
                <p className="text-sm font-bold text-black max-w-2xl leading-relaxed uppercase font-mono">
                  PUBLIC MONEY. DATA-DRIVEN OVERSIGHT. Continuous monitoring of MPLADS allocation patterns with explainable anomaly signals.
                </p>
              </div>

              {/* Bold Horizontal Intelligence Strip */}
              <OverviewMetrics kpis={kpis} highRiskCount={highRiskCount} />

              {/* AI Watch Hero Panel */}
              <AIWatch anomalies={anomalies} onSelectMP={(mp) => setSelectedMP(mp)} />

              {/* State & Map Analytics */}
              <IndiaRiskMap
                stateAnalytics={stateAnalytics}
                onSelectState={() => setActiveTab('mps')}
              />

              {/* Capability & Scope Card */}
              <CapabilityScopeCard />
            </motion.div>
          )}

          {/* TAB 2: MPS DIRECTORY */}
          {activeTab === 'mps' && (
            <AnomalyMatrix 
              mps={anomalies.length > 0 ? anomalies : mps} 
              onSelectMP={(mp) => setSelectedMP(mp)}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
            />
          )}

          {/* TAB 3: RISK INTELLIGENCE */}
          {activeTab === 'risk' && (
            <div className="space-y-8 max-w-6xl mx-auto">
              <AIWatch anomalies={anomalies} onSelectMP={(mp) => setSelectedMP(mp)} />
              <AnomalyMatrix 
                mps={anomalies} 
                onSelectMP={(mp) => setSelectedMP(mp)}
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
              />
            </div>
          )}

          {/* TAB 4: ALLOCATION ANOMALIES */}
          {activeTab === 'anomalies' && (
            <div className="max-w-6xl mx-auto">
              <AnomalyMatrix 
                mps={anomalies} 
                onSelectMP={(mp) => setSelectedMP(mp)}
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
              />
            </div>
          )}

          {/* TAB 5: FRAUD INTELLIGENCE */}
          {activeTab === 'fraud' && (
            <div className="max-w-6xl mx-auto">
              <FraudIntelligence />
            </div>
          )}

          {/* TAB 6: STATES */}
          {activeTab === 'states' && (
            <div className="max-w-6xl mx-auto">
              <IndiaRiskMap stateAnalytics={stateAnalytics} onSelectState={() => {}} />
            </div>
          )}

          {/* TAB 7: FUND ANALYTICS */}
          {activeTab === 'fund' && (
            <div className="space-y-8 max-w-6xl mx-auto">
              <OverviewMetrics kpis={kpis} highRiskCount={highRiskCount} />
              <IndiaRiskMap stateAnalytics={stateAnalytics} onSelectState={() => {}} />
            </div>
          )}

          {/* TAB 8: AI INVESTIGATOR */}
          {activeTab === 'ai_investigator' && (
            <div className="max-w-5xl mx-auto">
              <AIInvestigatorChat />
            </div>
          )}

          {/* TAB 9: DATA SOURCES */}
          {activeTab === 'data_sources' && (
            <div className="max-w-4xl mx-auto">
              <DataSourcesModal onClose={() => setActiveTab('overview')} />
            </div>
          )}

          {/* TAB 10: MODEL HEALTH */}
          {activeTab === 'model_health' && (
            <div className="max-w-4xl mx-auto">
              <ModelHealthCard />
            </div>
          )}
        </main>
      </div>

      {/* Investigation Drawer */}
      {selectedMP && (
        <InvestigationWorkspace
          mp={selectedMP}
          onClose={() => setSelectedMP(null)}
        />
      )}

      {/* Standalone Modals */}
      {showDataSources && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <DataSourcesModal onClose={() => setShowDataSources(false)} />
          </div>
        </div>
      )}

      {showModelHealth && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-4xl">
            <ModelHealthCard onClose={() => setShowModelHealth(false)} />
            <button
              onClick={() => setShowModelHealth(false)}
              className="mt-4 w-full bg-[#FF6B6B] hover:bg-black hover:text-white text-black font-black text-xs py-3 border-4 border-black shadow-[4px_4px_0px_0px_#000] uppercase"
            >
              CLOSE WINDOW
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default function CommandCenterPage() {
  return (
    <Suspense fallback={<div className="p-4 font-mono font-bold text-xs">Loading Command Center...</div>}>
      <MainContent />
    </Suspense>
  );
}
