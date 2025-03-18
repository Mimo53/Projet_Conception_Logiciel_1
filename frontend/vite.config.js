import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  // Charger les variables d'environnement depuis le fichier .env
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [react()],
    server: {
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_API_URL,  // Utilisation correcte de la variable d'environnement
          changeOrigin: true,
          secure: false
        }
      }
    }
  }
})
