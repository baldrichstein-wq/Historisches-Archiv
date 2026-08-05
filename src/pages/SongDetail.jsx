import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function SongDetail() {
  const { id } = useParams();
  const [song, setSong] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Da unsere API noch keinen direkten Endpunkt für eine einzelne ID hat,
    // fetchen wir alle und suchen das Passende (alternativ könnte man den Backend-Endpunkt erweitern).
    fetch('http://localhost:8091/api/songs')
      .then(res => res.json())
      .then(data => {
        const found = data.find(s => s.id.toString() === id);
        setSong(found);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="page-container fade-in">
        <p style={{textAlign: 'center', color: 'gray'}}>Lade Lied...</p>
      </div>
    );
  }

  if (!song) {
    return (
      <div className="page-container fade-in">
        <div style={{textAlign: 'center', marginTop: '2rem'}}>
          <h2 style={{color: 'var(--color-accent-gold)'}}>Lied nicht gefunden</h2>
          <Link to="/songs" className="hero-cta" style={{display: 'inline-block', marginTop: '1rem'}}>Zurück zur Übersicht</Link>
        </div>
      </div>
    );
  }

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canEdit = token && ['admin', 'moderator'].includes(userRole);

  return (
    <div className="page-container fade-in" style={{ maxWidth: '800px', margin: '0 auto', paddingBottom: '4rem' }}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem'}}>
        <Link to="/songs" style={{color: 'var(--color-accent-gold)', textDecoration: 'none'}}>
          &larr; Zurück zur Lieder-Übersicht
        </Link>
        {canEdit && (
          <Link to={`/admin/edit/song/${song.id}`} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.9rem'}}>
            ✏️ Bearbeiten
          </Link>
        )}
      </div>

      <div className="glass" style={{padding: '2rem', borderRadius: '12px'}}>
        <h1 style={{fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--color-text-main)'}}>{song.title}</h1>
        
        <div style={{display: 'flex', gap: '20px', fontSize: '1rem', color: 'var(--color-text-muted)', marginBottom: '2rem', flexWrap: 'wrap'}}>
          {song.author && <span>✍️ {song.author}</span>}
          {song.year && <span className="timeline-date">{song.year}</span>}
          {song.origin && <span>📍 {song.origin}</span>}
          {song.language && <span>🗣️ {song.language}</span>}
        </div>

        {song.lyrics && (
          <div style={{whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '1.05rem', lineHeight: '1.6', background: 'rgba(0,0,0,0.3)', padding: '1.5rem', borderRadius: '8px'}}>
            {song.lyrics}
          </div>
        )}

        {song.history && (
          <div style={{marginTop: '3rem', padding: '1.5rem', background: 'rgba(255, 215, 0, 0.05)', borderRadius: '8px', borderLeft: '4px solid var(--color-accent-gold)'}}>
            <h3 style={{marginBottom: '0.8rem', color: 'var(--color-accent-gold)'}}>Entstehungsgeschichte</h3>
            <p style={{lineHeight: '1.6', color: 'var(--color-text-main)', fontSize: '1.05rem', margin: 0}}>
              {song.history}
            </p>
          </div>
        )}

        {song.sheet_music_url && (
          <div style={{marginTop: '3rem'}}>
            <h3 style={{marginBottom: '1rem'}}>Noten</h3>
            <img src={song.sheet_music_url} alt={`Noten für ${song.title}`} style={{width: '100%', borderRadius: '8px', border: '1px solid var(--color-border)'}} />
          </div>
        )}

        {song.audio_url && (
          <div style={{marginTop: '3rem'}}>
            <h3 style={{marginBottom: '1rem'}}>Audio</h3>
            {song.audio_url.includes('youtube.com') || song.audio_url.includes('youtu.be') ? (
              <a href={song.audio_url} target="_blank" rel="noopener noreferrer" className="hero-cta" style={{display: 'inline-block'}}>
                Auf YouTube anhören
              </a>
            ) : (
              <audio controls src={song.audio_url} style={{width: '100%'}}>
                Dein Browser unterstützt das Audio-Element nicht.
              </audio>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default SongDetail;
