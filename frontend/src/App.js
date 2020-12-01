import "./App.scss";

import { useState } from "react";

import NavBar from "./components/NavBar/index.js";
import Send from "./components/Send/index.js";
import Sent from "./components/Sent/index.js";
import Inbox from "./components/Inbox/index.js";

const PAGE_CLASS = {
  send: Send,
  sent: Sent,
  inbox: Inbox,
};

function App() {
  const [page, setPage] = useState("send");
  const [encryptKey, setEncryptKey] = useState("");
  const [encryptMode, setEncryptMode] = useState("");

  const PageClass = PAGE_CLASS[page];

  return (
    <div className="App">
      <NavBar
        page={page}
        setPage={setPage}
        setEncryptKey={setEncryptKey}
        setEncryptMode={setEncryptMode}
        encryptMode={encryptMode}
      />
      <header className="App-header">
        <PageClass encryptKey={encryptKey} encryptMode={encryptMode} />
      </header>
    </div>
  );
}

export default App;
