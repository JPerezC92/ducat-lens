// Astro dev server runs on port 4321 by default.
// Backend (FastAPI) runs on port 8000.
// Cross-origin fetch from the React island to the backend uses CORS, which is
// already configured in backend/main.py to allow http://localhost:4321.
// No native proxy is needed in this config; the React island fetches
// http://localhost:8000/analyze directly during development.

import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://ducat-lens.example',
  integrations: [react(), sitemap()],
  output: 'static',
});
