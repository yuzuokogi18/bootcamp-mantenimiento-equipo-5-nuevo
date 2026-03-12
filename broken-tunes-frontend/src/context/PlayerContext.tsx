import { createContext, useContext } from 'react';
import type { ReactNode } from 'react';
import { usePlayer } from '../hooks/usePlayer';

type PlayerContextValue = ReturnType<typeof usePlayer>;

const PlayerContext = createContext<PlayerContextValue | null>(null);

export function PlayerProvider({ children }: { children: ReactNode }) {
  const player = usePlayer();
  return (
    <PlayerContext.Provider value={player}>
      {children}
    </PlayerContext.Provider>
  );
}

export function usePlayerContext(): PlayerContextValue {
  const ctx = useContext(PlayerContext);
  if (!ctx) throw new Error('usePlayerContext debe usarse dentro de <PlayerProvider>');
  return ctx;
}