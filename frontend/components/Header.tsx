"use client";

import React, { useState, useEffect, useRef, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Search, Database, Cpu, X, Clock, Trash2, MapPin, User, Shield, LogIn, LogOut, Download, FileText } from 'lucide-react';
import { API_BASE } from '../lib/api';
import LoginModal from './LoginModal';

interface HeaderProps {
  activeTab: string;
  setActiveTab?: (tab: string) => void;
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
  onOpenDataSources?: () => void;
  onOpenModelHealth?: () => void;
}

function SearchBarInput({
  activeTab,
  setActiveTab,
  searchQuery,
  setSearchQuery
}: {
  activeTab: string;
  setActiveTab?: (tab: string) => void;
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
}) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const dropdownRef = useRef<HTMLDivElement>(null);

  const [internalQuery, setInternalQuery] = useState<string>(searchQuery ?? searchParams.get('q') ?? "");
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const [allMPs, setAllMPs] = useState<any[]>([]);

  useEffect(() => {
    try {
      const saved = localStorage.getItem('mplads_recent_searches');
      if (saved) {
        setRecentSearches(JSON.parse(saved));
      }
    } catch {}
  }, []);

  useEffect(() => {
    fetch(`${API_BASE}/api/risk/anomalies`)
      .then(res => res.json())
      .then(data => {
        if (data.anomalies) {
          setAllMPs(data.anomalies);
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (searchQuery !== undefined) {
      setInternalQuery(searchQuery);
    }
  }, [searchQuery]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const saveRecentSearch = (term: string) => {
    const trimmed = term.trim();
    if (!trimmed) return;
    const updated = [trimmed, ...recentSearches.filter(s => s.toLowerCase() !== trimmed.toLowerCase())].slice(0, 5);
    setRecentSearches(updated);
    try {
      localStorage.setItem('mplads_recent_searches', JSON.stringify(updated));
    } catch {}
  };

  const clearRecentSearches = (e: React.MouseEvent) => {
    e.stopPropagation();
    setRecentSearches([]);
    try {
      localStorage.removeItem('mplads_recent_searches');
    } catch {}
  };

  const triggerSearch = (queryText: string) => {
    setInternalQuery(queryText);
    saveRecentSearch(queryText);
    setIsOpen(false);

    if (setSearchQuery) {
      setSearchQuery(queryText);
      if (queryText.trim() && setActiveTab && activeTab !== 'anomalies' && activeTab !== 'mps' && activeTab !== 'risk') {
        setActiveTab('anomalies');
      }
    } else {
      if (queryText.trim()) {
        router.push(`/anomalies?q=${encodeURIComponent(queryText)}`);
      }
    }
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const q = e.target.value;
    setInternalQuery(q);
    setIsOpen(true);

    if (setSearchQuery) {
      setSearchQuery(q);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      triggerSearch(internalQuery);
    }
  };

  const handleClearSearch = () => {
    setInternalQuery("");
    if (setSearchQuery) setSearchQuery("");
  };

  const suggestions = internalQuery.trim()
    ? allMPs.filter(mp =>
        mp.mp_name.toLowerCase().includes(internalQuery.toLowerCase()) ||
        mp.constituency.toLowerCase().includes(internalQuery.toLowerCase()) ||
        mp.state.toLowerCase().includes(internalQuery.toLowerCase())
      ).slice(0, 6)
    : [];

  return (
    <div className="relative w-72" ref={dropdownRef}>
      <div className="relative">
        <Search className="w-4 h-4 text-black absolute left-3 top-1/2 -translate-y-1/2 stroke-[3px]" />
        <input
          type="text"
          value={internalQuery}
          onFocus={() => setIsOpen(true)}
          onChange={handleSearchChange}
          onKeyDown={handleKeyDown}
          placeholder="SEARCH CONSTITUENCY..."
          className="w-full bg-white border-2 border-black text-xs font-bold pl-9 pr-8 py-1.5 text-black placeholder-black/50 focus:outline-none focus:bg-[#FFD93D] shadow-[3px_3px_0px_0px_#000] transition-all uppercase"
        />
        {internalQuery && (
          <button
            onClick={handleClearSearch}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 text-black hover:bg-black hover:text-white p-0.5 font-black text-xs"
          >
            <X className="w-3.5 h-3.5 stroke-[3px]" />
          </button>
        )}
      </div>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border-4 border-black shadow-[4px_4px_0px_0px_#000] z-50 max-h-72 overflow-y-auto font-mono text-xs">
          {suggestions.length > 0 && (
            <div>
              <div className="bg-[#FFD93D] px-3 py-1 font-black text-[10px] uppercase border-b-2 border-black text-black">
                MATCHING CONSTITUENCIES & MPs ({suggestions.length})
              </div>
              {suggestions.map((mp, i) => (
                <div
                  key={i}
                  onClick={() => triggerSearch(mp.constituency || mp.mp_name)}
                  className="px-3 py-2 hover:bg-[#FFE600] cursor-pointer border-b border-black/20 flex flex-col justify-center transition-colors"
                >
                  <div className="flex items-center justify-between font-bold text-black">
                    <span className="truncate flex items-center gap-1">
                      <User className="w-3 h-3 text-black shrink-0" />
                      {mp.mp_name}
                    </span>
                    <span className={`text-[9px] px-1.5 py-0.2 border border-black font-mono font-black ${
                      mp.risk_level === 'CRITICAL' ? 'bg-red-500 text-white' :
                      mp.risk_level === 'HIGH' ? 'bg-amber-400 text-black' :
                      'bg-emerald-300 text-black'
                    }`}>
                      {mp.risk_level}
                    </span>
                  </div>
                  <div className="flex items-center text-[10px] text-black/70 font-semibold gap-1">
                    <MapPin className="w-2.5 h-2.5 text-black shrink-0" />
                    <span>{mp.constituency} · {mp.state}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {internalQuery.trim() === "" && recentSearches.length > 0 && (
            <div>
              <div className="bg-[#C4B5FD] px-3 py-1 font-black text-[10px] uppercase border-b-2 border-black flex justify-between items-center text-black">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" /> RECENT SEARCHES
                </span>
                <button
                  onClick={clearRecentSearches}
                  className="text-[9px] hover:underline flex items-center gap-0.5 text-black"
                >
                  <Trash2 className="w-2.5 h-2.5" /> CLEAR
                </button>
              </div>
              {recentSearches.map((term, i) => (
                <div
                  key={i}
                  onClick={() => triggerSearch(term)}
                  className="px-3 py-2 hover:bg-[#FFFDF5] cursor-pointer border-b border-black/20 flex items-center justify-between font-bold text-black"
                >
                  <span className="flex items-center gap-1.5 text-xs">
                    <Search className="w-3 h-3 text-black/60 stroke-[3px]" />
                    {term}
                  </span>
                  <span className="text-[10px] text-black/50 font-mono">USE</span>
                </div>
              ))}
            </div>
          )}

          {internalQuery.trim() !== "" && suggestions.length === 0 && (
            <div className="p-3 text-center text-black/70 font-bold text-xs bg-[#FFFDF5]">
              NO MATCHES FOR "{internalQuery.toUpperCase()}"
              <p className="text-[10px] font-mono text-black/50 mt-1">Press Enter to search all records</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function Header({
  activeTab,
  setActiveTab,
  searchQuery,
  setSearchQuery,
  onOpenDataSources,
  onOpenModelHealth
}: HeaderProps) {
  const router = useRouter();
  const [showLoginModal, setShowLoginModal] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<any | null>(null);

  useEffect(() => {
    try {
      const savedUser = localStorage.getItem("mplads_user");
      if (savedUser) {
        setCurrentUser(JSON.parse(savedUser));
      }
    } catch {}
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("mplads_auth_token");
    localStorage.removeItem("mplads_user");
    setCurrentUser(null);
  };

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

  return (
    <>
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
          <Suspense fallback={
            <div className="w-72 bg-white border-2 border-black px-3 py-1.5 text-xs font-mono font-bold">
              SEARCHING...
            </div>
          }>
            <SearchBarInput
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
            />
          </Suspense>

          <div className="flex items-center space-x-2 text-xs font-black text-black bg-[#FFD93D] border-2 border-black px-3 py-1.5 shadow-[3px_3px_0px_0px_#000] uppercase">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 border border-black animate-pulse"></span>
            <span>SYSTEM MONITORING</span>
          </div>
        </div>

        {/* Right Tools & Auth */}
        <div className="flex items-center space-x-2 font-mono text-xs">
          {/* Export PDF Download Quick Button */}
          <a
            href={`${API_BASE}/api/exports/pdf`}
            download
            className="flex items-center space-x-1.5 bg-[#FFD93D] hover:bg-black hover:text-white text-black font-bold px-2.5 py-1.5 border-2 border-black shadow-[3px_3px_0px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all uppercase"
            title="Download Official Executive Summary PDF Report"
          >
            <Download className="w-3.5 h-3.5 stroke-[3px]" />
            <span className="hidden lg:inline text-[11px]">PDF REPORT</span>
          </a>

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

          {/* Authentication Badge & Action */}
          {currentUser ? (
            <div className="flex items-center space-x-1.5 bg-[#C4B5FD] border-2 border-black px-2.5 py-1.5 shadow-[3px_3px_0px_0px_#000]">
              <Shield className="w-3.5 h-3.5 text-black stroke-[3px]" />
              <span className="font-black text-[11px] uppercase truncate max-w-[90px]">{currentUser.username}</span>
              <button
                onClick={handleLogout}
                className="text-black hover:text-red-600 font-black p-0.5 border border-black bg-white hover:bg-black text-[9px] uppercase ml-1"
                title="Log out session"
              >
                <LogOut className="w-3 h-3 stroke-[3px]" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowLoginModal(true)}
              className="flex items-center space-x-1 bg-[#FF6B6B] text-white hover:bg-black font-black px-3 py-1.5 border-2 border-black shadow-[3px_3px_0px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all uppercase"
            >
              <LogIn className="w-4 h-4 stroke-[3px]" />
              <span>OFFICER LOGIN</span>
            </button>
          )}
        </div>
      </header>

      {/* Login Modal */}
      {showLoginModal && (
        <LoginModal
          onClose={() => setShowLoginModal(false)}
          onLoginSuccess={(userData) => setCurrentUser(userData)}
        />
      )}
    </>
  );
}
