// Client-side Web Speech API Wrapper for STT and TTS in en-IN, hi-IN, mr-IN

export function listenSpeech(
  language: string,
  onResult: (text: string) => void,
  onError: (err: any) => void
) {
  if (typeof window === 'undefined') return null;

  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
  if (!SpeechRecognition) {
    onError("Speech Recognition not supported in this browser.");
    return null;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  let langCode = 'en-IN';
  if (language === 'hi') langCode = 'hi-IN';
  if (language === 'mr') langCode = 'mr-IN';

  recognition.lang = langCode;

  recognition.onresult = (event: any) => {
    const transcript = event.results[0][0].transcript;
    onResult(transcript);
  };

  recognition.onerror = (event: any) => {
    onError(event.error);
  };

  recognition.start();
  return recognition;
}

export function speakText(text: string, language: string) {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;

  window.speechSynthesis.cancel(); // Stop any active speech

  const utterance = new SpeechSynthesisUtterance(text);
  let langCode = 'en-IN';
  if (language === 'hi') langCode = 'hi-IN';
  if (language === 'mr') langCode = 'mr-IN';

  utterance.lang = langCode;
  utterance.rate = 0.95;

  // Find matching voice if available
  const voices = window.speechSynthesis.getVoices();
  const match = voices.find(v => v.lang.includes(langCode) || v.lang.includes(language));
  if (match) {
    utterance.voice = match;
  }

  window.speechSynthesis.speak(utterance);
}
