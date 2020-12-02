import React, { useEffect, useState } from "react";
import {
  Button,
  Container,
  Collapse,
  FormGroup,
  Input,
  Label,
  Modal,
  ModalFooter,
  ModalBody,
  ModalHeader,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";

function NavBar({ setPage }) {
  const [isOpen, setIsOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [publicKey, setPublicKey] = useState("");
  const [privateKey, setPrivateKey] = useState("");

  const toggle = () => setIsOpen(!isOpen);
  const toggleModal = () => setModalOpen(!modalOpen);

  const generateKey = () => {
    fetch(`http://127.0.0.1:5000/keygen`)
      .then((response) => response.json())
      .then(({ publicKey: pbKey, privateKey: prKey }) => {
        setPublicKey(pbKey);
        setPrivateKey(prKey);
      });
    toggleModal();
  };

  const downloadFile = (value, filename) => {
    const element = document.createElement("a");
    const file = new Blob([value], {
      type: "text/plain",
    });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  };

  const downloadKeys = () => {
    downloadFile(publicKey, "key.pub");
    downloadFile(publicKey, "key.pri");
  };

  return (
    <Navbar color="light" light expand="md">
      <Container>
        <NavbarBrand
          onClick={() => setPage("send")}
          style={{ cursor: "pointer" }}
        >
          cMail
        </NavbarBrand>
        <NavbarToggler onClick={toggle} />
        <Collapse isOpen={isOpen} navbar>
          <Nav className="mr-auto" navbar>
            <NavItem
              onClick={() => setPage("inbox")}
              style={{ cursor: "pointer" }}
            >
              <NavLink>Inbox</NavLink>
            </NavItem>
            <NavItem
              onClick={() => setPage("sent")}
              style={{ cursor: "pointer" }}
            >
              <NavLink>Sent Mail</NavLink>
            </NavItem>
            <NavItem onClick={generateKey} style={{ cursor: "pointer" }}>
              <NavLink>Generate Key</NavLink>
            </NavItem>
          </Nav>
        </Collapse>
      </Container>
      <Modal isOpen={modalOpen} toggle={toggleModal} style={{ marginTop: 144 }}>
        <ModalHeader toggle={toggleModal}>Generate Key</ModalHeader>
        <ModalBody>
          <FormGroup>
            <Label>Kunci Publik</Label>
            <Input
              disabled
              id="signatureKey"
              placeholder="Kunci Publik.."
              value={publicKey}
            />
          </FormGroup>
          <FormGroup>
            <Label>Kunci Privat</Label>
            <Input
              disabled
              id="signatureKey"
              placeholder="Kunci Privat.."
              value={privateKey}
            />
          </FormGroup>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={downloadKeys}>
            Download
          </Button>
          <Button color="secondary" onClick={() => setModalOpen(false)}>
            Cancel
          </Button>
        </ModalFooter>
      </Modal>
    </Navbar>
  );
}

export default NavBar;
