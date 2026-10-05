import './App.scss'
import { useEffect, useState } from 'react';

function PayloadComponent({ loading, error, data }: { loading: boolean, error: string | null, data: any }): React.JSX.Element {
    if (loading) {
        return <>Loading...</>;
    } else if (error) {
        return <>Error - {error}</>;
    } else {
        return <>{data}</>;
    }
}

function AppComponent(): React.JSX.Element {
    const [data] = useState(null);
    const [error, setError] = useState<string | null>(null);
    const [imageSrc, setImageSrc] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [streaming, setStreaming] = useState(false);
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

    const toggleStream = () => {
        setError(null);
        setStreaming((current) => !current);
        setDate(() => new Date());
    };

    const clickGetFrame = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/capture/frame');
            if (response.status === 204) {
                throw new Error('No frame is currently available.');
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const frameBlob = await response.blob();
            setImageSrc(URL.createObjectURL(frameBlob));
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
            setDate(() => new Date());
        }
    };

    useEffect(() => {
        return () => {
            if (imageSrc) {
                URL.revokeObjectURL(imageSrc);
            }
        };
    }, [imageSrc]);

    return (
        <>
            <button onClick={clickStart} disabled={loading}>
                <label>Start Capture</label>
            </button>
            <button onClick={clickGetFrame} disabled={loading}>
                <label>Get Frame</label>
            </button>
            <button onClick={toggleStream}>
                <label>{streaming ? 'Stop Live Stream' : 'Start Live Stream'}</label>
            </button>

            <h1>Status from Server: <PayloadComponent loading={loading} error={error} data={data} /></h1>
            <span>Last request: {date.toLocaleString()}</span>

            <hr />

            {!!imageSrc && <img src={imageSrc}/>}
            {!!streaming && <img src="http://localhost:8000/capture/stream" />}
        </>
    );
}

export default AppComponent
