import React, { useState } from "react";
import {
  Container,
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";

function NavBar({ setPage }) {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);

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
          </Nav>
        </Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
