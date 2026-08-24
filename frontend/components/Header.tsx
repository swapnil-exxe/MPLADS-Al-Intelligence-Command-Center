"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { Search, Database, Cpu, X } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab?: (tab: string) => void;
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
  onOpenDataSources?: () => void;
  onOpenModelHealth?: () => void;
}

export default function Header({
  activeTab,
  setActiveTab,
  searchQuery = "",
  setSearchQuery,
  onOpenDataSources,
  onOpenModelHealth
}: HeaderProps) {
  const router = useRouter();

  const handleBrandClick = () => {
    if (setActiveTab) setActiveTab('overview');
    router.push('/');
  };

  const handleDataSourcesClick = () => {
    if (onOpenDataSources) {
      onOpenDataSources();
    } else {
      router.push('/data-sources');
    }
  };

  const handleModelHealthClick = () => {
    if (onOpenModelHealth) {
      onOpenModelHealth();
    } else {
      router.push('/model-health');
    }
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const q = e.target.value;
    if (setSearchQuery) {
      setSearchQuery(q);
      if (q.trim() && setActiveTab && activeTab !== 'anomalies' && activeTab !== 'mps') {
        setActiveTab('anomalies');
      }
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-[#FFFDF5] border-b-4 border-black px-6 py-3 flex items-center justify-between font-['Space_Grotesk',sans-serif]">
      {/* Brand & Authority */}
      <div className="flex items-center space-x-4">
        <div 
          onClick={handleBrandClick}
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="w-9 h-9 bg-[#FF6B6B] border-2 border-black flex items-center justify-center font-black text-black text-lg shadow-[3px_3px_0px_0px_#000]">
            M
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-black text-base uppercase text-black tracking-tight">MPLADS INTELLIGENCE</span>
              <span className="text-[11px] font-bold text-black bg-[#FFD93D] px-2 py-0.5 border-2 border-black uppercase font-mono">
                MoSPI · DIID
              </span>
            </div>
            <p className="text-[11px] font-bold text-black uppercase tracking-wider hidden sm:block">
              Official Dataset · 543 MPs · 36 States / UTs
            </p>
          </div>
        </div>
      </div>

      {/* Center Search & Status */}
      <div className="hidden md:flex items-center space-x-3 font-mono">
        <div className="relative w-72">
          <Search className="w-4 h-4 text-black absolute left-3 top-1/2 -translate-y-1/2 stroke-[3px]" />
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="SEARCH CONSTITUENCY..."
            className="w-full bg-white border-2 border-black text-xs font-bold pl-9 pr-8 py-1.5 text-black placeholder-black/50 focus:outline-none focus:bg-[#FFD93D] shadow-[3px_3px_0px_0px_#000] transition-all uppercase"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery && setSearchQuery("")}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-black hover:bg-black hover:text-white p-0.5 font-black text-xs"
            >
              <X className="w-3.5 h-3.5 stroke-[3px]" />
            </button>
          )}
        </div>

        <div className="flex items-center space-x-2 text-xs font-black text-black bg-[#FFD93D] border-2 border-black px-3 py-1.5 shadow-[3px_3px_0px_0px_#000] uppercase">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 border border-black animate-pulse"></span>
          <span>SYSTEM MONITORING</span>
        </div>
      </div>

      {/* Right Tools */}
      <div className="flex items-center space-x-2 font-mono text-xs">
        <button
          onClick={handleDataSourcesClick}
          className="flex items-center space-x-1.5 bg-white hover:bg-[#C4B5FD] text-black font-bold px-3 py-1.5 border-2 border-black shadow-[3px_3px_0px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all uppercase"
        >
          <Database className="w-4 h-4 stroke-[3px]" />
          <span className="hidden sm:inline">DATA SOURCES</span>
        </button>

        <button
          onClick={handleModelHealthClick}
          className="flex items-center space-x-1.5 bg-white hover:bg-[#FFD93D] text-black font-bold px-3 py-1.5 border-2 border-black shadow-[3px_3px_0px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all uppercase"
        >
          <Cpu className="w-4 h-4 stroke-[3px]" />
          <span className="hidden sm:inline">MODEL HEALTH</span>
        </button>
      </div>
    </header>
  );
}
