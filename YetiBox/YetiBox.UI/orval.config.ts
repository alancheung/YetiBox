import { defineConfig } from 'orval';

export default defineConfig({
  yetibox: {
    input: {
      target: './openapi.json',
    },
    output: {
      mode: 'tags-split',
      target: './src/api/generated/endpoints.ts',
      schemas: './src/api/generated/models',
      client: 'fetch',
    },
  },
});
