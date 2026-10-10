import { Link } from 'react-router';
import './App.scss'
import type { ReactElement } from 'react';
import { YetiBoxRouter } from './Router';

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
            <h1>Hello, world!</h1>
            <YetiBoxRouter />
        </>
    );
}

export default AppComponent
