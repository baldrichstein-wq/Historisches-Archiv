import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Links() {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/links')
      .then(res => res.json())
      .then(data => {
        setLinks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fehler beim Laden der Links:", err);
        setLoading(false);
      });
  }, []);

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canAdd = token && userRole === 'admin';

  return (
    <div className="page-container fade-in">
      <header className="page-header" style={{position: 'relative'}}>
        <h1 className="page-title">Links & Verweise</h1>
        <p className="page-description">Weiterführende Ressourcen, Partnerarchive und historische Quellen im Netz.</p>
        {canAdd && (
          <div style={{marginTop: '1rem'}}>
            <Link to="/admin/new/link" className="hero-cta" style={{padding: '0.5rem 1rem', fontSize: '0.9rem', display: 'inline-block'}}>
              + Neuen Link hinzufügen
            </Link>
          </div>
        )}
      </header>

      {loading ? (
        <p style={{textAlign: 'center'}}>Lade Links...</p>
      ) : links.length === 0 ? (
        <p style={{textAlign: 'center', color: '#ccc'}}>Noch keine Links vorhanden.</p>
      ) : (
        <div className="dashboard-grid">
          {links.map(link => (
            <a 
              key={link.id} 
              href={link.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="dashboard-card glass hover-lift"
              style={{textDecoration: 'none', display: 'block'}}
            >
              <h3 style={{color: 'var(--color-accent-gold)', marginBottom: '0.5rem'}}>{link.title}</h3>
              {link.description && <p style={{color: '#ddd', fontSize: '0.95rem'}}>{link.description}</p>}
              <div style={{marginTop: '1rem', color: '#aaa', fontSize: '0.8rem', wordBreak: 'break-all'}}>
                {link.url}
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

export default Links;
