import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],base:'./',build:{copyPublicDir:false,rollupOptions:{input:{index:'index.html',studio:'studio.html'}}}});
