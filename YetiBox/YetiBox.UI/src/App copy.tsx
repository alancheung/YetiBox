import './App.scss'
import { useEffect, useLayoutEffect, useRef, useState } from 'react';

type CaptureStatus = {
    Worker: boolean;
};

function PayloadComponent({ loading, error, data }: { loading: boolean, error: string | null, data: CaptureStatus | null }): React.JSX.Element {
    if (loading) {
        return <>Loading...</>;
    } else if (error) {
        return <>Error - {error}</>;
    } else {
        return <>{data ? `Worker is ${data.Worker ? 'running' : 'not running'}` : 'No status available.'}</>;
    }
}

function AppComponent(): React.JSX.Element {
    const [data, setData] = useState<CaptureStatus | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [imageSrc, setImageSrc] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [streaming, setStreaming] = useState(false);
    const [date, setDate] = useState(() => new Date());
    const streamImageRef = useRef<HTMLImageElement>(null);

    useEffect(() => {
        const controller = new AbortController();
        void getStatus(controller.signal);
        return () => controller.abort();
    }, []);

    const clickStart = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('/api/capture/start', {
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
            const response = await fetch('/api/capture/frame');
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

    const getStatus = async (signal?: AbortSignal) => {
            try {
                const response = await fetch('/api/capture/', {
                    method: 'GET',
                    signal,
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const status: CaptureStatus = await response.json();
                setData(status);
            } catch (err: unknown) {
                if (!signal?.aborted) {
                    setError(err instanceof Error ? err.message : String(err));
                }
            } finally {
                if (!signal?.aborted) {
                    setLoading(false);
                    setDate(() => new Date());
                }
            }
        };

    useEffect(() => {
        return () => {
            if (imageSrc) {
                URL.revokeObjectURL(imageSrc);
            }
        };
    }, [imageSrc]);

    useLayoutEffect(() => {
        const image = streamImageRef.current;
        if (!streaming || !image) {
            return;
        }

        image.src = '/api/capture/stream';
        return () => {
            image?.removeAttribute('src');
        };
    }, [streaming]);

    return (
        <>
            <button onClick={() => getStatus()} disabled={loading}>
                <label>Get Status</label>
            </button>
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
            {!!streaming && <img ref={streamImageRef} alt="Live camera feed" />}
        </>
    );
}
