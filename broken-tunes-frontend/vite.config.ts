import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api':         'http://localhost:5000',
      '/play':        'http://localhost:5000',
      '/play_backup': 'http://localhost:5000',
    }
  }
})