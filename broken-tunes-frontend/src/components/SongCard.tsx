import { type Song }             from '../models/Song';
import { usePlayerContext } from '../context/PlayerContext';
import { useBackup }        from '../hooks/useBackup';
import styles               from './SongCard.module.css';

interface SongCardProps {
  song: Song;
}

export function SongCard({ song }: SongCardProps) {
  const { play } = usePlayerContext();
  const { createBackup, loading: backupLoading, error: backupError } = useBackup();

  async function handleBackup() {
    const result = await createBackup(song.id);
    if (result) alert(`Backup creado: #${result.backup_id}`);
  }

  return (
    <div className={styles.card} role="listitem">
      <div className={styles.art} aria-hidden="true">♪</div>

      <div className={styles.meta}>
        <p className={styles.title}  title={song.title}>{song.title}</p>
        <p className={styles.artist} title={song.artist}>{song.artist}</p>
      </div>

      <div className={styles.controls}>
        <button
          className={styles.playBtn}
          onClick={() => play(song.id, song.title, song.artist)}
          aria-label={`Reproducir ${song.title}`}
        >
          Play
        </button>
        <button
          className={`${styles.backupBtn} ${backupLoading ? styles.disabled : ''}`}
          onClick={handleBackup}
          disabled={backupLoading}
          aria-label={`Hacer backup de ${song.title}`}
        >
          {backupLoading ? '...' : 'Backup'}
        </button>
      </div>

      {backupError && (
        <p className={styles.error} role="alert">{backupError}</p>
      )}
    </div>
  );
}