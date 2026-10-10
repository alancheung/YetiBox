import './App.scss'
import type { ReactElement } from 'react';
import { Link, Outlet } from 'react-router';

function Header(): ReactElement {
    return (
        <>
            <Link to="/">YetiBox</Link>
            <Link to="/camera">Camera</Link>
            <Link to="/config">Config</Link>
        </>
    )
}

function AppComponent(): React.JSX.Element {
    return (
        <>
            <Header />
            <Outlet />
        </>
    );
}

export default AppComponent
