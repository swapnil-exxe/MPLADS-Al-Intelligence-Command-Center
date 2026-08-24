'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Volume2, Sparkles, User, Bot, Tag, Compass } from 'lucide-react';
import { listenSpeech, speakText } from '@/lib/speech';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  language?: string;
  sector?: string;
  sector_icon?: string;
  advisory?: string;
  rag_citations?: string[];
  is_emergency?: boolean;
  timestamp: string;
}

interface ChatProps {
  language: string;
  onSendMessage: (msg: string) => Promise<any>;
}

export const ChatContainer: React.FC<ChatProps> = ({ language, onSendMessage }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'bot',
      text: 'Namaste! I am WeatherGPT, your AI Weather Intelligence & Decision Support Assistant. Ask me about live weather, 7-day forecasts, travel safety, pesticide spraying, cyclone alerts, or climate comparisons in English, Hindi, or Marathi.',
      language: 'en',
      timestamp: '2026-08-24 21:00'
    }
  ]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (customText?: string) => {
    const textToSend = customText || input;
    if (!textToSend.trim() || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: textToSend,
      language,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (!customText) setInput('');
    setIsLoading(true);

    try {
      const response = await onSendMessage(textToSend);
      if (response) {
        const botMsg: Message = {
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          text: response.text || 'Weather intelligence retrieved.',
          language: response.language || language,
          sector: response.sector,
          sector_icon: response.sector_icon,
          advisory: response.advisory,
          rag_citations: response.rag_citations,
          is_emergency: response.is_emergency,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, botMsg]);

        // Auto speak response via TTS
        speakText(botMsg.text, language);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleVoice = () => {
    if (isListening) {
      setIsListening(false);
      return;
    }

    setIsListening(true);
    listenSpeech(
      language,
      (transcript) => {
        setIsListening(false);
        setInput(transcript);
        handleSend(transcript);
      },
      (err) => {
        setIsListening(false);
        console.error("Speech error:", err);
      }
    );
  };

  const handleQuickQuery = (query: string) => {
    setInput(query);
    handleSend(query);
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 shadow-lg flex flex-col h-[520px] backdrop-blur-md">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-sky-400" />
          <h3 className="text-sm font-semibold text-white">Conversational Weather Intelligence</h3>
        </div>
        <span className="text-xs text-slate-400">Zero-Hallucination Decoupled Engine</span>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin mb-3">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start gap-2.5 ${
              msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            <div
              className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                msg.sender === 'user'
                  ? 'bg-sky-600 text-white'
                  : 'bg-slate-800 text-sky-400 border border-slate-700'
              }`}
            >
              {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div className={`max-w-[82%] rounded-xl p-3 text-xs leading-relaxed ${
              msg.sender === 'user'
                ? 'bg-sky-600 text-white rounded-tr-none'
                : msg.is_emergency
                ? 'bg-red-950 border border-red-700 text-red-100 rounded-tl-none'
                : 'bg-slate-800/90 border border-slate-700/60 text-slate-200 rounded-tl-none'
            }`}>
              <div className="flex items-center justify-between mb-1 text-[10px] text-slate-400 gap-2">
                <span>{msg.sender === 'user' ? 'You' : 'WeatherGPT AI'}</span>
                <div className="flex items-center gap-1.5">
                  <span>{msg.timestamp}</span>
                  {msg.sender === 'bot' && (
                    <button
                      onClick={() => speakText(msg.text, language)}
                      className="p-0.5 hover:text-sky-300 transition-colors"
                      title="Listen to audio response"
                    >
                      <Volume2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>

              <div>{msg.text}</div>

              {/* Sector Advisory Badge */}
              {msg.sector && (
                <div className="mt-2.5 pt-2 border-t border-slate-700/50 flex flex-col gap-1 text-[11px]">
                  <div className="flex items-center gap-1 font-semibold text-sky-300">
                    <span>{msg.sector_icon}</span>
                    <span>{msg.sector} Advisory:</span>
                  </div>
                  <div className="text-slate-300 italic bg-slate-900/50 p-1.5 rounded border border-slate-800">
                    {msg.advisory}
                  </div>
                </div>
              )}

              {/* RAG Citations */}
              {msg.rag_citations && msg.rag_citations.length > 0 && (
                <div className="mt-1.5 flex items-center gap-1 text-[10px] text-slate-400">
                  <Tag className="w-3 h-3 text-emerald-400" />
                  <span>RAG Knowledge Cited: {msg.rag_citations.join(', ')}</span>
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-sky-400 animate-pulse p-2">
            <Bot className="w-4 h-4" />
            <span>Analyzing weather metrics & knowledge base...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Quick Demo Scenario Chips */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 scrollbar-none text-[11px] mb-2">
        <span className="text-slate-400 text-[10px] font-medium flex items-center gap-0.5">
          <Compass className="w-3 h-3 text-sky-400" /> Demo:
        </span>
        <button
          onClick={() => handleQuickQuery("Can I travel from Mumbai to Pune tomorrow afternoon?")}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-0.5 rounded border border-slate-700 whitespace-nowrap transition-colors"
        >
          🚗 Mumbai-Pune Travel
        </button>
        <button
          onClick={() => handleQuickQuery("क्या नाशिक में कल कपास की फसल पर कीटनाशक का छिड़काव करना सुरक्षित है?")}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-0.5 rounded border border-slate-700 whitespace-nowrap transition-colors"
        >
          🌾 Nashik Agri (Hindi)
        </button>
        <button
          onClick={() => handleQuickQuery("रत्नागिरीमध्ये आज समुद्रात मासेमारीसाठी जाणे सुरक्षित आहे का?")}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-0.5 rounded border border-slate-700 whitespace-nowrap transition-colors"
        >
          🚢 Ratnagiri Marine (Marathi)
        </button>
        <button
          onClick={() => handleQuickQuery("Is there any cyclone or flood warning in Puri?")}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-0.5 rounded border border-slate-700 whitespace-nowrap transition-colors"
        >
          🚨 Puri Cyclone Check
        </button>
      </div>

      {/* Input Bar */}
      <div className="flex items-center gap-2">
        <button
          onClick={toggleVoice}
          className={`p-2.5 rounded-lg border transition-all ${
            isListening
              ? 'bg-red-600 text-white border-red-500 animate-pulse'
              : 'bg-slate-800 hover:bg-slate-700 text-sky-400 border-slate-700'
          }`}
          title={isListening ? 'Stop Listening' : 'Speak to Query (STT)'}
        >
          {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={
            isListening
              ? 'Listening to speech...'
              : language === 'hi'
              ? 'मौसम या सुरक्षा के बारे में पूछें...'
              : language === 'mr'
              ? 'हवामान किंवा सुरक्षिततेबद्दल विचारा...'
              : 'Ask WeatherGPT about weather, travel, crops, warnings...'
          }
          className="flex-1 bg-slate-800 border border-slate-700 text-white text-xs rounded-lg px-3 py-2.5 focus:outline-none focus:border-sky-500"
        />

        <button
          onClick={() => handleSend()}
          disabled={isLoading || !input.trim()}
          className="bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white p-2.5 rounded-lg transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
