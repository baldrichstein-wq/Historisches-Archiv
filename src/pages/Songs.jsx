import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Songs() {
  const [songs, setSongs] = useState([]);
  const [sortBy, setSortBy] = useState('title');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedEras, setSelectedEras] = useState([]);
  const [selectedOrigins, setSelectedOrigins] = useState([]);
  const [selectedLanguages, setSelectedLanguages] = useState([]);

  const availableOrigins = [...new Set(songs.map(s => s.origin).filter(Boolean))].sort();
  const availableLanguages = [...new Set(songs.map(s => s.language).filter(Boolean))].sort();

  const handleEraToggle = (era) => {
    setSelectedEras(prev => 
      prev.includes(era) 
        ? prev.filter(e => e !== era)
        : [...prev, era]
    );
  };

  const handleOriginToggle = (origin) => {
    setSelectedOrigins(prev => 
      prev.includes(origin) 
        ? prev.filter(o => o !== origin)
        : [...prev, origin]
    );
  };

  const handleLanguageToggle = (lang) => {
    setSelectedLanguages(prev => 
      prev.includes(lang) 
        ? prev.filter(l => l !== lang)
        : [...prev, lang]
    );
  };

  useEffect(() => {
    fetch('http://localhost:8091/api/songs')
      .then(res => res.json())
      .then(data => setSongs(data))
      .catch(err => console.error(err));
  }, []);

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canAdd = token && ['admin', 'moderator', 'user'].includes(userRole);

  return (
    <div className="page-container fade-in">
      <header className="page-header" style={{position: 'relative'}}>
        <h1 className="page-title">Lieder & Texte</h1>
        <p className="page-description">Entdecke historische Lieder, Gedichte und ihre Texte.</p>
        {canAdd && (
          <div style={{marginTop: '1rem'}}>
            <Link to="/admin/new/song" className="hero-cta" style={{padding: '0.5rem 1rem', fontSize: '0.9rem', display: 'inline-block'}}>
              + Neues Lied hinzufügen
            </Link>
          </div>
        )}
      </header>

      <div className="glass" style={{maxWidth: '800px', margin: '0 auto 2rem auto', padding: '1.5rem', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
        <input 
          type="text" 
          placeholder="Schlagwortsuche in Titel, Autor, Text oder Hintergrund..." 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{padding: '0.8rem', width: '100%', borderRadius: '6px', border: '1px solid var(--color-border)', background: 'rgba(0,0,0,0.5)', color: '#fff', fontSize: '1rem'}}
        />
        
        <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1, minWidth: '150px'}}>
            <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem'}}>Sortieren:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              style={{padding: '0.5rem', flex: 1, borderRadius: '6px', background: 'rgba(0,0,0,0.5)', color: '#fff', border: '1px solid var(--color-border)'}}
            >
              <option value="title">Titel (A-Z)</option>
              <option value="year_asc">Jahr (Aufsteigend)</option>
              <option value="year_desc">Jahr (Absteigend)</option>
              <option value="origin">Herkunft (A-Z)</option>
              <option value="language">Sprache (A-Z)</option>
            </select>
          </div>
        </div>

        <div style={{marginTop: '1rem'}}>
          <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem', display: 'block', marginBottom: '0.5rem'}}>Epoche:</label>
          <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
            {[
              { id: 'pre1850', label: 'Vor 1850' },
              { id: '1850to1899', label: '1850 - 1899' },
              { id: '1900to1913', label: '1900 - 1913' },
              { id: 'ww1', label: '1914 - 1918' },
              { id: 'post1918', label: 'Nach 1918' }
            ].map(era => (
              <label key={era.id} style={{display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', color: 'var(--color-text-main)', fontSize: '0.9rem'}}>
                <input 
                  type="checkbox" 
                  checked={selectedEras.includes(era.id)}
                  onChange={() => handleEraToggle(era.id)}
                />
                {era.label}
              </label>
            ))}
          </div>
        </div>

        {availableOrigins.length > 0 && (
          <div style={{marginTop: '1rem'}}>
            <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem', display: 'block', marginBottom: '0.5rem'}}>Herkunft:</label>
            <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
              {availableOrigins.map(origin => (
                <label key={origin} style={{display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', color: 'var(--color-text-main)', fontSize: '0.9rem'}}>
                  <input 
                    type="checkbox" 
                    checked={selectedOrigins.includes(origin)}
                    onChange={() => handleOriginToggle(origin)}
                  />
                  {origin}
                </label>
              ))}
            </div>
          </div>
        )}

        {availableLanguages.length > 0 && (
          <div style={{marginTop: '1rem'}}>
            <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem', display: 'block', marginBottom: '0.5rem'}}>Sprache:</label>
            <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
              {availableLanguages.map(lang => (
                <label key={lang} style={{display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', color: 'var(--color-text-main)', fontSize: '0.9rem'}}>
                  <input 
                    type="checkbox" 
                    checked={selectedLanguages.includes(lang)}
                    onChange={() => handleLanguageToggle(lang)}
                  />
                  {lang}
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      <div>
        {songs.length === 0 ? (
          <p style={{textAlign: 'center', color: 'gray'}}>Noch keine Lieder vorhanden.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, margin: '0 auto', maxWidth: '800px' }}>
            {[...songs].filter(song => {
              const searchLower = (searchQuery || '').toLowerCase();
              const matchesSearch = (song.title && song.title.toLowerCase().includes(searchLower)) || 
                                    (song.author && song.author.toLowerCase().includes(searchLower)) ||
                                    (song.lyrics && song.lyrics.toLowerCase().includes(searchLower)) ||
                                    (song.history && song.history.toLowerCase().includes(searchLower));
              
              let matchesEra = true;
              if (selectedEras.length > 0) {
                const y = song.year;
                if (!y) {
                  matchesEra = false;
                } else {
                  matchesEra = selectedEras.some(era => {
                    if (era === 'pre1850') return y < 1850;
                    if (era === '1850to1899') return y >= 1850 && y <= 1899;
                    if (era === '1900to1913') return y >= 1900 && y <= 1913;
                    if (era === 'ww1') return y >= 1914 && y <= 1918;
                    if (era === 'post1918') return y > 1918;
                    return false;
                  });
                }
              }

              let matchesOrigin = true;
              if (selectedOrigins.length > 0) {
                matchesOrigin = selectedOrigins.includes(song.origin);
              }

              let matchesLanguage = true;
              if (selectedLanguages.length > 0) {
                matchesLanguage = selectedLanguages.includes(song.language);
              }

              return matchesSearch && matchesEra && matchesOrigin && matchesLanguage;
            }).sort((a, b) => {
              if (sortBy === 'title') return (a.title || '').localeCompare(b.title || '');
              if (sortBy === 'year_asc') return (a.year || 0) - (b.year || 0);
              if (sortBy === 'year_desc') return (b.year || 0) - (a.year || 0);
              if (sortBy === 'origin') return (a.origin || 'Z').localeCompare(b.origin || 'Z');
              if (sortBy === 'language') return (a.language || 'Z').localeCompare(b.language || 'Z');
              return 0;
            }).map((song) => (
              <li 
                key={song.id} 
                style={{
                  padding: '1rem 0',
                  borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
                }}
              >
                <Link 
                  to={`/songs/${song.id}`} 
                  style={{ display: 'block', textDecoration: 'none', color: 'inherit' }}
                  onMouseEnter={(e) => { e.currentTarget.querySelector('h3').style.color = 'var(--color-accent-hover)' }}
                  onMouseLeave={(e) => { e.currentTarget.querySelector('h3').style.color = 'var(--color-text-main)' }}
                >
                  <h3 style={{ margin: 0, transition: 'color 0.2s', color: 'var(--color-text-main)', fontSize: '1.2rem' }}>
                    {song.title}
                  </h3>
                  <div style={{ display: 'flex', gap: '15px', fontSize: '0.85rem', color: 'var(--color-text-muted)', marginTop: '0.4rem', flexWrap: 'wrap' }}>
                    {song.author && <span>✍️ {song.author}</span>}
                    {song.year && <span className="timeline-date">{song.year}</span>}
                    {song.origin && <span>📍 {song.origin}</span>}
                    {song.language && <span>🗣️ {song.language}</span>}
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Songs;
