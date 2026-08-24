"use client";

import React from 'react';
import OverviewMetrics from './OverviewMetrics';
import { DollarSign, Layers, TrendingUp, AlertCircle, ShieldCheck } from 'lucide-react';

interface FundAnalyticsViewProps {
  kpis: any;
  highRiskCount: number;
  anomalies: any[];
}

export default function FundAnalyticsView({ kpis, highRiskCount, anomalies }: FundAnalyticsViewProps) {
  const totalAllocationCr = kpis?.total_allocation_crores || 8306.21;
  const totalMPs = kpis?.total_records || 543;
  const baselineMPs = anomalies.filter(a => a.allocated_amount_crores === 14.70).length;
  const highAllocMPs = anomalies.filter(a => a.allocated_amount_crores > 20.0).length;
  const lowAllocMPs = anomalies.filter(a => a.allocated_amount_crores < 10.0 && a.allocated_amount_crores !== null).length;
  const missingMPs = anomalies.filter(a => a.allocated_amount_crores === null).length;

  return (
    <div className="space-y-8 font-['Space_Grotesk',sans-serif]">
      {/* Title Banner */}
      <div className="bg-[#FFD93D] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000]">
        <div className="flex items-center space-x-3 font-mono text-xs font-black uppercase mb-2">
          <span className="bg-black text-white px-2 py-0.5 border border-black">FINANCIAL AUDIT</span>
          <span>TOTAL ENTITLEMENT: ₹{totalAllocationCr.toLocaleString()} CR</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-black uppercase tracking-tight">
          MPLADS FUND FINANCIAL & ALLOCATION TIER ANALYTICS
        </h1>
        <p className="text-xs font-bold text-black font-mono mt-1 uppercase">
          Breakdown of standard baseline entitlement limits, allocation tier distributions, and financial divergence metrics.
        </p>
      </div>

      {/* Primary KPI Intelligence Strip */}
      <OverviewMetrics kpis={kpis} highRiskCount={highRiskCount} />

      {/* Fund Allocation Entitlement Tiers */}
      <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000] space-y-6">
        <div className="border-b-4 border-black pb-4">
          <div className="flex items-center space-x-2 font-mono text-xs font-black uppercase text-black/70 mb-1">
            <Layers className="w-4 h-4 text-black stroke-[3px]" />
            <span>FINANCIAL TIER BREAKDOWN</span>
          </div>
          <h2 className="text-xl font-black uppercase tracking-tight text-black">
            ALLOCATION ENTITLEMENT DISTRIBUTION TIERS
          </h2>
          <p className="text-xs font-bold text-black/70 font-mono mt-0.5">
            Statistical breakdown of 543 MP entitlement limits across baseline, elevated, and sub-baseline tiers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 font-mono">
          {/* Tier 1: Baseline */}
          <div className="bg-[#FFFDF5] border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black uppercase text-black">STANDARD BASELINE</span>
              <ShieldCheck className="w-4 h-4 text-emerald-600 stroke-[3px]" />
            </div>
            <div className="text-2xl font-black text-black mt-2">₹14.70 CR</div>
            <div className="text-xs font-bold text-black/80 mt-1">{baselineMPs} MPs ({((baselineMPs / totalMPs) * 100).toFixed(1)}%)</div>
            <p className="text-[10px] text-black/60 font-bold mt-2 border-t-2 border-black/20 pt-2 uppercase">
              Official Gazette standard single-term baseline entitlement.
            </p>
          </div>

          {/* Tier 2: High Allocation */}
          <div className="bg-[#FFD93D] border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black uppercase text-black">HIGH ENTITLEMENT</span>
              <TrendingUp className="w-4 h-4 text-black stroke-[3px]" />
            </div>
            <div className="text-2xl font-black text-black mt-2">&gt; ₹20.00 CR</div>
            <div className="text-xs font-bold text-black/80 mt-1">{highAllocMPs} MPs ({((highAllocMPs / totalMPs) * 100).toFixed(1)}%)</div>
            <p className="text-[10px] text-black/60 font-bold mt-2 border-t-2 border-black/20 pt-2 uppercase">
              Multi-term entitlement rollup or constituency limit adjustments.
            </p>
          </div>

          {/* Tier 3: Low Allocation */}
          <div className="bg-[#FFFDF5] border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black uppercase text-black">SUB-BASELINE</span>
              <DollarSign className="w-4 h-4 text-amber-600 stroke-[3px]" />
            </div>
            <div className="text-2xl font-black text-black mt-2">&lt; ₹10.00 CR</div>
            <div className="text-xs font-bold text-black/80 mt-1">{lowAllocMPs} MPs ({((lowAllocMPs / totalMPs) * 100).toFixed(1)}%)</div>
            <p className="text-[10px] text-black/60 font-bold mt-2 border-t-2 border-black/20 pt-2 uppercase">
              Partial entitlement release or mid-term seat succession limit.
            </p>
          </div>

          {/* Tier 4: Missing Allocation */}
          <div className="bg-[#FF6B6B] text-white border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000]">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black uppercase">MISSING LIMIT</span>
              <AlertCircle className="w-4 h-4 text-white stroke-[3px]" />
            </div>
            <div className="text-2xl font-black text-white mt-2">NULL IN CSV</div>
            <div className="text-xs font-bold text-white/90 mt-1">{missingMPs} MP ({((missingMPs / totalMPs) * 100).toFixed(1)}%)</div>
            <p className="text-[10px] text-white/80 font-bold mt-2 border-t-2 border-white/30 pt-2 uppercase">
              Unspecified Gazette allocation limit (Flagged as CRITICAL).
            </p>
          </div>
        </div>
      </div>

      {/* Extremes & Financial Outliers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono">
        {/* Highest Allocation Card */}
        <div className="bg-white border-4 border-black p-6 shadow-[6px_6px_0px_0px_#000]">
          <div className="flex items-center space-x-2 text-xs font-black uppercase text-black/70 mb-2">
            <TrendingUp className="w-4 h-4 text-black stroke-[3px]" />
            <span>HIGHEST ALLOCATION LIMIT</span>
          </div>
          <div className="text-3xl font-black text-black">₹32.75 CR</div>
          <div className="text-sm font-bold text-black mt-1">EATALA RAJENDER · Malkajgiri (TELANGANA)</div>
          <p className="text-xs text-black/70 font-bold mt-2 border-t-2 border-black/20 pt-2 uppercase">
            Allocation limit is +122.8% higher than standard ₹14.70 Cr baseline. Flagged by Isolation Forest, Tukey IQR, and Z-Score.
          </p>
        </div>

        {/* Lowest Allocation Card */}
        <div className="bg-white border-4 border-black p-6 shadow-[6px_6px_0px_0px_#000]">
          <div className="flex items-center space-x-2 text-xs font-black uppercase text-black/70 mb-2">
            <DollarSign className="w-4 h-4 text-black stroke-[3px]" />
            <span>LOWEST ALLOCATION LIMIT</span>
          </div>
          <div className="text-3xl font-black text-black">₹4.90 CR</div>
          <div className="text-sm font-bold text-black mt-1">SK NURUL ISLAM · Basirhat (WEST BENGAL)</div>
          <p className="text-xs text-black/70 font-bold mt-2 border-t-2 border-black/20 pt-2 uppercase">
            Allocation limit is -66.7% below standard ₹14.70 Cr baseline. Flagged as statistical distribution outlier.
          </p>
        </div>
      </div>
    </div>
  );
}
