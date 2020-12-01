import "./styles.scss";

function NavBar({ page, setPage, setEncryptKey, encryptMode, setEncryptMode }) {
  return (
    <ul>
      <li>
        <span
          onClick={() => setPage("send")}
          className={page === "send" ? "active" : ""}
        >
          Send
        </span>
      </li>
      <li>
        <span
          onClick={() => setPage("sent")}
          className={page === "sent" ? "active" : ""}
        >
          Sent
        </span>
      </li>
      <li>
        <span
          onClick={() => setPage("inbox")}
          className={page === "inbox" ? "active" : ""}
        >
          Inbox
        </span>
      </li>
      <span className="encryption">
        <select onChange={(e) => setEncryptMode(e.target.value)}>
          <option value="">-- encrypt mode --</option>
          <option value="ecb">ECB</option>
          <option value="cbc">CBC</option>
          <option value="counter">Counter</option>
        </select>
        <input
          onChange={(e) => setEncryptKey(e.target.value)}
          placeholder="Encrypt key..."
          disabled={!encryptMode}
        />
      </span>
    </ul>
  );
}

export default NavBar;
