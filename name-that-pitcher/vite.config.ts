import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

export default defineConfig({
  // Match Django's STATIC_URL
  base: '/static/',

  root: path.resolve(__dirname, './src'),

  build: {
    // Output target relative to the frontend/src root directory
    outDir: path.resolve(__dirname, './static'),
    emptyOutDir: true,
    manifest: 'manifest.json', // Required by django-vite

    rollupOptions: {
      // Your JavaScript/TypeScript entry point
      input: {
        'index': path.resolve(__dirname, './src/main.tsx'),
        'style': path.resolve(__dirname, './src/styles/styles.css'),
      },
      output: {
        entryFileNames: `ts/[name]-bundle.ts`,
        assetFileNames: `css/[name].css`
      }
    },
  },

  server: {
    // Enable HMR to accept cross-origin requests from Django server
    cors: true,
    strictPort: true,
    port: 5173,
  },

  plugins: [react(), tailwindcss()]
});
