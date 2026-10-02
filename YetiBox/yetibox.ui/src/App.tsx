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

    const getServerData = async () => {
        setLoading(true);
        setError(null);
        setData(null);
        try {
            const response = await fetch('http://localhost:8000/data');

            // Check if the HTTP request was successful (status 200-299)
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
            <button onClick={getServerData} disabled={loading}>
                <label>Click Me!</label>
            </button>
            <h1>Payload from Server: <PayloadComponent loading={loading} error={error} data={data} /></h1>
            <span>Last request: {date.toLocaleString()}</span>
        </>
    );
}

export default AppComponent
