import React, { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function CodeHelp() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const askCodeAI = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setOutput(""); // Reset previous output

    try {
      const res = await fetch("http://127.0.0.1:8000/api/codehelp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          language: "python", // Defaulting to Python for now
          prompt: input
        })
      });

      const data = await res.json();
      setOutput(data.reply || "No response received.");
    } catch (err) {
      setOutput("# Error: Could not connect to Lumina Backend.");
    }
    setLoading(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ padding: "40px", maxWidth: "900px", margin: "0 auto", color: "white" }}>
      <h1 style={{ marginBottom: "10px" }}>💻 Code Generator</h1>
      <p style={{ opacity: 0.7, marginBottom: "30px" }}>
        Ask Lumina to write code for you. It will be watermarked instantly.
      </p>

      {/* INPUT AREA */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input
          style={{
            flex: 1,
            padding: "15px",
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "10px",
            color: "white",
            fontSize: "16px",
            fontFamily: "monospace"
          }}
          placeholder="e.g. Create a Python function to calculate Fibonacci series..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askCodeAI()}
        />
        <button
          onClick={askCodeAI}
          disabled={loading}
          style={{
            padding: "0 25px",
            background: "#a66bff",
            borderRadius: "10px",
            border: "none",
            color: "white",
            fontWeight: "bold",
            cursor: loading ? "wait" : "pointer",
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? "Coding..." : "Generate"}
        </button>
      </div>

      {/* OUTPUT AREA (VS Code Style) */}
      {output && (
        <div style={{ 
          background: "#282a36", 
          borderRadius: "12px", 
          overflow: "hidden", 
          border: "1px solid #44475a",
          boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
        }}>
          {/* Header Bar */}
          <div style={{ 
            background: "#44475a", 
            padding: "8px 15px", 
            display: "flex", 
            justifyContent: "space-between", 
            alignItems: "center",
            borderBottom: "1px solid #6272a4"
          }}>
            <div style={{ display: "flex", gap: "6px" }}>
              <div style={{ width: 10, height: 10, borderRadius: "50%", background: "#ff5555" }}></div>
              <div style={{ width: 10, height: 10, borderRadius: "50%", background: "#f1fa8c" }}></div>
              <div style={{ width: 10, height: 10, borderRadius: "50%", background: "#50fa7b" }}></div>
            </div>
            <span style={{ fontSize: "12px", opacity: 0.7, fontFamily: "monospace" }}>generated_code.py</span>
            <button 
              onClick={copyToClipboard}
              style={{
                background: "transparent",
                border: "none",
                color: copied ? "#50fa7b" : "#f8f8f2",
                cursor: "pointer",
                fontSize: "12px",
                fontWeight: "bold"
              }}
            >
              {copied ? "✔ COPIED" : "📋 COPY"}
            </button>
          </div>

          {/* Code Block with Syntax Highlighting */}
          <SyntaxHighlighter 
            language="python" 
            style={dracula} 
            showLineNumbers={true}
            customStyle={{ margin: 0, padding: "20px", fontSize: "14px", lineHeight: "1.5" }}
            wrapLongLines={true}
          >
            {output}
          </SyntaxHighlighter>
        </div>
      )}
    </div>
  );
}