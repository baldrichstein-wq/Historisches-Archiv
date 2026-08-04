import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Gallery from './pages/Gallery';
import Timeline from './pages/Timeline';
import Songs from './pages/Songs';
import SongDetail from './pages/SongDetail';
import Recipes from './pages/Recipes';
import RecipeDetail from './pages/RecipeDetail';
import Admin from './pages/Admin';
import EditItem from './pages/EditItem';
import Links from './pages/Links';
import VerifyEmail from './pages/VerifyEmail';
import Impressum from './pages/Impressum';
import Guestbook from './pages/Guestbook';
import './App.css';

function App() {
  return (
    <Router basename="/archiv">
      <div className="app-container">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/gallery" element={<Gallery />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/songs" element={<Songs />} />
            <Route path="/songs/:id" element={<SongDetail />} />
            <Route path="/recipes" element={<Recipes />} />
            <Route path="/recipes/:id" element={<RecipeDetail />} />
            <Route path="/links" element={<Links />} />
            <Route path="/guestbook" element={<Guestbook />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/verify" element={<VerifyEmail />} />
            <Route path="/admin/edit/:type/:id" element={<EditItem />} />
            <Route path="/admin/new/:type" element={<EditItem />} />
            <Route path="/impressum" element={<Impressum />} />
          </Routes>
        </main>
        
        <footer style={{
          textAlign: 'center', 
          padding: '2rem', 
          marginTop: 'auto', 
          borderTop: '1px solid rgba(255,255,255,0.1)',
          background: 'rgba(0,0,0,0.5)'
        }}>
          <p style={{ color: '#aaa', fontSize: '0.9rem' }}>
            &copy; {new Date().getFullYear()} Historisches Archiv. Alle Rechte vorbehalten. | <Link to="/impressum" style={{ color: 'var(--color-accent-gold)', textDecoration: 'none' }}>Impressum</Link>
          </p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
