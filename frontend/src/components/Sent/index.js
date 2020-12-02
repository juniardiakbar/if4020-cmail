import { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import {
  Card,
  Button,
  CardTitle,
  CardText,
  CardHeader,
  CardBody,
  FormGroup,
  Input,
  CustomInput,
  Row,
  Col,
  Container,
} from "reactstrap";

function Sent({}) {
  const [inbox, setInbox] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const [encryptKey, setEncryptKey] = useState("");
  const [encryptMode, setEncryptMode] = useState("");

  const refresh = () => {
    fetch(
      `http://127.0.0.1:5000/sent?encryptKey=${encryptKey}&encryptMode=${encryptMode}`
    )
      .then((response) => response.json())
      .then(({ data }) => setInbox(data));
    setHasMore(true);
    setPage(1);
  };

  useEffect(refresh, []);

  const getMoreInbox = () => {
    fetch(
      `http://127.0.0.1:5000/sent?encryptKey=${encryptKey}&encryptMode=${encryptMode}&page=${
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
          inbox.map(({ to, subject, body }) => (
            <Card style={{ marginBottom: 16 }}>
              <CardHeader>
                <CardTitle tag="h5">{to}</CardTitle>
                <CardTitle tag="h6">{subject}</CardTitle>
              </CardHeader>
              <CardBody>
                <CardText style={{ whiteSpace: "pre-line" }}>{body}</CardText>
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
    </Container>
  );
}

export default Sent;
