import React, { useState } from "react";
import Chat from "./components/Chat";
import CodeHelp from "./components/CodeHelp";
import AIDetect from "./components/AIDetect";
import Training from "./components/Training";
import NavBar from "./components/NavBar";
import "./styles.css";

export default function App() {
  const [page, setPage] = useState("chat");

  return (
    <div className="app-container">
      <NavBar setPage={setPage} active={page} />

      {page === "chat" && <Chat />}
      {page === "code" && <CodeHelp />}
      {page === "detect" && <AIDetect />}
      {page === "train" && <Training />}
    </div>
  );
}
