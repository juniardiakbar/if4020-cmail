import { useState, useEffect } from "react";
import swal from "sweetalert";
import {
  Container,
  Row,
  Col,
  FormGroup,
  Label,
  Input,
  Button,
  CustomInput,
} from "reactstrap";

function Send() {
  const [to, setTo] = useState("");
  const [toValid, setTovalid] = useState(false);
  const [subject, setSubject] = useState("");
  const [content, setContent] = useState("");
  const [sign, setSign] = useState(false);
  const [signKey, setSignKey] = useState("");
  const [encrypt, setEncrypt] = useState(false);
  const [encryptKey, setEncryptKey] = useState("");
  const [encryptMode, setEncryptMode] = useState("");

  useEffect(() => {
    if (!sign) {
      setSignKey("");
    }

    if (!encrypt) {
      setEncryptKey("");
      setEncryptMode("");
    }
  }, [sign, encrypt]);

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
        signature: sign,
        signatureKey: signKey,
      }),
    })
      .then((response) => response.json())
      .then(({ status, message }) => {
        swal(message).then(() => {
          window.location.reload();
        });
      });
  };

  return (
    <Container>
      <Row>
        <Col sm="12" md={{ size: 6, offset: 3 }}>
          <FormGroup>
            <Label for="to">To:</Label>
            <Input
              placeholder="Destinantion..."
              valid={toValid && to !== ""}
              invalid={!toValid && to !== ""}
              onChange={(e) => {
                const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                setTo(e.target.value);
                setTovalid(re.test(e.target.value.toLowerCase()));
              }}
            />
          </FormGroup>
          <FormGroup>
            <Label for="subject">Subject:</Label>
            <Input
              placeholder="Subject..."
              onChange={(e) => setSubject(e.target.value)}
            />
          </FormGroup>
          <FormGroup>
            <Label for="body">Body:</Label>
            <Input
              placeholder="Body..."
              type="textarea"
              name="text"
              id="body"
              onChange={(e) => setContent(e.target.value)}
            />
          </FormGroup>

          <FormGroup>
            <CustomInput
              type="switch"
              id="encrypt"
              name="encrypt"
              label="Enkripsi"
              value={encrypt}
              onClick={(e) => setEncrypt(!encrypt)}
            />
          </FormGroup>
          <FormGroup hidden={!encrypt}>
            <Label for="encryptKey">Kunci Enkripsi:</Label>
            <Input
              id="encryptKey"
              placeholder="kunci..."
              onChange={(e) => setEncryptKey(e.target.value)}
            />
          </FormGroup>
          <FormGroup hidden={!encrypt}>
            <Label for="encryptMode">Mode Enkripsi:</Label>
            <CustomInput
              type="select"
              id="encryptMode"
              name="encryptMode"
              onChange={(e) => setEncryptMode(e.target.value)}
            >
              <option value="">Select</option>
              <option value="ebc">EBC</option>
              <option value="cbc">CBC</option>
              <option value="counter">Counter</option>
            </CustomInput>
          </FormGroup>
          <FormGroup>
            <CustomInput
              type="switch"
              id="sign"
              name="sign"
              label="Tanda Tangan"
              value={sign}
              onClick={(e) => setSign(!sign)}
            />
          </FormGroup>
          <FormGroup hidden={!sign}>
            <Label for="signKey">Kunci Tanda Tangan:</Label>
            <Input
              id="signKey"
              placeholder="kunci..."
              onChange={(e) => setSignKey(e.target.value)}
            />
          </FormGroup>
          <Button color="primary" onClick={() => sendEmail()}>
            Kirim Email
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Send;
