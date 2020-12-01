import { useState } from "react";
import swal from "sweetalert";

import "./styles.scss";

function Send({ encryptKey, encryptMode }) {
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [content, setContent] = useState("");
  const [sign, setSign] = useState(false);

  const sendEmail = () => {
    fetch("http://127.0.0.1:5000/send", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        to,
        subject,
        message: content,
        encryptKey,
        encryptMode,
        sign
      }),
    })
      .then((response) => response.json())
      .then(({ status, message }) => {
        if (status === "200") {
          setTo("");
          setSubject("");
          setContent("");
        }
        swal(message);
      });
  };

  return (
    <form>
      <div className="title">Send Email</div>
      <div>
        <div className="label">to</div>
        <input
          value={to}
          onChange={(e) => setTo(e.target.value)}
          className="field"
          placeholder="Destination..."
        />
      </div>
      <div>
        <div className="label">subject</div>
        <input
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          className="field"
          placeholder="Subject..."
        />
      </div>
      <div>
        <div className="label">content</div>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="field"
          rows="5"
          placeholder="Email content..."
        />
      </div>
      <span className="sign" onClick={() => setSign(!sign)}>
        <span>Sign email?</span>
        <input className="checkbox" type="checkbox" checked={sign} />
      </span>
      <button type="button" onClick={sendEmail}>
        Submit
      </button>
    </form>
  );
}

export default Send;
