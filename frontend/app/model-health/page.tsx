"use client";

import React, { Suspense } from 'react';
import Header from '../../components/Header';
import SidebarNav from '../../components/SidebarNav';
import ModelHealthCard from '../../components/ModelHealthCard';

export default function ModelHealthPage() {
  return (
    <Suspense fallback={<div className="p-4 font-mono font-bold text-xs">Loading Model Health...</div>}>
      <div className="flex flex-col min-h-screen bg-[#FFFDF5] text-black font-['Space_Grotesk',sans-serif]">
        <Header activeTab="model_health" />
        <div className="flex flex-1 overflow-hidden">
          <SidebarNav activeTab="model_health" highRiskCount={42} />
          <main className="flex-1 p-6 overflow-y-auto max-h-[calc(100vh-57px)] space-y-6">
            <ModelHealthCard />
          </main>
        </div>
      </div>
    </Suspense>
  );
}
