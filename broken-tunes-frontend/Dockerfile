# =============================================================
# BROKEN TUNES — Frontend Dockerfile
# Sirve el build estático desde dist/ con nginx Alpine
# Requiere haber ejecutado antes: npm run build
# =============================================================

FROM nginx:alpine

# Copiar el build ya generado al directorio de nginx
COPY dist/ /usr/share/nginx/html

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]