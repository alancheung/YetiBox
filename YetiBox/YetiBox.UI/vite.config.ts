import { defineConfig } from 'vite';
import plugin from '@vitejs/plugin-react';

const apiProxyTarget = process.env.API_PROXY_TARGET ?? 'http://api:8000';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [plugin()],
    server: {
        host: '0.0.0.0',
        port: 58369,
        proxy: {
            '/capture': {
                target: apiProxyTarget,
            },
            '/decompiler': {
                target: apiProxyTarget,
            },
        },
    }
})
