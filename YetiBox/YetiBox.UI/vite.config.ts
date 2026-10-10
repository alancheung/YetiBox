import { defineConfig } from 'vite';
import plugin from '@vitejs/plugin-react';

/** The location of the API using the env for Docker or checking locally otherwise. */
const apiProxyTarget = process.env.API_PROXY_TARGET ?? 'http://localhost:8000';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [plugin()],
    server: {
        host: '0.0.0.0',
        port: 58369,
        proxy: {
            '/api': {
                target: apiProxyTarget,
            },
        },
    }
})
