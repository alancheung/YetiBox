import './App.scss'
import type { ReactElement } from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { Link, Outlet } from 'react-router';

function Header(): ReactElement {
    return (
        <Navbar expand="lg" bg="dark" data-bs-theme="dark">
            <Container fluid>
                <Navbar.Brand as={Link} to="/">YetiBox</Navbar.Brand>
                <Navbar.Toggle aria-controls="main-navbar" />
                <Navbar.Collapse id="main-navbar">
                    <Nav>
                        <Nav.Link as={Link} to="/camera">Camera</Nav.Link>
                        <Nav.Link as={Link} to="/config">Config</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
                {/* TODO - timestamp or something Centered text in the NavBar */}
                <Navbar.Text className="position-absolute start-50 translate-middle-x">
                    My special text
                </Navbar.Text>
            </Container>
        </Navbar>
    )
}

function AppComponent(): ReactElement {
    return (
        <>
            <Header />
            <Outlet />
        </>
    );
}

export default AppComponent
