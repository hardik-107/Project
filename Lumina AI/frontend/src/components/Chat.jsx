import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

export default function Chat() {
  const [input, setInput] = useState("");
  
  // 1. MEMORY: Load history safely
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem("lumina_history");
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [availableVoices, setAvailableVoices] = useState([]);
  
  const synth = useRef(window.speechSynthesis);
  const messagesEndRef = useRef(null);

  // 2. AUTO-SAVE: Save history whenever it changes
  useEffect(() => {
    localStorage.setItem("lumina_history", JSON.stringify(history));
    scrollToBottom();
  }, [history]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // 3. LOAD VOICES
  useEffect(() => {
    const loadVoices = () => {
      const voices = synth.current.getVoices();
      setAvailableVoices(voices);
    };
    loadVoices();
    if (synth.current.onvoiceschanged !== undefined) {
      synth.current.onvoiceschanged = loadVoices;
    }
  }, []);

  // --- VOICE OUTPUT (Siri-Style) ---
  const speakText = (text) => {
    if (synth.current.speaking) {
      synth.current.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    // Find a soothing voice (Google US, Zira, Samantha)
    const preferredVoice = availableVoices.find(
      (v) => v.name.includes("Google US English") || v.name.includes("Zira") || v.name.includes("Samantha")
    );

    if (preferredVoice) utterance.voice = preferredVoice;
    utterance.rate = 1.0;
    utterance.pitch = 1.0; 

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    synth.current.speak(utterance);
  };

  // --- VOICE INPUT ---
  const startListening = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Browser does not support voice input.");
      return;
    }
    // Toggle: If listening, stop it.
    if (isListening) {
       // Ideally we'd have a ref to the recognition instance to stop it cleanly,
       // but reloading page/state works for simple toggle off in this context
       window.location.reload(); 
       return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    
    setIsListening(true);
    
    recognition.onresult = (e) => {
      setInput(e.results[0][0].transcript);
      setIsListening(false);
    };
    
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    
    recognition.start();
  };

  async function sendMessage(textOverride) {
    const text = textOverride || input.trim();
    if (!text) return;

    // FIX: Generate unique ID to prevent React "key" duplicates
    const userMsgId = Date.now();
    const newMessage = { id: userMsgId, sender: "user", text };
    
    // Optimistic Update
    setHistory((prev) => {
        // Prevent duplicate if user mashes enter
        if (prev.length > 0 && prev[prev.length-1].id === userMsgId) return prev;
        return [...prev, newMessage];
    });

    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      if (!res.ok) throw new Error("Server error");
      
      const aiText = await res.text();
      
      // Add AI Response
      setHistory((prev) => [
        ...prev, 
        { id: Date.now() + 1, sender: "ai", text: aiText }
      ]);

    } catch (err) {
      setHistory((prev) => [...prev, { id: Date.now(), sender: "ai", text: "❌ Connection failed." }]);
    }
    setLoading(false);
  }

  const startNewChat = () => {
    // Clear the active view AND the storage for a fresh start
    if (window.confirm("Start a fresh chat? This clears the current history.")) {
      setHistory([]);
      localStorage.removeItem("lumina_history");
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", background: "#040b18", color: "white" }}>
      
      {/* SIDEBAR */}
      <div style={{ width: "260px", background: "#060d1f", padding: "20px", borderRight: "1px solid #1a2538", display: "flex", flexDirection: "column" }}>
        <h2 style={{ fontSize: "20px", marginBottom: "20px", fontWeight: "700", color: "#a66bff" }}>Lumina AI</h2>
        
        <button onClick={startNewChat} style={{ padding: "12px", background: "#1e293b", border: "1px solid #334155", color: "white", borderRadius: "10px", cursor: "pointer", marginBottom: "15px", fontWeight: "bold", display: "flex", alignItems: "center", gap: "10px", justifyContent: "center" }}>
          <span>+</span> New Chat
        </button>

        <div style={{ flex: 1, overflowY: "auto" }}>
          <div style={{ fontSize: "12px", color: "#64748b", marginBottom: "10px", textTransform: "uppercase", letterSpacing: "1px" }}>History</div>
          {history.slice().reverse().map((h) => (
            <div key={h.id} style={{ padding: "10px", borderRadius: "8px", marginBottom: "5px", fontSize: "13px", color: "#94a3b8", cursor: "pointer", borderBottom: "1px solid #1e293b", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {h.text}
            </div>
          ))}
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div style={{ flex: 1, position: "relative", display: "flex", flexDirection: "column" }}>
        
        {/* HEADER (Clean, No "Voice Enabled" text) */}
        <div style={{ padding: "20px", textAlign: "center" }}>
            <h3 style={{ margin: 0, opacity: 0.8 }}>Lumina Assistant</h3>
        </div>

        {/* CHAT AREA */}
        <div style={{ flex: 1, overflowY: "auto", padding: "20px", display: "flex", flexDirection: "column", gap: "20px" }}>
          {history.length === 0 && (
            <div style={{ textAlign: "center", marginTop: "100px", opacity: 0.5 }}>
                <h1 style={{ fontSize: "2.5rem", marginBottom: "10px" }}>How can I help?</h1>
                <div style={{ display: "flex", gap: "10px", justifyContent: "center", marginTop: "30px" }}>
                    {["Write Python Code", "Explain Quantum Physics", "Healthy Dinner Ideas"].map((suggestion) => (
                        <button key={suggestion} onClick={() => sendMessage(suggestion)} style={{ padding: "10px 20px", background: "#1e293b", border: "1px solid #334155", borderRadius: "20px", color: "white", cursor: "pointer", transition: "0.2s hover" }}>
                            {suggestion}
                        </button>
                    ))}
                </div>
            </div>
          )}
          
          {history.map((m) => (
            <div key={m.id} style={{ display: "flex", justifyContent: m.sender === "user" ? "flex-end" : "flex-start" }}>
              <div style={{ background: m.sender === "user" ? "#3b82f6" : "#1e293b", padding: "15px 20px", borderRadius: "18px", borderBottomLeftRadius: m.sender === "ai" ? "4px" : "18px", borderBottomRightRadius: m.sender === "user" ? "4px" : "18px", maxWidth: "70%", lineHeight: "1.6", position: "relative", boxShadow: "0 4px 6px rgba(0,0,0,0.1)" }}>
                
                {/* Message Content */}
                <div className="markdown-content">
                    <ReactMarkdown>{m.text}</ReactMarkdown>
                </div>
                
                {/* VOICE CONTROL (Only for AI) */}
                {m.sender === "ai" && (
                  <button onClick={() => speakText(m.text)} title={isSpeaking ? "Stop Speaking" : "Read Aloud"} style={{ position: "absolute", bottom: "-32px", left: "0", background: isSpeaking ? "#ef4444" : "transparent", border: "none", color: isSpeaking ? "white" : "#64748b", cursor: "pointer", fontSize: "12px", display: "flex", alignItems: "center", gap: "6px", padding: "4px 10px", borderRadius: "20px", transition: "all 0.2s" }}>
                    {isSpeaking ? "■ Stop" : "🔊 Listen"}
                  </button>
                )}
              </div>
            </div>
          ))}
          
          {loading && (
            <div style={{ alignSelf: "flex-start", paddingLeft: "20px", display: "flex", gap: "5px" }}>
                <div style={{ width: "8px", height: "8px", background: "#94a3b8", borderRadius: "50%", animation: "bounce 1.4s infinite ease-in-out both" }}></div>
                <div style={{ width: "8px", height: "8px", background: "#94a3b8", borderRadius: "50%", animation: "bounce 1.4s infinite ease-in-out both", animationDelay: "0.2s" }}></div>
                <div style={{ width: "8px", height: "8px", background: "#94a3b8", borderRadius: "50%", animation: "bounce 1.4s infinite ease-in-out both", animationDelay: "0.4s" }}></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* INPUT AREA */}
        <div style={{ padding: "20px", background: "#040b18" }}>
            <div style={{ maxWidth: "800px", margin: "0 auto", background: "#0f172a", borderRadius: "40px", padding: "8px 15px", display: "flex", alignItems: "center", gap: "10px", border: "1px solid #334155", boxShadow: "0 -5px 20px rgba(0,0,0,0.2)" }}>
                
                {/* SIRI-STYLE MIC BUTTON */}
                <button onClick={startListening} style={{ width: "40px", height: "40px", borderRadius: "50%", border: "none", background: isListening ? "#ef4444" : "transparent", color: isListening ? "white" : "#94a3b8", cursor: "pointer", fontSize: "20px", transition: "all 0.3s ease", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    {isListening ? "⏹" : "🎙️"}
                </button>

                <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && sendMessage()} placeholder={isListening ? "Listening..." : "Message Lumina..."} style={{ flex: 1, background: "transparent", border: "none", color: "white", fontSize: "16px", outline: "none", padding: "10px" }} />
                
                <button onClick={() => sendMessage()} style={{ padding: "10px 25px", borderRadius: "20px", border: "none", background: "#a66bff", color: "white", fontWeight: "bold", cursor: "pointer" }}>Send</button>
            </div>
        </div>
      </div>
      
      {/* CSS FOR ANIMATIONS & MARKDOWN */}
      <style>{`
        @keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
        .markdown-content p { margin: 0 0 10px 0; }
        .markdown-content pre { background: #0f172a; padding: 10px; borderRadius: 8px; overflow-x: auto; font-family: monospace; }
        .markdown-content code { background: rgba(255,255,255,0.1); padding: 2px 5px; borderRadius: 4px; font-family: monospace; }
        .markdown-content ul { padding-left: 20px; }
      `}</style>
    </div>
  );
}