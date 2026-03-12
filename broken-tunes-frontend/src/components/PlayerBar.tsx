import { usePlayerContext } from '../context/PlayerContext';
import { SpeedControl }     from './SpeedControl.tsx';
import styles               from './PlayerBar.module.css';

export function PlayerBar() {
  const { audioRef, currentSong, playbackRate, setSpeed } = usePlayerContext();

  return (
    <footer className={styles.bar} role="region" aria-label="Controles de reproducción">

      {/* Izquierda — info de la canción activa */}
      <div className={styles.left}>
        <div className={styles.art} aria-hidden="true">
          {currentSong?.isBackup ? '⌁' : '♪'}
        </div>
        <div className={styles.trackInfo}>
          <p className={styles.title}>
            {currentSong ? currentSong.title : 'Nada reproduciéndose'}
          </p>
          <p className={styles.artist}>
            {currentSong ? currentSong.artist : '—'}
          </p>
        </div>
      </div>

      {/* Centro — elemento audio nativo */}
      <div className={styles.center}>
        <audio
          ref={audioRef}
          controls
          className={styles.audio}
          aria-label="Reproductor de audio"
        />
      </div>

      {/* Derecha — control de velocidad */}
      <div className={styles.right}>
        <SpeedControl value={playbackRate} onChange={setSpeed} />
      </div>

    </footer>
  );
}