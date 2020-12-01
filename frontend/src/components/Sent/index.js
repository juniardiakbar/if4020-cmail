import { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";

import "../Inbox/styles.scss";

function Send() {
  const [inbox, setInbox] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const refresh = () => {
    fetch("http://127.0.0.1:5000/sent")
      .then((response) => response.json())
      .then(({ data }) => setInbox(data));
    setHasMore(true);
    setPage(1);
  };

  useEffect(refresh, []);

  const getMoreInbox = () => {
    fetch(`http://127.0.0.1:5000/sent?page=${page + 1}`)
      .then((response) => response.json())
      .then(({ data }) => {
        setHasMore(hasMore && data.length);
        setInbox([...inbox, ...data]);
      });
    setPage(page + 1);
  };

  const renderItems = () => (
    <InfiniteScroll
      style={{ height: "50%" }}
      dataLength={inbox.length}
      next={getMoreInbox}
      hasMore={hasMore}
      loader={<h4>Membuka pesan...</h4>}
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
        inbox.map(({ to, subject, body }) => (
          <div className="email">
            <div className="from">{to}</div>
            <div className="subject">{subject}</div>
            <div className="body">{body}</div>
          </div>
        ))}
    </InfiniteScroll>
  );

  return (
    <form>
      <div className="title">Sent</div>
      {renderItems()}
    </form>
  );
}

export default Send;
