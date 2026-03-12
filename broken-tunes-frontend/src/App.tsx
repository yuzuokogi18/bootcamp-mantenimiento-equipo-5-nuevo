import { PlayerProvider } from './context/PlayerContext';
import { LibraryPage }    from './pages/LibraryPage';
import { PlayerBar }      from './components/PlayerBar';
import './index.css';

export default function App() {
  return (
    <PlayerProvider>
      <LibraryPage />
      <PlayerBar />
    </PlayerProvider>
  );
}