"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import {
  LayoutDashboard,
  ShieldAlert,
  AlertTriangle,
  GitGraph,
  Sparkles,
  MapPin,
  BarChart3,
  Database,
  Cpu
} from 'lucide-react';

interface SidebarNavProps {
  activeTab: string;
  setActiveTab?: (tab: string) => void;
  highRiskCount?: number;
}

export default function SidebarNav({ activeTab, setActiveTab, highRiskCount = 42 }: SidebarNavProps) {
  const router = useRouter();

  const navItems = [
    { id: 'overview', label: 'OVERVIEW', icon: LayoutDashboard, path: '/?tab=overview' },
    { id: 'risk', label: 'RISK INTELLIGENCE', icon: ShieldAlert, badge: highRiskCount, path: '/risk' },
    { id: 'anomalies', label: 'ANOMALIES', icon: AlertTriangle, path: '/anomalies' },
    { id: 'fraud', label: 'RELATIONSHIP SCOPE', icon: GitGraph, path: '/fraud' },
    { id: 'ai_investigator', label: 'INVESTIGATOR', icon: Sparkles, highlight: true, path: '/investigator' },
    { id: 'states', label: 'STATE ANALYTICS', icon: MapPin, path: '/?tab=states' },
    { id: 'fund', label: 'FUND ANALYTICS', icon: BarChart3, path: '/?tab=fund' },
    { id: 'data_sources', label: 'DATA SOURCES', icon: Database, path: '/data-sources' },
    { id: 'model_health', label: 'MODEL HEALTH', icon: Cpu, path: '/model-health' }
  ];

  const handleNavClick = (item: typeof navItems[0]) => {
    if (setActiveTab) {
      setActiveTab(item.id);
    } else if (item.path) {
      router.push(item.path);
    }
  };

  return (
    <aside className="w-64 bg-[#FFFDF5] border-r-4 border-black p-4 flex flex-col justify-between shrink-0 font-['Space_Grotesk',sans-serif]">
      <div className="space-y-6">
        <div className="space-y-2">
          <span className="text-xs font-black text-black uppercase tracking-widest px-2 block border-b-2 border-black pb-1">
            NAVIGATION
          </span>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleNavClick(item)}
                className={`w-full flex items-center justify-between px-3 py-2.5 text-xs font-black uppercase transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none ${
                  isActive
                    ? "bg-[#FFD93D] text-black border-2 border-black shadow-[4px_4px_0px_0px_#000]"
                    : "bg-white text-black border-2 border-black hover:bg-[#FF6B6B] hover:text-white shadow-[2px_2px_0px_0px_#000]"
                }`}
              >
                <div className="flex items-center space-x-2.5">
                  <Icon className="w-4 h-4 stroke-[3px]" />
                  <span>{item.label}</span>
                </div>

                {item.badge !== undefined && item.badge > 0 && (
                  <span className="bg-[#FF6B6B] text-white border border-black text-[10px] font-black px-1.5 py-0.2">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Footer System Info */}
      <div className="pt-4 border-t-4 border-black text-xs font-mono font-bold space-y-1 bg-[#FFD93D] p-3 border-2 border-black shadow-[4px_4px_0px_0px_#000]">
        <div className="flex items-center justify-between uppercase">
          <span>MoSPI Official CSV</span>
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 border border-black"></span>
        </div>
        <div className="text-[10px] text-black font-bold">543 MPs · ₹8,306.21 Cr Ingested</div>
      </div>
    </aside>
  );
}
