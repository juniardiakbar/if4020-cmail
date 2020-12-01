import "./styles.scss";

function NavBar({ page, setPage }) {
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
    </ul>
  );
}

export default NavBar;
