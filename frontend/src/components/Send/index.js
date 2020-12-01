import "./styles.scss";

function Send() {
  return (
    <form>
      <div className="title">Send Email</div>
      <div>
        <div className="label">to</div>
        <input className="field" placeholder="Email content..." />
      </div>
      <div>
        <div className="label">subject</div>
        <input className="field" placeholder="Email content..." />
      </div>
      <div>
        <div className="label">content</div>
        <textarea className="field" rows="5" placeholder="Email content..." />
      </div>
      <input type="submit" value="Submit" />
    </form>
  );
}

export default Send;
