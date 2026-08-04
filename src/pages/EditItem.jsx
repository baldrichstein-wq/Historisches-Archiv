import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function EditItem() {
  const { type, id } = useParams();
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const [message, setMessage] = useState('');

  const [formData, setFormData] = useState({});
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    if (!token) {
      navigate('/admin');
      return;
    }

    // Verify role
    fetch('http://localhost:8000/api/users/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(user => {
        const allowedRoles = type === 'link' ? ['admin'] : (id ? ['admin', 'moderator'] : ['admin', 'moderator', 'user']);
        if (!allowedRoles.includes(user.role)) {
          navigate('/admin');
        } else {
          setCurrentUser(user);
          localStorage.setItem('userRole', user.role);
        }
      })
      .catch(err => {
        console.error(err);
        navigate('/admin');
      });

    if (id) {
      let url = '';
      if (type === 'song') url = `http://localhost:8000/api/songs/${id}`;
      else if (type === 'recipe') url = `http://localhost:8000/api/recipes/${id}`;
      else if (type === 'timeline') url = `http://localhost:8000/api/timeline/${id}`;
      else if (type === 'archive') url = `http://localhost:8000/api/archive/${id}`;
      else if (type === 'link') url = `http://localhost:8000/api/links/${id}`;

      if (url) {
        fetch(url)
          .then(res => res.json())
          .then(data => setFormData(data))
          .catch(err => console.error(err));
      }
    } else {
      // Initialize defaults for new items
      if (type === 'archive') setFormData({ item_type: 'Postkarte' });
      else setFormData({});
    }
  }, [id, type, navigate, token]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let url = '';
    if (type === 'song') url = 'http://localhost:8000/api/songs';
    else if (type === 'recipe') url = 'http://localhost:8000/api/recipes';
    else if (type === 'timeline') url = 'http://localhost:8000/api/timeline';
    else if (type === 'archive') url = 'http://localhost:8000/api/archive';
    else if (type === 'link') url = 'http://localhost:8000/api/links';

    if (id) url += `/${id}`;

    const method = id ? 'PUT' : 'POST';

    // Parse numeric fields if needed
    const payload = { ...formData };
    if (payload.year) payload.year = parseInt(payload.year);

    try {
      const res = await fetch(url, {
        method,
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const data = await res.json().catch(() => null);
        if (!id && data && data.approved === false && type !== 'link') {
          alert('Vielen Dank! Dein Eintrag wurde zur Prüfung an die Moderatoren gesendet und wird nach Freigabe veröffentlicht.');
        }
        navigate('/admin');
      } else {
        setMessage('Fehler beim Speichern');
      }
    } catch (err) {
      console.error(err);
      setMessage('Netzwerkfehler');
    }
  };

  const renderFormFields = () => {
    if (type === 'song') {
      return (
        <>
          <div className="form-group"><label>Titel</label><input type="text" name="title" value={formData.title || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Autor / Komponist</label><input type="text" name="author" value={formData.author || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Herkunft</label><input type="text" name="origin" value={formData.origin || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Sprache</label><input type="text" name="language" value={formData.language || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Jahr</label><input type="number" name="year" value={formData.year || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Liedtext</label><textarea name="lyrics" value={formData.lyrics || ''} onChange={handleChange} rows="12"></textarea></div>
          <div className="form-group"><label>Geschichte / Hintergrund</label><textarea name="history" value={formData.history || ''} onChange={handleChange} rows="6"></textarea></div>
          <div className="form-group"><label>Audio-URL</label><input type="url" name="audio_url" value={formData.audio_url || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Noten-URL</label><input type="url" name="sheet_music_url" value={formData.sheet_music_url || ''} onChange={handleChange} /></div>
        </>
      );
    } else if (type === 'recipe') {
      return (
        <>
          <div className="form-group"><label>Titel</label><input type="text" name="title" value={formData.title || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Zutaten</label><textarea name="ingredients" value={formData.ingredients || ''} onChange={handleChange} rows="8"></textarea></div>
          <div className="form-group"><label>Zubereitung</label><textarea name="instructions" value={formData.instructions || ''} onChange={handleChange} rows="12"></textarea></div>
          <div className="form-group"><label>Geschichte / Hintergrund</label><textarea name="history" value={formData.history || ''} onChange={handleChange} rows="6"></textarea></div>
          <div className="form-group"><label>Jahr</label><input type="number" name="year" value={formData.year || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Land / Herkunft</label><input type="text" name="country" value={formData.country || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Bild-URL</label><input type="url" name="image_url" value={formData.image_url || ''} onChange={handleChange} /></div>
        </>
      );
    } else if (type === 'timeline') {
      return (
        <>
          <div className="form-group"><label>Titel</label><input type="text" name="title" value={formData.title || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Datum (YYYY-MM-DD)</label><input type="text" name="event_date" value={formData.event_date ? formData.event_date.split('T')[0] : ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Inhalt</label><textarea name="content" value={formData.content || ''} onChange={handleChange} rows="10" required></textarea></div>
        </>
      );
    } else if (type === 'archive') {
      return (
        <>
          <div className="form-group">
            <label>Kategorie</label>
            <select name="item_type" value={formData.item_type || 'Postkarte'} onChange={handleChange} style={{padding: '0.8rem', background: 'rgba(255,255,255,0.1)', color: 'white', border: '1px solid var(--color-accent-gold)', borderRadius: '4px'}}>
              <option value="Postkarte" style={{color: 'black'}}>Postkarte</option>
              <option value="Dokument" style={{color: 'black'}}>Dokument</option>
              <option value="Zeitschrift" style={{color: 'black'}}>Zeitschrift</option>
              <option value="Vordruck" style={{color: 'black'}}>Vordruck</option>
            </select>
          </div>
          <div className="form-group"><label>Titel</label><input type="text" name="title" value={formData.title || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Bild-URL</label><input type="url" name="image_url" value={formData.image_url || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Jahr</label><input type="number" name="year" value={formData.year || ''} onChange={handleChange} /></div>
          <div className="form-group"><label>Beschreibung</label><textarea name="description" value={formData.description || ''} onChange={handleChange} rows="8"></textarea></div>
        </>
      );
    } else if (type === 'link') {
      return (
        <>
          <div className="form-group"><label>Titel</label><input type="text" name="title" value={formData.title || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>URL</label><input type="url" name="url" value={formData.url || ''} onChange={handleChange} required /></div>
          <div className="form-group"><label>Beschreibung</label><textarea name="description" value={formData.description || ''} onChange={handleChange} rows="8"></textarea></div>
        </>
      );
    }
  };

  if (!currentUser) {
    return <div className="page-container fade-in"><p style={{textAlign: 'center', color: 'gray'}}>Berechtigung wird geprüft...</p></div>;
  }

  return (
    <div className="page-container fade-in">
      <header className="page-header">
        <h1 className="page-title">{id ? 'Eintrag bearbeiten' : 'Neuer Eintrag'}</h1>
        <p className="page-description">
          Typ: {type.toUpperCase()} {id ? `(ID: ${id})` : ''}
        </p>
      </header>

      <div className="glass" style={{maxWidth: '800px', margin: '0 auto', padding: '2rem'}}>
        {message && <div style={{color: 'red', marginBottom: '1rem'}}>{message}</div>}
        
        {id && (
          <div style={{background: 'rgba(0,0,0,0.5)', border: '1px solid var(--color-accent-gold)', borderRadius: '8px', padding: '1.5rem', marginBottom: '2rem'}}>
            <h4 style={{color: 'var(--color-accent-gold)', margin: '0 0 1rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem'}}>
              <span>📄 Gesamter Text des zu bearbeitenden Beitrags</span>
            </h4>
            <div style={{color: '#ddd', fontSize: '0.95rem', whiteSpace: 'pre-wrap', maxHeight: '400px', overflowY: 'auto', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', borderLeft: '3px solid var(--color-accent-gold)'}}>
              {type === 'song' && (
                <>
                  <p style={{margin: '0 0 0.5rem 0'}}><strong>Titel:</strong> {formData.title}</p>
                  {formData.author && <p style={{margin: '0 0 0.5rem 0'}}><strong>Autor / Komponist:</strong> {formData.author}</p>}
                  {formData.lyrics && <p style={{margin: '0 0 0.5rem 0'}}><strong>Liedtext:</strong><br/>{formData.lyrics}</p>}
                  {formData.history && <p style={{margin: '0'}}><strong>Hintergrund:</strong><br/>{formData.history}</p>}
                </>
              )}
              {type === 'recipe' && (
                <>
                  <p style={{margin: '0 0 0.5rem 0'}}><strong>Titel:</strong> {formData.title}</p>
                  {formData.ingredients && <p style={{margin: '0 0 0.5rem 0'}}><strong>Zutaten:</strong><br/>{formData.ingredients}</p>}
                  {formData.instructions && <p style={{margin: '0 0 0.5rem 0'}}><strong>Zubereitung:</strong><br/>{formData.instructions}</p>}
                  {formData.history && <p style={{margin: '0'}}><strong>Hintergrund:</strong><br/>{formData.history}</p>}
                </>
              )}
              {type === 'timeline' && (
                <>
                  <p style={{margin: '0 0 0.5rem 0'}}><strong>Titel:</strong> {formData.title} {formData.event_date && `(${formData.event_date})`}</p>
                  {formData.content && <p style={{margin: '0'}}><strong>Inhalt:</strong><br/>{formData.content}</p>}
                </>
              )}
              {type === 'archive' && (
                <>
                  <p style={{margin: '0 0 0.5rem 0'}}><strong>Titel:</strong> {formData.title} ({formData.item_type || 'Postkarte'})</p>
                  {formData.description && <p style={{margin: '0'}}><strong>Beschreibung:</strong><br/>{formData.description}</p>}
                </>
              )}
              {type === 'link' && (
                <>
                  <p style={{margin: '0 0 0.5rem 0'}}><strong>Titel:</strong> {formData.title} ({formData.url})</p>
                  {formData.description && <p style={{margin: '0'}}><strong>Beschreibung:</strong><br/>{formData.description}</p>}
                </>
              )}
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="admin-form">
          {renderFormFields()}
          
          <div style={{display: 'flex', gap: '1rem', marginTop: '2rem'}}>
            <button type="submit" className="hero-cta">Speichern</button>
            <button type="button" onClick={() => navigate('/admin')} className="hero-cta" style={{borderColor: 'gray', color: 'gray'}}>Abbrechen</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EditItem;
