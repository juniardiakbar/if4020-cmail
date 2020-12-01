import { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Modal from "react-modal";

import "./styles.scss";

function Send({ encryptKey, encryptMode }) {
  const [inbox, setInbox] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMessageId, setSelectedMessageId] = useState(null);
  const [signatureKey, setSignatureKey] = useState("");

  // Possible buat diganti kalo dah ada API nya
  const [signatureMessage, setSignatureMessage] = useState("");

  const refresh = () => {
    fetch(
      `http://127.0.0.1:5000/inbox?encryptKey=${encryptKey}&encryptMode=${encryptMode}`
    )
      .then((response) => response.json())
      .then(({ data }) => setInbox(data));
    setHasMore(true);
    setPage(1);
  };

  useEffect(refresh, []);

  const checkSignature = (id, key) => {
    setSignatureMessage("Checking...");
    fetch("http://127.0.0.1:5000/checkSignature", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        // Parameternya ganti kalo dah ada API nya
        id,
        key,
      }),
    })
      .then((response) => response.json())
      .then(({ message }) => {
        // Response ganti kalo dah ada API nya
        setSignatureMessage(message);
      });
  };

  const getMoreInbox = () => {
    fetch(
      `http://127.0.0.1:5000/inbox?encryptKey=${encryptKey}&encryptMode=${encryptMode}&page=${
        page + 1
      }`
    )
      .then((response) => response.json())
      .then(({ data }) => {
        setHasMore(hasMore && data.length);
        setInbox([...inbox, ...data]);
      });
    setPage(page + 1);
  };

  const renderItems = () => (
    <InfiniteScroll
      dataLength={inbox.length}
      next={getMoreInbox}
      hasMore={hasMore}
      loader={<p>Membuka pesan...</p>}
      endMessage={
        <p style={{ textAlign: "center" }}>
          <b>--- semua pesan sudah terbaca ---</b>
        </p>
      }
      refreshFunction={refresh}
      pullDownToRefresh
      pullDownToRefreshThreshold={50}
      pullDownToRefreshContent={
        <h3 style={{ textAlign: "center" }}>&#8595; Tarik untuk me-refresh</h3>
      }
      releaseToRefreshContent={
        <h3 style={{ textAlign: "center" }}>&#8593; Lepas untuk me-refresh</h3>
      }
    >
      {inbox &&
        inbox.map(({ from, subject, body, signature, id }) => (
          <div className="email">
            {signature && (
              <button
                type="button"
                className="signature"
                onClick={() => {
                  setSelectedMessageId(id);
                  setModalOpen(true);
                }}
              >
                Check Signature
              </button>
            )}
            <div className="from">{from}</div>
            <div className="subject">{subject}</div>
            <div className="body">{body}</div>
          </div>
        ))}
    </InfiniteScroll>
  );

  return (
    <div>
      <Modal
        className="modal"
        isOpen={modalOpen}
        onRequestClose={() => setModalOpen(false)}
        contentLabel="Check Signature"
      >
        <span className="signature-key">
          <span>Signature Key</span>
          <input
            onChange={(e) => setSignatureKey(e.target.value)}
            placeholder="Input key here..."
          />
          <button
            type="button"
            onClick={() => checkSignature(selectedMessageId, signatureKey)}
          >
            Submit
          </button>
          <div>{signatureMessage}</div>
        </span>
      </Modal>
      <form>
        <div className="title">Inbox</div>
        {renderItems()}
      </form>
    </div>
  );
}

export default Send;
