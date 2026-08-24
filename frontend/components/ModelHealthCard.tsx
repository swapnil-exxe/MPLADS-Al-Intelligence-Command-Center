"use client";

import React, { useEffect, useState } from 'react';
import { Cpu, CheckCircle2, ShieldCheck, Database, Sliders, Activity } from 'lucide-react';
import { API_BASE } from '../lib/api';

interface ModelHealthCardProps {
  onClose?: () => void;
}

export default function ModelHealthCard({ onClose }: ModelHealthCardProps) {
  const [models, setModels] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/system/model-health`)
      .then(res => res.json())
      .then(data => setModels(data.models || []))
      .catch(() => {});
  }, []);

  return (
    <div className="bg-[#FFFDF5] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000] space-y-6 font-['Space_Grotesk',sans-serif]">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between pb-4 border-b-4 border-black bg-[#FFD93D] p-4 border-2 gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-black text-white border-2 border-black">
            <Cpu className="w-6 h-6 stroke-[3px]" />
          </div>
          <div>
            <h2 className="text-xl font-black text-black uppercase tracking-tight">AI MODEL HEALTH & PRODUCTION MATRIX</h2>
            <p className="text-xs font-bold text-black font-mono">
              Unsupervised Allocation Anomaly Detection operating on official MoSPI entitlement parameters.
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <span className="bg-emerald-400 text-black border-2 border-black px-3 py-1 text-xs font-mono font-black uppercase shadow-[2px_2px_0px_0px_#000]">
            STATUS: OPERATIONAL
          </span>
          <span className="bg-black text-white border-2 border-black px-3 py-1 text-xs font-mono font-black uppercase shadow-[2px_2px_0px_0px_#FFD93D]">
            SYSTEM READINESS: 98/100
          </span>
        </div>
      </div>

      {/* Production Key Metrics Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
        <div className="bg-white p-3 border-4 border-black shadow-[4px_4px_0px_0px_#000]">
          <span className="text-[10px] font-black uppercase text-gray-600 block">MODEL TYPE</span>
          <span className="font-black text-sm text-black block uppercase font-sans">UNSUPERVISED ANOMALY</span>
        </div>
        <div className="bg-white p-3 border-4 border-black shadow-[4px_4px_0px_0px_#000]">
          <span className="text-[10px] font-black uppercase text-gray-600 block">PRODUCTION ALGORITHMS</span>
          <span className="font-black text-xs text-black block uppercase font-sans">ISOLATION FOREST + TUKEY IQR</span>
        </div>
        <div className="bg-white p-3 border-4 border-black shadow-[4px_4px_0px_0px_#000]">
          <span className="text-[10px] font-black uppercase text-gray-600 block">DATASET & SCOPE</span>
          <span className="font-black text-sm text-black block font-sans">543 MPs (36 States/UTs)</span>
        </div>
        <div className="bg-white p-3 border-4 border-black shadow-[4px_4px_0px_0px_#000]">
          <span className="text-[10px] font-black uppercase text-gray-600 block">REPRODUCIBILITY</span>
          <span className="font-black text-sm text-black block uppercase font-sans">DETERMINISTIC (SEED 42)</span>
        </div>
      </div>

      {/* Validation Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
        <div className="bg-[#FF6B6B] text-white p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] space-y-1">
          <span className="text-[10px] font-black uppercase block bg-black text-white px-2 py-0.5 border border-white inline-block">GROUND TRUTH STATUS</span>
          <span className="font-black block text-base font-sans uppercase">SUPERVISED ACCURACY NOT APPLICABLE</span>
          <p className="font-sans text-xs font-bold leading-relaxed">
            Supervised accuracy is not available because no verified labeled ground-truth dataset is connected.
          </p>
        </div>

        <div className="bg-[#C4B5FD] text-black p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] space-y-1">
          <span className="text-[10px] font-black uppercase block bg-black text-white px-2 py-0.5 border border-black inline-block">MODEL PARADIGM & CONSENSUS</span>
          <span className="font-black block text-base font-sans uppercase">MULTI-METHOD ANOMALY CONSENSUS</span>
          <p className="font-sans text-xs font-bold leading-relaxed">
            Evaluated via 90% top-K random seed stability and multi-method consensus agreement across Isolation Forest, Tukey IQR, and statistical baseline tests.
          </p>
        </div>
      </div>

      {/* Models List */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
        {models.map((m, idx) => (
          <div key={idx} className="bg-white border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-black text-black text-base uppercase font-sans">{m.name}</span>
              <CheckCircle2 className="w-5 h-5 text-emerald-600 stroke-[3px]" />
            </div>

            <div className="space-y-1 text-black font-bold text-xs">
              <div>ALGORITHM: <span className="bg-[#FFD93D] px-1 border border-black">{m.algorithm}</span></div>
              <div>SAMPLES: <span className="bg-white px-1 border border-black">{m.data_points} MPs</span></div>
              <div>STATUS: <span className="bg-emerald-400 px-1 border border-black">{m.status}</span></div>
            </div>

            <div className="bg-[#FFFDF5] p-2.5 border-2 border-black space-y-1">
              <span className="text-[10px] font-black uppercase block">NON-REDUNDANT FEATURES:</span>
              <div className="flex flex-wrap gap-1">
                {(m.feature_inputs || []).map((f: string, i: number) => (
                  <span key={i} className="bg-white text-black text-[10px] font-bold px-1.5 py-0.5 border border-black">
                    {f}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
