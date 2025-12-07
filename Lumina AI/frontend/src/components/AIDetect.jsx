import React, { useState } from "react";
import "../styles.css";

export default function AIDetect() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: true });
    }
    setLoading(false);
  }

  // Helper to determine color based on score
  const getColor = (score) => {
    if (score > 80) return "#ef4444"; // Red (High AI)
    if (score > 40) return "#eab308"; // Yellow (Suspicious)
    return "#22c55e"; // Green (Human)
  };

  return (
    <div className="chat-page" style={{ maxWidth: "800px", margin: "0 auto", paddingBottom: "100px" }}>
      <h1 className="page-title">🛡️ GhostPrint Detective</h1>
      <p className="page-subtitle">Analyze text for invisible AI watermarks.</p>

      <textarea
        className="detect-box"
        placeholder="Paste suspicious text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ height: "150px", fontFamily: "sans-serif", fontSize: "16px" }}
      ></textarea>

      <button className="chat-send" onClick={analyze} disabled={loading}>
        {loading ? "Scanning..." : "Analyze Text"}
      </button>

      {/* DASHBOARD RESULT UI */}
      {result && !result.error && (
        <div style={{ marginTop: "40px", animation: "fadeIn 0.5s" }}>
          
          {/* 1. THE METER */}
          <div style={{ 
            background: "#0c1424", 
            padding: "30px", 
            borderRadius: "20px", 
            border: `2px solid ${getColor(result.probability)}`,
            position: "relative",
            overflow: "hidden"
          }}>
            {/* Background Glow */}
            <div style={{
                position: "absolute", top: 0, left: 0, right: 0, bottom: 0,
                background: getColor(result.probability), opacity: 0.05, zIndex: 0
            }}></div>

            <div style={{ position: "relative", zIndex: 1 }}>
                <h3 style={{ margin: 0, color: "#94a3b8", fontSize: "14px", textTransform: "uppercase", letterSpacing: "1px" }}>
                    AI Probability Score
                </h3>
                
                <div style={{ fontSize: "60px", fontWeight: "800", color: getColor(result.probability), margin: "10px 0" }}>
                    {result.probability}%
                </div>

                {/* Progress Bar Container */}
                <div style={{ width: "100%", height: "12px", background: "#1e293b", borderRadius: "10px", overflow: "hidden" }}>
                    <div style={{ 
                        width: `${result.probability}%`, 
                        height: "100%", 
                        background: getColor(result.probability),
                        transition: "width 1s ease-out"
                    }}></div>
                </div>

                <div style={{ display: "flex", justifyContent: "space-between", marginTop: "20px", textAlign: "left" }}>
                    <div>
                        <div style={{ fontSize: "12px", color: "#94a3b8" }}>DETECTED SOURCE</div>
                        <div style={{ fontSize: "18px", color: "white", fontWeight: "bold" }}>{result.source}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                        <div style={{ fontSize: "12px", color: "#94a3b8" }}>ENGINE USED</div>
                        <div style={{ fontSize: "18px", color: "white", fontWeight: "bold" }}>{result.model}</div>
                    </div>
                </div>
            </div>
          </div>

          {/* 2. ANALYSIS TEXT */}
          <div style={{ marginTop: "20px", padding: "20px", background: "#1e293b", borderRadius: "12px", borderLeft: "4px solid white" }}>
            <h4 style={{ margin: "0 0 5px 0", color: "white" }}>Analysis Report</h4>
            <p style={{ margin: 0, color: "#cbd5e1" }}>{result.analysis}</p>
          </div>

        </div>
      )}
    </div>
  );
}