import React, { useState } from "react";

export default function InputBox({ onSend, loading }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-row">
      <textarea
        className="input-textarea"
        placeholder="Type the code you want... (e.g. 'Write a Python function to merge two sorted lists')"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKey}
        rows={2}
      />
      <button className="btn primary" onClick={handleSend} disabled={loading}>
        {loading ? "Lumina is thinking..." : "Send"}
      </button>
    </div>
  );
}
