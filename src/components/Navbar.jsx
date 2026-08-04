import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();
  
  return (
    <nav className="navbar glass">
      <div className="nav-brand">
        <Link to="/">Historisches Archiv</Link>
      </div>
      <div className="nav-links">
        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
          Startseite
        </Link>
        <Link to="/gallery" className={`nav-link ${location.pathname === '/gallery' ? 'active' : ''}`}>
          Archiv
        </Link>
        <Link to="/timeline" className={`nav-link ${location.pathname === '/timeline' ? 'active' : ''}`}>
          Zeitstrahl
        </Link>
        <Link to="/songs" className={`nav-link ${location.pathname === '/songs' ? 'active' : ''}`}>
          Lieder
        </Link>
        <Link to="/recipes" className={`nav-link ${location.pathname === '/recipes' ? 'active' : ''}`}>
          Rezepte
        </Link>
        <Link to="/links" className={`nav-link ${location.pathname === '/links' ? 'active' : ''}`}>
          Links
        </Link>
        <Link to="/guestbook" className={`nav-link ${location.pathname === '/guestbook' ? 'active' : ''}`}>
          Gästebuch
        </Link>
        <Link to="/admin" className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}>
          REG/Anmeldung
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
