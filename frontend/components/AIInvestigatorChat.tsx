"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { toast } from 'sonner';
import { motion } from 'framer-motion';

import { API_BASE, apiFetch } from '../lib/api';

export default function AIInvestigatorChat() {
  const [query, setQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [messages, setMessages] = useState<any[]>([
    {
      sender: 'assistant',
      answer: "WELCOME TO MPLADS INTELLIGENCE QUERY ENGINE. ASK GROUNDED QUESTIONS REGARDING CONSTITUENCY ALLOCATION LIMITS, STATISTICAL OUTLIERS, BASELINE DEVIATIONS, AND STATE ANALYTICS.",
      evidence: ["543 OFFICIAL MoSPI MP ALLOCATION LIMITS INGESTED"],
      source: "Allocated Limit for Honble MPs.csv",
      limitation: "DATASET CONTAINS ALLOCATION LIMITS PER MP. WORK-LEVEL EXPENDITURE REQUIRES ADDITIONAL DATASET INGESTION."
    }
  ]);

  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const suggestedQuestions = [
    "Why is Malkajgiri showing an allocation anomaly?",
    "Which state has the highest total allocation?",
    "Compare Maharashtra allocation with Gujarat average",
    "Show the highest risk allocation records",
    "Which constituency has missing allocation data?"
  ];

  const handleSend = async (textToSend?: string) => {
    const promptText = textToSend || query;
    if (!promptText.trim()) return;

    const userMsg = { sender: 'user', text: promptText };
    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setQuery("");
    setLoading(true);

    try {
      const res = await apiFetch('/api/ai/investigate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: promptText })
      });
      const data = await res.json();

      const botMsg = {
        sender: 'assistant',
        answer: data.answer,
        evidence: data.evidence_used || [],
        source: "Allocated Limit for Honble MPs.csv (Official MoSPI Dataset)",
        limitation: data.notice || "Grounded strictly in verified MoSPI allocation limits.",
        query_type: data.query_type
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      toast.error("Failed to fetch response from backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-['Space_Grotesk',sans-serif] max-w-4xl mx-auto">
      {/* Header Title */}
      <div className="space-y-2 bg-[#FFD93D] p-5 border-4 border-black shadow-[8px_8px_0px_0px_#000]">
        <div className="flex items-center space-x-2 text-xs font-black text-black uppercase tracking-wider font-mono">
          <Sparkles className="w-4 h-4 stroke-[3px]" />
          <span>GROUNDED TOOL-CALLING ENGINE</span>
        </div>
        <h1 className="text-3xl font-black text-black uppercase tracking-tight">ASK MPLADS INTELLIGENCE</h1>
        <p className="text-xs font-bold text-black font-mono">
          Zero-hallucination query interface connected to official MoSPI dataset and Scikit-Learn anomaly detectors.
        </p>
      </div>

      {/* Suggested Prompt Chips */}
      <div className="flex flex-wrap gap-2">
        {suggestedQuestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            className="bg-white hover:bg-[#FF6B6B] hover:text-white border-2 border-black text-black text-xs font-black px-3.5 py-2 transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[3px_3px_0px_0px_#000] text-left uppercase"
          >
            "{q}"
          </button>
        ))}
      </div>

      {/* Chat Messages Container */}
      <div className="space-y-4 min-h-[350px] max-h-[500px] overflow-y-auto pr-1">
        {messages.map((m, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-5 border-4 border-black text-xs font-mono space-y-3 ${
              m.sender === 'user'
                ? "bg-black text-white ml-auto max-w-lg font-bold shadow-[6px_6px_0px_0px_#FFD93D]"
                : "bg-white text-black shadow-[8px_8px_0px_0px_#000]"
            }`}
          >
            {m.sender === 'user' ? (
              <p className="uppercase">{m.text}</p>
            ) : (
              <div className="prose prose-xs max-w-none text-black font-sans font-bold leading-relaxed whitespace-pre-wrap">
                {m.answer}
              </div>
            )}
          </motion.div>
        ))}

        {loading && (
          <div className="bg-[#FFD93D] border-4 border-black p-4 font-mono font-black text-xs text-black animate-pulse shadow-[4px_4px_0px_0px_#000]">
            ANALYZING MoSPI DATASET RECORDS...
          </div>
        )}

        {/* Dummy div anchor for auto-scrolling to newest message */}
        <div ref={chatEndRef} />
      </div>

      {/* Query Input */}
      <div className="flex items-center space-x-2 pt-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="ASK WHY A CONSTITUENCY WAS FLAGGED OR COMPARE STATE BASELINES..."
          className="flex-1 bg-white border-4 border-black text-xs font-black px-4 py-3 text-black focus:outline-none focus:bg-[#FFD93D] shadow-[4px_4px_0px_0px_#000] uppercase font-sans"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading}
          className="bg-[#FF6B6B] hover:bg-black hover:text-white text-black font-black text-xs px-6 py-3 border-4 border-black transition-all active:translate-x-[2px] active:translate-y-[2px] active:shadow-none shadow-[4px_4px_0px_0px_#000] flex items-center space-x-2 uppercase tracking-wide"
        >
          <span>QUERY</span>
          <Send className="w-4 h-4 stroke-[3px]" />
        </button>
      </div>
    </div>
  );
}
