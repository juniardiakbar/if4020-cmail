import { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import {
  Modal,
  ModalFooter,
  ModalBody,
  ModalHeader,
  Card,
  Button,
  CardTitle,
  CardText,
  CardHeader,
  CardBody,
  FormGroup,
  FormText,
  Input,
  CustomInput,
  Container,
  Row,
  Col,
} from "reactstrap";

function Send() {
  const [inbox, setInbox] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMessageId, setSelectedMessageId] = useState(null);
  const [signatureKey, setSignatureKey] = useState("");

  const [encryptKey, setEncryptKey] = useState("");
  const [encryptMode, setEncryptMode] = useState("");
  const [signatureMessage, setSignatureMessage] = useState("");

  const toggleModal = () => {
    setModalOpen(!modalOpen);
    setSignatureMessage("");
  };

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
    fetch("http://127.0.0.1:5000/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id,
        key,
      }),
    })
      .then((response) => response.json())
      .then(({ message }) => {
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

  const onFileChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function (event) {
      setSignatureKey(event.target.result);
    };
    reader.readAsText(file);
  };

  const renderItems = () => (
    <>
      <Row>
        <Col>
          <FormGroup>
            <Input
              id="encryptKey"
              placeholder="Kunci Dekripsi.."
              onChange={(e) => setEncryptKey(e.target.value)}
            />
          </FormGroup>
        </Col>
        <Col>
          <FormGroup>
            <CustomInput
              type="select"
              id="encryptMode"
              name="encryptMode"
              onChange={(e) => setEncryptMode(e.target.value)}
            >
              <option value="">Select Mode</option>
              <option value="ebc">EBC</option>
              <option value="cbc">CBC</option>
              <option value="counter">Counter</option>
            </CustomInput>
          </FormGroup>
        </Col>
        <Col>
          <Button
            color="primary"
            onClick={() => {
              refresh();
              setInbox([]);
            }}
          >
            Submit
          </Button>
        </Col>
      </Row>

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
          <h3 style={{ textAlign: "center" }}>
            &#8595; Tarik untuk me-refresh
          </h3>
        }
        releaseToRefreshContent={
          <h3 style={{ textAlign: "center" }}>
            &#8593; Lepas untuk me-refresh
          </h3>
        }
      >
        {inbox &&
          inbox.map(({ from, subject, body, signature, id }) => (
            <Card style={{ marginBottom: 16 }}>
              <CardHeader>
                <CardTitle tag="h5">{from}</CardTitle>
                <CardTitle tag="h6">{subject}</CardTitle>
              </CardHeader>
              <CardBody>
                <CardText style={{ whiteSpace: "pre-line" }}>{body}</CardText>
                {signature && (
                  <Button
                    onClick={() => {
                      setSelectedMessageId(id);
                      setModalOpen(true);
                    }}
                  >
                    Verify Signature
                  </Button>
                )}
              </CardBody>
            </Card>
          ))}
      </InfiniteScroll>
    </>
  );

  return (
    <Container>
      <Row>
        <Col sm="12" md={{ size: 6, offset: 3 }}>
          {renderItems()}
        </Col>
      </Row>
      <Modal isOpen={modalOpen} toggle={toggleModal} style={{ marginTop: 144 }}>
        <ModalHeader toggle={toggleModal}>Verifikasi email</ModalHeader>
        <ModalBody>
          <FormGroup>
            <Input
              id="signatureKey"
              placeholder="Kunci Verifikasi.."
              value={signatureKey}
              onChange={(e) => setSignatureKey(e.target.value)}
            />
            <FormText>Format: x;y. Contoh: 123;987</FormText>
          </FormGroup>
          <input type="file" onChange={onFileChange} />
          <Button
            style={{ float: "right" }}
            color="primary"
            onClick={() => {
              checkSignature(selectedMessageId, signatureKey);
            }}
          >
            Verify Signature
          </Button>
          <div>{signatureMessage}</div>
        </ModalBody>
        <ModalFooter>
          <Button color="secondary" onClick={toggleModal}>
            Cancel
          </Button>
        </ModalFooter>
      </Modal>
    </Container>
  );
}

export default Send;
