# =============================================================
# BROKEN TUNES — FTP Dockerfile
# Imagen base: garethflowers/ftp-server (vsftpd Alpine)
# Permite subir canciones MP3 al volumen compartido con el backend
# =============================================================

FROM garethflowers/ftp-server

# Variables de entorno con defaults — sobreescribir en docker-compose
ENV FTP_USER=ftpuser \
    FTP_PASS=ftppass

EXPOSE 20 21