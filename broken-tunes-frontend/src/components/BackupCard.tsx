import { type Backup, formatBackupDate } from '../models/Backup';
import { usePlayerContext }          from '../context/PlayerContext';
import styles                        from './BackupCard.module.css';

interface BackupCardProps {
  backup: Backup;
}

export function BackupCard({ backup }: BackupCardProps) {
  const { playBackup } = usePlayerContext();

  return (
    <div className={styles.card} role="listitem">
      <div className={styles.art} aria-hidden="true">⌁</div>

      <div className={styles.meta}>
        <p className={styles.title} title={backup.title}>
          <span className={styles.badge}>B{backup.id}</span>
          {backup.title}
        </p>
        <p className={styles.sub}>
          {backup.artist} · {backup.backed_up_by} · {formatBackupDate(backup)}
        </p>
      </div>

      <div className={styles.controls}>
        <button
          className={styles.playBtn}
          onClick={() => playBackup(backup.id, backup.title, backup.artist)}
          aria-label={`Reproducir backup ${backup.title}`}
        >
          Play
        </button>
      </div>
    </div>
  );
}