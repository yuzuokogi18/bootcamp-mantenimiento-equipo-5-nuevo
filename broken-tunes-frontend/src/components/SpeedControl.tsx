import styles from './SpeedControl.module.css';

interface SpeedControlProps {
  value:    number;
  onChange: (value: number) => void;
}

export function SpeedControl({ value, onChange }: SpeedControlProps) {
  return (
    <div className={styles.wrapper}>
      <span className={styles.label}>Velocidad</span>
      <input
        className={styles.slider}
        type="range"
        min={0.5}
        max={2.0}
        step={0.1}
        value={value}
        onChange={e => onChange(parseFloat(e.target.value))}
        aria-label="Velocidad de reproducción"
        aria-valuetext={`${value.toFixed(1)}x`}
      />
      <span className={styles.value}>{value.toFixed(1)}x</span>
    </div>
  );
}