import { useSongs }   from '../hooks/useSongs';
import { useBackups } from '../hooks/useBackups';
import { SongCard }   from '../components/SongCard';
import { BackupCard } from '../components/BackupCard';
import styles         from './LibraryPage.module.css';

export function LibraryPage() {
  const { songs,   loading: songsLoading,   error: songsError   } = useSongs();
  const { backups, loading: backupsLoading, error: backupsError } = useBackups();

  return (
    <div className={styles.app}>

      <header className={styles.header}>
        <div className={styles.logo}>
          <div className={styles.mark}>BT</div>
          <div>
            <h1 className={styles.title}>BROKEN TUNES</h1>
            <p className={styles.subtitle}>Tu música local — prueba rápida</p>
          </div>
        </div>
      </header>

      <main className={styles.grid}>

        {/* Columna izquierda — Biblioteca */}
        <section className={styles.panel}>
          <div className={styles.panelHeader}>
            <h3 className={styles.panelTitle}>Tu Biblioteca</h3>
            <small className={styles.panelMeta}>
              {!songsLoading && !songsError && `${songs.length} canciones`}
            </small>
          </div>

          <div className={styles.list} role="list" aria-label="Lista de canciones">
            {songsLoading && <p className={styles.state}>Cargando canciones…</p>}

            {songsError && (
              <p className={styles.stateError} role="alert">
                Error: {songsError}
              </p>
            )}

            {!songsLoading && !songsError && songs.length === 0 && (
              <p className={styles.state}>No hay canciones disponibles.</p>
            )}

            {!songsLoading && !songsError && songs.map(song => (
              <SongCard key={song.id} song={song} />
            ))}
          </div>
        </section>

        {/* Columna derecha — Backups */}
        <aside className={styles.rightCol}>
          <div className={styles.panel}>
            <div className={styles.panelHeader}>
              <h3 className={styles.panelTitle}>Backups</h3>
              <small className={styles.panelMeta}>
                {!backupsLoading && !backupsError && `${backups.length} copias`}
              </small>
            </div>

            <div className={styles.list} role="list" aria-label="Lista de backups">
              {backupsLoading && <p className={styles.state}>Cargando backups…</p>}

              {backupsError && (
                <p className={styles.stateError} role="alert">
                  Error: {backupsError}
                </p>
              )}

              {!backupsLoading && !backupsError && backups.length === 0 && (
                <p className={styles.state}>No hay backups aún.</p>
              )}

              {!backupsLoading && !backupsError && backups.map(backup => (
                <BackupCard key={backup.id} backup={backup} />
              ))}
            </div>
          </div>
        </aside>

      </main>
    </div>
  );
}