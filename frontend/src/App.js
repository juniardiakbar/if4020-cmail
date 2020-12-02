// import "./App.scss";

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
  const PageClass = PAGE_CLASS[page];

  return (
    <div className="App">
      <NavBar page={page} setPage={setPage} />
      <header className="App-header">
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: 24,
          }}
        >
          <PageClass />
        </div>
      </header>
    </div>
  );
}

export default App;
