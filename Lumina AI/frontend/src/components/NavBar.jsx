import React from "react";
import "../styles.css";

export default function NavBar({ setPage, active }) {
  return (
    <div className="navbar">
      <div className="nav-left">
        <h2 className="logo">Lumina</h2>
        <span className="subtitle">AI — Thinking...</span>
      </div>

      <div className="nav-right">
        <button className={active==="chat" ? "active" : ""} onClick={() => setPage("chat")}>Chat</button>
        <button className={active==="detect" ? "active" : ""} onClick={() => setPage("detect")}>AI Detection</button>
        <button className={active==="code" ? "active" : ""} onClick={() => setPage("code")}>Code Help</button>
        <button className={active==="train" ? "active" : ""} onClick={() => setPage("train")}>Training</button>
      </div>
    </div>
  );
}
