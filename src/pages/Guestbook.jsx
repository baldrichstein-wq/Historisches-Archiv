import { useState, useEffect } from 'react';

function Guestbook() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [submitMsg, setSubmitMsg] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canDelete = token && ['admin', 'moderator'].includes(userRole);

  const fetchEntries = () => {
    fetch('http://localhost:8091/api/guestbook')
      .then(res => res.json())
      .then(data => {
        setEntries(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fehler beim Laden des Gästebuchs:", err);
        setEntries([]);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchEntries();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim() || !message.trim()) {
      setSubmitMsg('Fehler: Bitte fülle alle Pflichtfelder (Name, E-Mail-Adresse und Nachricht) vollständig aus.');
      return;
    }
    if (!email.includes('@') || !email.includes('.')) {
      setSubmitMsg('Fehler: Bitte gib eine gültige E-Mail-Adresse ein.');
      return;
    }

    setSubmitting(true);
    setSubmitMsg('');

    try {
      const token = localStorage.getItem('token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch('http://localhost:8091/api/guestbook', {
        method: 'POST',
        headers,
        body: JSON.stringify({ name, email, message })
      });

      if (res.ok) {
        const newEntry = await res.json();
        setName('');
        setEmail('');
        setMessage('');
        if (newEntry.approved) {
          setSubmitMsg('Dein Eintrag wurde erfolgreich im Gästebuch veröffentlicht!');
        } else {
          setSubmitMsg('Vielen Dank! Dein Eintrag wurde zur Prüfung an die Moderatoren gesendet und wird in Kürze freigegeben.');
        }
        fetchEntries();
        setTimeout(() => setSubmitMsg(''), 7000);
      } else {
        const errorData = await res.json().catch(() => null);
        setSubmitMsg(errorData?.detail || 'Fehler beim Senden des Eintrags.');
      }
    } catch (err) {
      console.error(err);
      setSubmitMsg('Ein Verbindungsfehler ist aufgetreten.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Diesen Gästebucheintrag wirklich löschen?")) return;

    try {
      const res = await fetch(`http://localhost:8091/api/guestbook/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (res.ok) {
        fetchEntries();
      } else {
        alert("Fehler beim Löschen des Eintrags.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const safeEntries = Array.isArray(entries) ? entries : [];
  const filteredEntries = safeEntries.filter(e => 
    (e?.name || '').toLowerCase().includes(search.toLowerCase()) || 
    (e?.message || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page-container fade-in">
      <header className="page-header">
        <h1 className="page-title">Gästebuch</h1>
        <p className="page-description">
          Hinterlasse uns gerne eine Nachricht, ein Feedback oder teile deine Gedanken zu unserem historischen Archiv.
        </p>
      </header>

      <div style={{ maxWidth: '800px', margin: '0 auto 3rem auto' }}>
        <div className="dashboard-card glass" style={{ padding: '2rem' }}>
          <h3 style={{ color: 'var(--color-accent-gold)', marginBottom: '1.5rem', fontSize: '1.4rem' }}>
            Neuen Eintrag verfassen
          </h3>
          
          {submitMsg && (
            <div 
              className="glass" 
              style={{ 
                padding: '1rem', 
                marginBottom: '1.5rem', 
                borderRadius: '8px',
                color: submitMsg.includes('Fehler') ? '#ff6b6b' : 'var(--color-accent-gold)',
                border: `1px solid ${submitMsg.includes('Fehler') ? 'red' : 'var(--color-accent-gold)'}`,
                textAlign: 'center'
              }}
            >
              {submitMsg}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#ccc', fontSize: '0.95rem' }}>
                Dein Name *
              </label>
              <input 
                type="text" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="z. B. Max Mustermann" 
                required 
                style={{ 
                  width: '100%', 
                  padding: '0.8rem 1rem', 
                  borderRadius: '6px', 
                  border: '1px solid rgba(255,255,255,0.2)', 
                  background: 'rgba(0,0,0,0.3)', 
                  color: 'white',
                  fontSize: '1rem'
                }} 
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#ccc', fontSize: '0.95rem' }}>
                Deine E-Mail-Adresse *
              </label>
              <input 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="z. B. max@beispiel.de" 
                required 
                style={{ 
                  width: '100%', 
                  padding: '0.8rem 1rem', 
                  borderRadius: '6px', 
                  border: '1px solid rgba(255,255,255,0.2)', 
                  background: 'rgba(0,0,0,0.3)', 
                  color: 'white',
                  fontSize: '1rem'
                }} 
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#ccc', fontSize: '0.95rem' }}>
                Deine Nachricht *
              </label>
              <textarea 
                value={message} 
                onChange={(e) => setMessage(e.target.value)} 
                placeholder="Schreibe hier deine Nachricht ins Gästebuch..." 
                required 
                rows="4" 
                style={{ 
                  width: '100%', 
                  padding: '0.8rem 1rem', 
                  borderRadius: '6px', 
                  border: '1px solid rgba(255,255,255,0.2)', 
                  background: 'rgba(0,0,0,0.3)', 
                  color: 'white',
                  fontSize: '1rem',
                  resize: 'vertical',
                  fontFamily: 'inherit'
                }} 
              />
            </div>

            <button 
              type="submit" 
              className="hero-cta" 
              disabled={submitting}
              style={{ 
                alignSelf: 'flex-start', 
                padding: '0.8rem 2rem', 
                fontSize: '1rem', 
                cursor: submitting ? 'not-allowed' : 'pointer',
                opacity: submitting ? 0.7 : 1
              }}
            >
              {submitting ? 'Wird gesendet...' : 'Eintrag absenden'}
            </button>
          </form>
        </div>
      </div>

      <div style={{ maxWidth: '800px', margin: '0 auto 2rem auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <h2 style={{ color: 'white', margin: 0, fontSize: '1.6rem' }}>
            Bisherige Einträge ({filteredEntries.length})
          </h2>
          
          <input 
            type="text" 
            value={search} 
            onChange={(e) => setSearch(e.target.value)} 
            placeholder="Einträge durchsuchen..." 
            style={{ 
              padding: '0.6rem 1rem', 
              borderRadius: '20px', 
              border: '1px solid var(--color-accent-gold)', 
              background: 'rgba(0,0,0,0.3)', 
              color: 'white',
              width: '250px',
              fontSize: '0.9rem'
            }} 
          />
        </div>

        {loading ? (
          <p style={{ textAlign: 'center', color: '#aaa', padding: '2rem 0' }}>Lade Gästebuch...</p>
        ) : filteredEntries.length === 0 ? (
          <div className="glass" style={{ padding: '3rem', textAlign: 'center', borderRadius: '12px', color: '#ccc' }}>
            {search ? 'Keine Einträge für diese Suche gefunden.' : 'Noch keine Einträge im Gästebuch. Sei der Erste!'}
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {filteredEntries.map(entry => (
              <div key={entry.id} className="dashboard-card glass hover-lift" style={{ padding: '1.8rem', position: 'relative' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' }}>
                  <div>
                    <h3 style={{ color: 'var(--color-accent-gold)', margin: 0, fontSize: '1.2rem' }}>{entry.name}</h3>
                    {entry.email && (
                      <span style={{ color: '#888', fontSize: '0.85rem', display: 'block', marginTop: '0.2rem' }}>
                        {entry.email}
                      </span>
                    )}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <span style={{ color: '#aaa', fontSize: '0.85rem' }}>{entry.created_at}</span>
                    {canDelete && (
                      <button 
                        onClick={() => handleDelete(entry.id)} 
                        className="delete-btn" 
                        style={{ padding: '0.2rem 0.6rem', fontSize: '0.8rem' }}
                        title="Diesen Eintrag löschen"
                      >
                        Löschen
                      </button>
                    )}
                  </div>
                </div>
                <p style={{ color: '#eee', lineHeight: '1.6', margin: 0, whiteSpace: 'pre-wrap', fontSize: '1.05rem' }}>
                  {entry.message}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Guestbook;
