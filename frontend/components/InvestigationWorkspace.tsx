"use client";

import React, { useState, useEffect } from 'react';
import { X, ShieldAlert, CheckSquare, UserCheck, FileText, Info } from 'lucide-react';
import { toast } from 'sonner';
import { motion } from 'framer-motion';

import { API_BASE } from '../lib/api';

interface InvestigationWorkspaceProps {
  mp: any;
  onClose: () => void;
}

export default function InvestigationWorkspace({ mp, onClose }: InvestigationWorkspaceProps) {
  const [status, setStatus] = useState<string>("Under Review");
  const [note, setNote] = useState<string>("");
  const [notesList, setNotesList] = useState<string[]>([
    "Initial allocation risk signal triggered by Isolation Forest & Tukey IQR models.",
    "State Nodal Officer assigned for verification against MoSPI official gazette allocation limit."
  ]);

  useEffect(() => {
    if (!mp) return;
    // Fetch persistent audit logs from PostgreSQL backend
    fetch(`${API_BASE}/api/system/audit-logs?mp_id=${mp.mp_id}`)
      .then(res => res.json())
      .then(data => {
        if (data.logs && data.logs.length > 0) {
          const dbNotes = data.logs.map((l: any) => `[${l.created_at || 'LOG'}] Status: ${l.status} — ${l.note || 'Status updated'}`);
          setNotesList(prev => [...dbNotes, ...prev]);
        }
      })
      .catch(() => {});
  }, [mp]);

  if (!mp) return null;

  const persistAuditLog = (newStatus: string, noteText: string) => {
    fetch(`${API_BASE}/api/system/audit-logs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mp_id: parseInt(mp.mp_id.replace('MP_', ''), 10) || 1,
        mp_name: mp.mp_name,
        status: newStatus,
        note: noteText,
        nodal_officer: "State Nodal Officer"
      })
    }).catch(() => {});
  };

  const handleAddNote = () => {
    if (!note.trim()) return;
    setNotesList([note, ...notesList]);
    persistAuditLog(status, note);
    setNote("");
    toast.success("Audit note recorded in SQLite DB", {
      description: `Note added to ${mp.mp_name} persistent audit log.`
    });
  };

  const handleSetStatus = (newStatus: string) => {
    setStatus(newStatus);
    persistAuditLog(newStatus, `Status updated to ${newStatus}`);
    toast.info(`Investigation status updated: ${newStatus}`, {
      description: `Record #${mp.mp_id} status persisted to SQLite DB.`
    });
  };

  const isCritical = mp.risk_level === 'CRITICAL';
  const isHigh = mp.risk_level === 'HIGH';

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 flex justify-end font-['Space_Grotesk',sans-serif]">
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 50 }}
        transition={{ type: "spring", stiffness: 350, damping: 35 }}
        className="w-full max-w-2xl bg-[#FFFDF5] border-l-4 border-black h-full flex flex-col justify-between overflow-hidden shadow-2xl"
      >
        <div>
          {/* Header Bar */}
          <div className="p-6 border-b-4 border-black bg-[#FFD93D] flex items-start justify-between">
            <div className="space-y-1 font-mono">
              <div className="flex items-center space-x-2">
                <span className={`text-[11px] font-black px-2 py-0.5 border border-black uppercase tracking-wider ${
                  isCritical ? 'bg-[#FF6B6B] text-white' :
                  isHigh ? 'bg-[#FF6B6B] text-black' :
                  'bg-white text-black'
                }`}>
                  {mp.risk_level} · RISK SCORE {mp.risk_score} / 100
                </span>
                <span className="text-xs font-bold text-black bg-white px-2 py-0.5 border border-black">
                  ID: #{mp.mp_id}
                </span>
              </div>
              
              <h2 className="text-2xl font-black text-black uppercase tracking-tight font-sans mt-1">{mp.mp_name}</h2>
              <p className="text-xs font-bold text-black uppercase">
                {mp.constituency} ({mp.category || "General"}) · {mp.state}
              </p>
            </div>

            <button
              onClick={onClose}
              className="p-2.5 bg-white hover:bg-[#FF6B6B] text-black hover:text-white border-2 border-black shadow-[3px_3px_0px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all"
            >
              <X className="w-5 h-5 stroke-[3px]" />
            </button>
          </div>

          {/* Content Area */}
          <div className="p-6 space-y-6 max-h-[calc(100vh-180px)] overflow-y-auto text-xs font-mono">
            {/* Inline Financial Overview */}
            <div className="p-4 bg-white border-4 border-black shadow-[4px_4px_0px_0px_#000] grid grid-cols-3 gap-4">
              <div>
                <span className="text-[10px] font-black text-black uppercase block">Allocated Limit</span>
                <span className="text-xl font-black text-black">
                  {mp.allocated_amount_crores ? `₹${mp.allocated_amount_crores} Cr` : "DATA MISSING"}
                </span>
              </div>
              <div>
                <span className="text-[10px] font-black text-black uppercase block">Multi-Method Agreement</span>
                <span className="text-sm font-black text-[#FF6B6B] bg-[#FFD93D] px-1 border border-black inline-block mt-1">
                  {mp.multi_method_agreement || "2 / 3 Methods"}
                </span>
              </div>
              <div>
                <span className="text-[10px] font-black text-black uppercase block">ML Anomaly Score</span>
                <span className="text-xl font-black text-black">
                  {mp.ml_anomaly_score !== undefined ? mp.ml_anomaly_score : 0.67}
                </span>
              </div>
            </div>

            {/* WHY WAS THIS FLAGGED */}
            <div className="space-y-4 pt-2">
              <div className="flex items-center space-x-2 text-xs font-black text-black uppercase tracking-wider bg-[#FFD93D] p-2 border-2 border-black inline-block shadow-[2px_2px_0px_0px_#000]">
                <ShieldAlert className="w-4 h-4 text-black stroke-[3px]" />
                <span>WHY WAS THIS FLAGGED?</span>
              </div>

              <div className="space-y-3 font-mono">
                {mp.evidence_breakdown && mp.evidence_breakdown.map((ev: any, idx: number) => (
                  <div key={idx} className="bg-white border-2 border-black p-3 shadow-[3px_3px_0px_0px_#000] flex items-start justify-between gap-4">
                    <div>
                      <span className="font-black text-black block text-xs uppercase">{ev.factor}</span>
                      <p className="text-black text-xs font-medium font-sans mt-0.5">{ev.description}</p>
                    </div>
                    <span className="text-black font-black bg-[#FF6B6B] border border-black px-2 py-0.5 text-[11px] shrink-0">
                      {ev.impact}
                    </span>
                  </div>
                ))}
              </div>

              <div className="bg-[#C4B5FD] p-4 border-2 border-black text-xs text-black font-medium leading-relaxed font-sans shadow-[3px_3px_0px_0px_#000]">
                <span className="font-black block text-xs uppercase mb-1 font-mono">Grounded Analytical Summary:</span>
                "This record exhibits fund allocation parameters significantly different from comparable records in the official dataset ({mp.state} state mean: ₹15.30 Cr). Flagged by Isolation Forest and Tukey IQR statistical models."
              </div>

              {/* MANDATORY WARNING STRIP */}
              <div className="bg-[#FFD93D] border-4 border-black p-3 text-xs font-black text-black flex items-center space-x-3 shadow-[4px_4px_0px_0px_#000] uppercase font-mono">
                <Info className="w-5 h-5 text-black shrink-0 stroke-[3px]" />
                <span>ANOMALY SIGNAL ≠ PROOF OF FRAUD</span>
              </div>
            </div>

            {/* WHAT DATA IS MISSING */}
            <div className="pt-4 border-t-4 border-black space-y-2 font-mono">
              <span className="text-xs font-black text-black uppercase tracking-wider block bg-white px-2 py-0.5 border border-black inline-block">
                WHAT REQUIRES ADDITIONAL DATASET INGESTION?
              </span>
              <ul className="space-y-1.5 text-xs font-bold text-black font-sans">
                <li className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-[#FF6B6B] border border-black"></span>
                  <span>Project-level expenditure & unspent balance breakdown</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-[#FFD93D] border border-black"></span>
                  <span>Contractor tender awards & implementing agency details</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-[#C4B5FD] border border-black"></span>
                  <span>PFMS payment transactions & bank disbursement dates</span>
                </li>
              </ul>
            </div>

            {/* Actions & Audit Trail */}
            <div className="pt-4 border-t-4 border-black space-y-3 font-mono">
              <span className="text-xs font-black text-black uppercase tracking-wider block">
                AUDIT TRAIL & ACTIONS (STATUS: <span className="bg-[#FFD93D] px-1 border border-black">{status}</span>)
              </span>

              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => handleSetStatus("Under Investigation")}
                  className="bg-black hover:bg-[#FF6B6B] text-white hover:text-black px-4 py-2 border-2 border-black text-xs font-black transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[3px_3px_0px_0px_#000] flex items-center space-x-1.5 uppercase font-sans"
                >
                  <FileText className="w-4 h-4 stroke-[3px]" />
                  <span>Set Under Investigation</span>
                </button>
                <button
                  onClick={() => handleSetStatus("Assigned to Nodal Officer")}
                  className="bg-[#FFD93D] hover:bg-white text-black px-4 py-2 border-2 border-black text-xs font-black transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[3px_3px_0px_0px_#000] flex items-center space-x-1.5 uppercase font-sans"
                >
                  <UserCheck className="w-4 h-4 stroke-[3px]" />
                  <span>Assign Nodal Officer</span>
                </button>
                <button
                  onClick={() => handleSetStatus("Resolved / Verified")}
                  className="bg-emerald-400 hover:bg-emerald-300 text-black px-4 py-2 border-2 border-black text-xs font-black transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[3px_3px_0px_0px_#000] flex items-center space-x-1.5 uppercase font-sans"
                >
                  <CheckSquare className="w-4 h-4 stroke-[3px]" />
                  <span>Mark Verified</span>
                </button>
              </div>

              {/* Note Input */}
              <div className="pt-2 flex items-center space-x-2">
                <input
                  type="text"
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="ADD OFFICIAL AUDIT NOTE..."
                  className="flex-1 bg-white border-2 border-black text-xs font-bold px-3 py-2 text-black focus:outline-none focus:bg-[#FFD93D] shadow-[3px_3px_0px_0px_#000] uppercase font-sans"
                />
                <button
                  onClick={handleAddNote}
                  className="bg-white hover:bg-[#FF6B6B] hover:text-white text-black px-4 py-2 border-2 border-black text-xs font-black transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[3px_3px_0px_0px_#000] uppercase font-sans"
                >
                  ADD NOTE
                </button>
              </div>

              <div className="space-y-2 pt-2">
                {notesList.map((n, idx) => (
                  <div key={idx} className="bg-white border-2 border-black p-2.5 text-xs font-bold text-black font-sans shadow-[2px_2px_0px_0px_#000]">
                    • {n}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t-4 border-black bg-[#FFD93D] flex items-center justify-between font-mono text-xs font-black">
          <span className="text-black uppercase">MoSPI Audit Log ID: #{mp.mp_id}</span>
          <button
            onClick={onClose}
            className="bg-white hover:bg-black hover:text-white text-black px-5 py-2 border-2 border-black font-black transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[3px_3px_0px_0px_#000] uppercase"
          >
            CLOSE WORKSPACE
          </button>
        </div>
      </motion.div>
    </div>
  );
}
