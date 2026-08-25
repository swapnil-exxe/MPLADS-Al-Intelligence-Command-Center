"use client";

import React, { useState } from 'react';
import { Shield, Key, User, X, AlertCircle, CheckCircle2 } from 'lucide-react';
import { API_BASE } from '../lib/api';

interface LoginModalProps {
  onClose: () => void;
  onLoginSuccess: (userData: any) => void;
}

export default function LoginModal({ onClose, onLoginSuccess }: LoginModalProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError("Username and password are required.");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username.trim(), password: password.trim() })
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Authentication failed");
      }

      // Save token and user info to localStorage
      localStorage.setItem("mplads_auth_token", data.access_token);
      localStorage.setItem("mplads_user", JSON.stringify(data));

      onLoginSuccess(data);
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to authenticate");
    } finally {
      setLoading(false);
    }
  };

  const handleFillDemo = (u: string, p: string) => {
    setUsername(u);
    setPassword(p);
    setError(null);
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 flex items-center justify-center p-4 font-['Space_Grotesk',sans-serif]">
      <div className="bg-[#FFFDF5] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000] w-full max-w-md space-y-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-black hover:bg-black hover:text-white p-1 border-2 border-black font-black"
        >
          <X className="w-5 h-5 stroke-[3px]" />
        </button>

        {/* Header */}
        <div className="space-y-1 border-b-4 border-black pb-4">
          <div className="flex items-center space-x-2 font-mono text-xs font-black uppercase text-black">
            <Shield className="w-4 h-4 text-black stroke-[3px]" />
            <span>OFFICIAL AUTHORIZATION</span>
          </div>
          <h2 className="text-2xl font-black text-black uppercase tracking-tight">
            GOVERNMENT OFFICER LOGIN
          </h2>
          <p className="text-xs font-bold text-black/70 font-mono">
            Authenticate to access Nodal Officer audit actions and model administration.
          </p>
        </div>

        {error && (
          <div className="bg-[#FF6B6B] text-white border-2 border-black p-3 text-xs font-mono font-bold flex items-center space-x-2 shadow-[2px_2px_0px_0px_#000]">
            <AlertCircle className="w-4 h-4 shrink-0 stroke-[3px]" />
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-4 font-mono text-xs">
          <div>
            <label className="block font-black text-black uppercase mb-1">USERNAME</label>
            <div className="relative">
              <User className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-black/60 stroke-[3px]" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. nodal_officer_tg"
                className="w-full bg-white border-2 border-black pl-9 pr-3 py-2 text-black font-bold focus:outline-none focus:bg-[#FFD93D] shadow-[2px_2px_0px_0px_#000]"
              />
            </div>
          </div>

          <div>
            <label className="block font-black text-black uppercase mb-1">PASSWORD</label>
            <div className="relative">
              <Key className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-black/60 stroke-[3px]" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-white border-2 border-black pl-9 pr-3 py-2 text-black font-bold focus:outline-none focus:bg-[#FFD93D] shadow-[2px_2px_0px_0px_#000]"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#FFD93D] hover:bg-black hover:text-white text-black font-black py-3 border-4 border-black shadow-[4px_4px_0px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all uppercase text-sm mt-2"
          >
            {loading ? "VERIFYING CREDENTIALS..." : "LOG IN TO COMMAND CENTER"}
          </button>
        </form>

        {/* Quick Credentials Helper for Verification */}
        <div className="bg-[#FFFDF5] border-2 border-black p-3 space-y-2 font-mono text-[11px]">
          <div className="font-black text-black uppercase text-[10px] border-b border-black/30 pb-1">
            VERIFIED TEST ACCOUNTS (SELECT TO PRE-FILL)
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleFillDemo("nodal_officer_tg", "NodalOfficer@2026")}
              className="bg-[#C4B5FD] hover:bg-black hover:text-white text-black font-bold px-2 py-1 border border-black text-[10px] uppercase"
            >
              NODAL OFFICER (TELANGANA)
            </button>
            <button
              onClick={() => handleFillDemo("admin_mospi", "AdminPassword@2026")}
              className="bg-[#FFD93D] hover:bg-black hover:text-white text-black font-bold px-2 py-1 border border-black text-[10px] uppercase"
            >
              ADMIN (MoSPI DIID)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
