'use client';

import React from 'react';
import { ShieldAlert, AlertTriangle, PhoneCall, Radio, ExternalLink } from 'lucide-react';

interface EmergencyProps {
  isEmergency: boolean;
  riskData: any;
  locationName: string;
}

export const EmergencyOverlay: React.FC<EmergencyProps> = ({ isEmergency, riskData, locationName }) => {
  if (!isEmergency && (!riskData || !riskData.is_emergency)) return null;

  const alerts = riskData?.active_alerts || [];
  const primaryAlert = alerts.length > 0 ? alerts[0] : {
    title: "🚨 CRITICAL CYCLONE & HEAVY FLOOD EMERGENCY WARNING",
    description: `Severe hazard conditions reported for ${locationName}. Heavy precipitation, squally winds, and potential river discharge surge expected.`,
    issued_by: "India Meteorological Department (IMD) - Disaster Warning Division",
    valid_until: "2026-08-26 18:00 IST",
    recommended_actions: [
      "Move to elevated ground or designated NDMA cyclone/flood shelters immediately.",
      "Coastal fishermen must remain on shore and secure all vessels.",
      "Keep emergency battery lights, first-aid kits, and clean drinking water ready.",
      "Call National Emergency Helpline 112 for rescue assistance."
    ]
  };

  return (
    <div className="bg-red-950/90 border-2 border-red-600 rounded-xl p-4 shadow-2xl backdrop-blur-md emergency-bg text-white mb-4 transition-all">
      <div className="flex items-center justify-between border-b border-red-700/60 pb-3 mb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-red-600 rounded-lg animate-bounce">
            <ShieldAlert className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="text-[10px] font-bold tracking-widest text-red-300 uppercase px-2 py-0.5 rounded bg-red-900 border border-red-700">
              DISASTER EMERGENCY MODE ACTIVE
            </span>
            <h2 className="text-lg font-extrabold text-white mt-0.5">{primaryAlert.title}</h2>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <a
            href="https://mausam.imd.gov.in"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1 bg-red-800 hover:bg-red-700 text-xs px-2.5 py-1.5 rounded-lg border border-red-600 font-semibold"
          >
            Official IMD Portal <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>

      <p className="text-xs text-red-100 mb-3 leading-relaxed">
        {primaryAlert.description}
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs mb-3">
        {/* Recommended Safety Directives */}
        <div className="bg-red-900/60 border border-red-700/50 p-3 rounded-lg">
          <div className="font-bold text-red-200 mb-1.5 flex items-center gap-1">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            NDMA Evacuation & Safety Directives:
          </div>
          <ul className="space-y-1 text-red-100 text-[11px]">
            {primaryAlert.recommended_actions?.map((act: string, idx: number) => (
              <li key={idx} className="flex items-start gap-1.5">
                <span className="text-amber-400 mt-0.5">•</span>
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Emergency Contacts */}
        <div className="bg-red-900/60 border border-red-700/50 p-3 rounded-lg flex flex-col justify-between">
          <div>
            <div className="font-bold text-red-200 mb-1.5 flex items-center gap-1">
              <PhoneCall className="w-4 h-4 text-emerald-400" />
              Emergency Response Helplines:
            </div>
            <div className="space-y-1 text-[11px] text-red-100">
              <div>• National Emergency Number: <span className="font-bold text-white">112</span></div>
              <div>• NDRF Disaster Helpline: <span className="font-bold text-white">011-24363260</span></div>
              <div>• State Disaster Response: <span className="font-bold text-white">1070 / 1077</span></div>
            </div>
          </div>
          <div className="mt-2 pt-2 border-t border-red-800 text-[10px] text-red-300 flex items-center gap-1">
            <Radio className="w-3 h-3 text-red-400 animate-pulse" />
            <span>Issued by {primaryAlert.issued_by || "IMD"}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
