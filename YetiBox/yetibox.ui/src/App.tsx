import './App.scss'
import { useState } from 'react';

function PayloadComponent({ loading, error, data }: { loading:boolean, error: string | null, data: any}): React.JSX.Element {
    if (loading) {
        return <>Loading...</>;
    } else if (error) {
        return <>Error - {error}</>;
    } else {
        return <>{data}</>;
    }
}

function AppComponent(): React.JSX.Element  {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [date, setDate] = useState(() => new Date());

    const clickStart = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/capture/start', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return;
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
            setDate(() => new Date());
        }
    }

    const clickGetFrame = async () => {
        setLoading(true);
        setError(null);
        setData(null);
        try {
            const response = await fetch('http://localhost:8000/capture/frame');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            setData(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
            setDate(() => new Date());
        }
    };

    return (
        <>
            <button onClick={clickStart} disabled={loading}>
                <label>Start Capture</label>
            </button>
            <button onClick={clickGetFrame} disabled={loading}>
                <label>Get Frame</label>
            </button>
            <h1>Payload from Server: <PayloadComponent loading={loading} error={error} data={data} /></h1>
            <span>Last request: {date.toLocaleString()}</span>
        </>
    );
}

export default AppComponent
