import os
import base64
import mysql.connector

# --- CARGA DE VARIABLES DE ENTORNO ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # Carga manual si no existe la librería python-dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as envf:
            for line in envf:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'broken_tunes')
}

UPLOAD_DIR = 'uploads'

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def main():
    # 1. Validar directorio
    if not os.path.isdir(UPLOAD_DIR):
        print(f"Error: No existe la carpeta '{UPLOAD_DIR}'. Créala y pon tus mp3 ahí.")
        return
    
    files = os.listdir(UPLOAD_DIR)
    print(f"--- Iniciando carga de {len(files)} archivos ---\n")

    conn = get_db()
    cur = conn.cursor()
    
    for f in files:
        path = os.path.join(UPLOAD_DIR, f)
        if os.path.isdir(path):
            continue
            
        print(f"Procesando: {f}")
        
        try:
            # 1. Leer el archivo
            with open(path, 'rb') as fh:
                file_bytes = fh.read()
            
            # --- CORRECCIÓN CRÍTICA ---
            # No adivines. Usa la extensión para saber cómo tratar los datos.
            
            final_data = None
            
            if f.lower().endswith('.mp3'):
                # Es un MP3 real: Lo guardamos tal cual (Binario puro)
                final_data = file_bytes
                
            elif f.lower().endswith('.b64') or f.lower().endswith('.txt'):
                # Es un texto en Base64: Lo decodificamos a binario
                try:
                    final_data = base64.b64decode(file_bytes)
                except Exception as e:
                    print(f"  > Error decodificando Base64: {e}")
                    continue
            else:
                # Otros archivos: Asumimos binario por defecto
                final_data = file_bytes

            # --------------------------

            # ... (Aquí sigue tu lógica de separación de Artista/Título igual que antes)
            
            clean_name = f.rsplit('.', 1)[0]
            if ' - ' in clean_name:
                parts = clean_name.split(' - ', 1)
                artist_name = parts[0].strip()
                song_title = parts[1].strip()
            else:
                artist_name = "Unknown Artist"
                song_title = clean_name

            # Validar si es backup o canción normal
            is_backup = 'backup' in f.lower()
            
            if is_backup:
                # ... (Lógica de backup simplificada) ...
                cur.execute("INSERT INTO songs_backup (title, artist, mp3_data, backup_note, backed_up_by, backed_up_at) VALUES (%s, %s, %s, 'manual upload', 'script', NOW())", 
                           (f, 'uploader', final_data))
                conn.commit()
                print("  > Guardado en Backups")
            else:
                # 1. Gestionar Artista
                cur.execute("SELECT id FROM artists WHERE name = %s", (artist_name,))
                row = cur.fetchone()
                if row:
                    artist_id = row[0]
                else:
                    cur.execute("INSERT INTO artists (name) VALUES (%s)", (artist_name,))
                    conn.commit()
                    artist_id = cur.lastrowid
                
                # 2. Insertar Canción
                cur.execute("SELECT COUNT(*) FROM songs_data WHERE title = %s AND artist_id = %s", (song_title, artist_id))
                if cur.fetchone()[0] == 0:
                    # Usamos final_data que asegura ser binario limpio
                    cur.execute("INSERT INTO songs_data (title, artist_id, mp3_data) VALUES (%s, %s, %s)", 
                                (song_title, artist_id, final_data))
                    conn.commit()
                    print(f"  > [OK] Subida correcta: {song_title}")
                else:
                    print(f"  > Ya existe: {song_title}")

        except Exception as e:
            print(f"  > Error en {f}: {e}")

    cur.close()
    conn.close()
    print("\n--- Proceso finalizado ---")

if __name__ == '__main__':
    main()