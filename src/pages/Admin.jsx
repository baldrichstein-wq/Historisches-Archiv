import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

function Admin() {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [loginError, setLoginError] = useState('');

  // Data lists
  const [postcards, setPostcards] = useState([]);
  const [events, setEvents] = useState([]);
  const [users, setUsers] = useState([]);
  const [songs, setSongs] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [links, setLinks] = useState([]);
  const [blockedEmails, setBlockedEmails] = useState([]);
  const [blockedIps, setBlockedIps] = useState([]);
  const [pendingItems, setPendingItems] = useState({ guestbook: [], archive: [], timeline: [], songs: [], recipes: [] });

  // CAPTCHA State
  const [captchaNum1, setCaptchaNum1] = useState(0);
  const [captchaNum2, setCaptchaNum2] = useState(0);
  const [captchaAnswer, setCaptchaAnswer] = useState('');

  // Auth/Role states
  const [currentUser, setCurrentUser] = useState(null);

  const [message, setMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('default');
  const [selectedSections, setSelectedSections] = useState(['pending', 'users', 'archive', 'timeline', 'songs', 'recipes', 'links']);

  const fetchData = useCallback(async () => {
    try {
      const pcRes = await fetch('http://localhost:8091/api/archive');
      if(pcRes.ok) setPostcards(await pcRes.json());
      const evRes = await fetch('http://localhost:8091/api/timeline');
      if(evRes.ok) setEvents(await evRes.json());
      const songRes = await fetch('http://localhost:8091/api/songs');
      if(songRes.ok) setSongs(await songRes.json());
      const recRes = await fetch('http://localhost:8091/api/recipes');
      if(recRes.ok) setRecipes(await recRes.json());
      const linkRes = await fetch('http://localhost:8091/api/links');
      if(linkRes.ok) setLinks(await linkRes.json());
    } catch (err) {
      console.error("Fehler beim Laden der Daten:", err);
    }
  }, []);

  const fetchUsers = useCallback(async () => {
    try {
      const res = await fetch('http://localhost:8091/api/users', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setUsers(await res.json());
      }
      const role = localStorage.getItem('userRole');
      if (role === 'admin') {
        const blockRes = await fetch('http://localhost:8091/api/blocked-emails', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (blockRes.ok) {
          setBlockedEmails(await blockRes.json());
        }
        const ipRes = await fetch('http://localhost:8091/api/blocked-ips', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (ipRes.ok) {
          setBlockedIps(await ipRes.json());
        }
      }
    } catch (err) {
      console.error(err);
    }
  }, [token]);

  const fetchPending = useCallback(async () => {
    if (!token) return;
    try {
      const res = await fetch('http://localhost:8091/api/admin/pending', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setPendingItems(data);
      }
    } catch (err) {
      console.error("Fehler beim Laden der Warteschlange:", err);
    }
  }, [token]);

  const fetchCurrentUser = useCallback(async () => {
    try {
      const res = await fetch('http://localhost:8091/api/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const user = await res.json();
        setCurrentUser(user);
        localStorage.setItem('userRole', user.role);
        if (user.role === 'admin' || user.role === 'moderator') {
          fetchUsers();
          fetchPending();
        }
      }
    } catch (err) {
      console.error(err);
    }
  }, [token, fetchUsers, fetchPending]);



  const updateUserRole = async (userId, newRole) => {
    try {
      const res = await fetch(`http://localhost:8091/api/users/${userId}/role`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ role: newRole })
      });
      if (res.ok) {
        setMessage('Rolle erfolgreich aktualisiert');
        fetchUsers();
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Aktualisieren der Rolle');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const deleteUser = async (userId) => {
    if (!window.confirm('Möchtest du diesen User wirklich löschen? Seine Einträge bleiben erhalten.')) return;
    try {
      const res = await fetch(`http://localhost:8091/api/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setMessage('User erfolgreich gelöscht.');
        fetchUsers();
        setTimeout(() => setMessage(''), 3000);
      } else {
        const errorData = await res.json();
        setMessage(errorData.detail || 'Fehler beim Löschen des Users');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleBlockEmail = async (e) => {
    e.preventDefault();
    const emailToBlock = e.target.elements.emailToBlock.value;
    try {
      const res = await fetch('http://localhost:8091/api/blocked-emails', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ email: emailToBlock })
      });
      if (res.ok) {
        e.target.reset();
        const blockRes = await fetch('http://localhost:8091/api/blocked-emails', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (blockRes.ok) setBlockedEmails(await blockRes.json());
      } else {
        const errData = await res.json();
        alert(errData.detail);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const unblockEmail = async (id) => {
    if(!window.confirm('Blockierung aufheben?')) return;
    try {
      const res = await fetch(`http://localhost:8091/api/blocked-emails/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setBlockedEmails(prev => prev.filter(b => b.id !== id));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleBlockIp = async (e) => {
    e.preventDefault();
    const ipToBlock = e.target.elements.ipToBlock.value;
    try {
      const res = await fetch('http://localhost:8091/api/blocked-ips', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ ip_address: ipToBlock })
      });
      if (res.ok) {
        e.target.reset();
        const blockRes = await fetch('http://localhost:8091/api/blocked-ips', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (blockRes.ok) setBlockedIps(await blockRes.json());
      } else {
        const errData = await res.json();
        alert(errData.detail);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const blockUserIp = async (ipAddress) => {
    if (!ipAddress || ipAddress === 'Unbekannt') return alert("Keine gültige IP-Adresse vorhanden.");
    try {
      const res = await fetch('http://localhost:8091/api/blocked-ips', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ ip_address: ipAddress })
      });
      if (res.ok) {
        alert(`IP ${ipAddress} wurde blockiert.`);
        const blockRes = await fetch('http://localhost:8091/api/blocked-ips', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (blockRes.ok) setBlockedIps(await blockRes.json());
      } else {
        const errData = await res.json();
        alert(errData.detail || "Fehler beim Blockieren der IP.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const unblockIp = async (id) => {
    if(!window.confirm('IP-Blockierung aufheben?')) return;
    try {
      const res = await fetch(`http://localhost:8091/api/blocked-ips/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setBlockedIps(prev => prev.filter(b => b.id !== id));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleApprove = async (category, id) => {
    if (!token) return;
    try {
      const res = await fetch(`http://localhost:8091/api/admin/approve/${category}/${id}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setMessage('Eintrag erfolgreich freigegeben!');
        fetchPending();
        fetchData();
        setTimeout(() => setMessage(''), 3000);
      } else {
        const errData = await res.json();
        alert(`Fehler: ${errData.detail || 'Konnte nicht freigeben'}`);
      }
    } catch (err) {
      console.error(err);
      alert('Fehler bei der Verbindung zum Server.');
    }
  };

  const handleReject = async (category, id) => {
    if (!token) return;
    if (!window.confirm('Möchtest du diesen Eintrag wirklich ablehnen und löschen?')) return;
    try {
      const res = await fetch(`http://localhost:8091/api/admin/reject/${category}/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setMessage('Eintrag abgelehnt und gelöscht.');
        fetchPending();
        setTimeout(() => setMessage(''), 3000);
      } else {
        const errData = await res.json();
        alert(`Fehler: ${errData.detail || 'Konnte nicht löschen'}`);
      }
    } catch (err) {
      console.error(err);
      alert('Fehler bei der Verbindung zum Server.');
    }
  };

  useEffect(() => {
    if (token) {
      fetchData();
      fetchCurrentUser();
    }
  }, [token, fetchData, fetchCurrentUser]);

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:8091/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      });
      if (response.ok) {
        const data = await response.json();
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        setLoginError('');
      } else {
        const errorData = await response.json();
        setLoginError(errorData.detail || 'Falscher Benutzername oder Passwort');
      }
    } catch (err) {
      setLoginError('Netzwerkfehler');
    }
  };

  const generateCaptcha = () => {
    setCaptchaNum1(Math.floor(Math.random() * 10) + 1);
    setCaptchaNum2(Math.floor(Math.random() * 10) + 1);
    setCaptchaAnswer('');
  };

  useEffect(() => {
    if (isRegistering) generateCaptcha();
  }, [isRegistering]);

  const handleRegister = async (e) => {
    e.preventDefault();
    if (parseInt(captchaAnswer) !== (captchaNum1 + captchaNum2)) {
      setLoginError('Sicherheitsüberprüfung (Matheaufgabe) ist falsch.');
      generateCaptcha();
      return;
    }

    try {
      const response = await fetch('http://localhost:8091/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          username, 
          email, 
          password,
          captcha_answer: parseInt(captchaAnswer),
          captcha_expected: captchaNum1 + captchaNum2
        })
      });
      if (response.ok) {
        setLoginError('Registrierung erfolgreich! Bitte prüfe deine E-Mails, um deinen Account zu bestätigen.');
        setIsRegistering(false);
      } else {
        const errorData = await response.json();
        setLoginError(errorData.detail || 'Registrierung fehlgeschlagen');
        generateCaptcha();
      }
    } catch (err) {
      setLoginError('Netzwerkfehler');
      generateCaptcha();
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    setCurrentUser(null);
    setUsers([]);
  };



  const deletePostcard = async (id) => {
    if (!window.confirm("Bist du sicher, dass du diesen Archiv-Eintrag löschen möchtest?")) return;
    try {
      const response = await fetch(`http://localhost:8091/api/archive/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setMessage("Archiv-Eintrag gelöscht.");
        fetchData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };



  const deleteEvent = async (id) => {
    if (!window.confirm("Bist du sicher, dass du dieses Ereignis löschen möchtest?")) return;
    try {
      const response = await fetch(`http://localhost:8091/api/timeline/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setMessage("Ereignis gelöscht.");
        fetchData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const deleteSong = async (id) => {
    if(!window.confirm('Wirklich löschen?')) return;
    try {
      const response = await fetch(`http://localhost:8091/api/songs/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setMessage("Lied gelöscht.");
        fetchData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const deleteRecipe = async (id) => {
    if(!window.confirm('Wirklich löschen?')) return;
    try {
      const response = await fetch(`http://localhost:8091/api/recipes/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setMessage("Rezept gelöscht.");
        fetchData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const deleteLink = async (id) => {
    if(!window.confirm('Wirklich löschen?')) return;
    try {
      const response = await fetch(`http://localhost:8091/api/links/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setMessage("Link gelöscht.");
        fetchData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const editItem = (type, id) => {
    navigate(`/admin/edit/${type}/${id}`);
  };

  const newItem = (type) => {
    navigate(`/admin/new/${type}`);
  };

  if (!token) {
    return (
      <div className="admin-container">
        <div className="login-card glass">
          <h2 className="page-title">{isRegistering ? 'Registrieren' : 'Admin Login'}</h2>
          {loginError && <p className="error-msg">{loginError}</p>}
          <form onSubmit={isRegistering ? handleRegister : handleLogin} className="admin-form">
            <div className="form-group">
              <label>Benutzername</label>
              <input type="text" value={username} onChange={e => setUsername(e.target.value)} required />
            </div>
            {isRegistering && (
              <div className="form-group">
                <label>E-Mail</label>
                <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
              </div>
            )}
            <div className="form-group">
              <label>Passwort</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
            </div>
            {isRegistering && (
              <div className="form-group" style={{marginTop: '1rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px'}}>
                <label>Sicherheitsüberprüfung (Spamschutz)</label>
                <p style={{marginBottom: '0.5rem', color: '#ccc'}}>Was ist {captchaNum1} + {captchaNum2}?</p>
                <input 
                  type="number" 
                  value={captchaAnswer} 
                  onChange={e => setCaptchaAnswer(e.target.value)} 
                  required 
                  placeholder="Ergebnis eingeben"
                />
              </div>
            )}
            <button type="submit" className="hero-cta" style={{marginTop: '1rem'}}>
              {isRegistering ? 'Account erstellen' : 'Einloggen'}
            </button>
            <p style={{marginTop: '1rem', textAlign: 'center'}}>
              {isRegistering ? 'Bereits einen Account?' : 'Noch keinen Account?'}{' '}
              <span 
                style={{color: 'var(--color-accent-gold)', cursor: 'pointer', textDecoration: 'underline'}} 
                onClick={() => { setIsRegistering(!isRegistering); setLoginError(''); }}
              >
                {isRegistering ? 'Hier einloggen' : 'Hier registrieren'}
              </span>
            </p>
          </form>
        </div>
      </div>
    );
  }

  if (currentUser && !['admin', 'moderator', 'user'].includes(currentUser.role)) {
    return (
      <div className="admin-dashboard" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div className="dashboard-card glass" style={{padding: '3rem', textAlign: 'center', maxWidth: '500px'}}>
          <h2 style={{color: 'var(--color-accent-gold)', marginBottom: '1rem'}}>Zugriff verweigert</h2>
          <p style={{marginBottom: '2rem'}}>Du benötigst mindestens Benutzer-Rechte, um diesen Bereich zu sehen.</p>
          <button onClick={handleLogout} className="hero-cta">Abmelden</button>
        </div>
      </div>
    );
  }

  const handleSectionToggle = (secId) => {
    if (selectedSections.includes(secId)) {
      if (selectedSections.length === 1) return;
      setSelectedSections(selectedSections.filter(id => id !== secId));
    } else {
      setSelectedSections([...selectedSections, secId]);
    }
  };

  const matchesDashboardSearch = (item, q) => {
    if (!q) return true;
    const lower = q.toLowerCase();
    const str = [
      item.title,
      item.name,
      item.username,
      item.email,
      item.item_type,
      item.description,
      item.content,
      item.message,
      item.author,
      item.origin,
      item.language,
      item.lyrics,
      item.ingredients,
      item.instructions,
      item.history,
      item.url,
      item.role,
      item.ip_address,
      item.year ? String(item.year) : '',
      item.event_date ? String(item.event_date) : ''
    ].filter(Boolean).join(' ').toLowerCase();
    return str.includes(lower);
  };

  const sortDashboardItems = (list, sortBy) => {
    if (!list) return [];
    const sorted = [...list];
    if (sortBy === 'title') {
      sorted.sort((a, b) => (a.title || a.name || a.username || '').localeCompare(b.title || b.name || b.username || ''));
    } else if (sortBy === 'year_asc') {
      sorted.sort((a, b) => (a.year || a.id || 0) - (b.year || b.id || 0));
    } else if (sortBy === 'year_desc') {
      sorted.sort((a, b) => (b.year || b.id || 0) - (a.year || a.id || 0));
    }
    return sorted;
  };

  const filteredUsers = sortDashboardItems(users.filter(u => matchesDashboardSearch(u, searchQuery)), sortBy);
  const filteredPostcards = sortDashboardItems(postcards.filter(pc => matchesDashboardSearch(pc, searchQuery)), sortBy);
  const filteredEvents = sortDashboardItems(events.filter(ev => matchesDashboardSearch(ev, searchQuery)), sortBy);
  const filteredSongs = sortDashboardItems(songs.filter(s => matchesDashboardSearch(s, searchQuery)), sortBy);
  const filteredRecipes = sortDashboardItems(recipes.filter(r => matchesDashboardSearch(r, searchQuery)), sortBy);
  const filteredLinks = sortDashboardItems(links.filter(l => matchesDashboardSearch(l, searchQuery)), sortBy);

  const filteredPending = {
    guestbook: sortDashboardItems((pendingItems.guestbook || []).filter(item => matchesDashboardSearch(item, searchQuery)), sortBy),
    archive: sortDashboardItems((pendingItems.archive || []).filter(item => matchesDashboardSearch(item, searchQuery)), sortBy),
    timeline: sortDashboardItems((pendingItems.timeline || []).filter(item => matchesDashboardSearch(item, searchQuery)), sortBy),
    songs: sortDashboardItems((pendingItems.songs || []).filter(item => matchesDashboardSearch(item, searchQuery)), sortBy),
    recipes: sortDashboardItems((pendingItems.recipes || []).filter(item => matchesDashboardSearch(item, searchQuery)), sortBy)
  };

  const totalPendingCount = 
    (filteredPending.guestbook?.length || 0) + 
    (filteredPending.archive?.length || 0) + 
    (filteredPending.timeline?.length || 0) + 
    (filteredPending.songs?.length || 0) + 
    (filteredPending.recipes?.length || 0);

  return (
    <div className="admin-dashboard">
      <header className="page-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div>
          <div style={{display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem', flexWrap: 'wrap'}}>
            <h1 className="page-title" style={{margin: 0}}>Dashboard</h1>
            <span style={{background: 'rgba(255, 215, 0, 0.2)', color: 'var(--color-accent-gold)', padding: '0.3rem 0.8rem', borderRadius: '12px', fontSize: '0.9rem', fontWeight: 'bold', border: '1px solid var(--color-accent-gold)'}}>
              Rolle: {currentUser?.role === 'admin' ? 'Administrator' : currentUser?.role === 'moderator' ? 'Moderator' : 'Benutzer'}
            </span>
            {['admin', 'moderator'].includes(currentUser?.role) && currentUser?.ip_address && (
              <span style={{background: 'rgba(255, 255, 255, 0.1)', color: '#ccc', padding: '0.3rem 0.8rem', borderRadius: '12px', fontSize: '0.85rem', border: '1px solid rgba(255,255,255,0.2)'}}>
                Deine IP: {currentUser.ip_address}
              </span>
            )}
          </div>
          <p className="page-description" style={{margin: 0}}>Inhalte pflegen, bearbeiten und entfernen.</p>
        </div>
        <button onClick={handleLogout} className="hero-cta" style={{padding: '0.5rem 1rem', fontSize: '0.9rem'}}>Logout</button>
      </header>

      {message && <div className="success-msg glass" style={{marginBottom: '2rem', padding: '1rem', color: 'var(--color-accent-gold)', textAlign: 'center'}}>{message}</div>}

      <div className="glass" style={{maxWidth: '900px', margin: '0 auto 2rem auto', padding: '1.5rem', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
        <input 
          type="text" 
          placeholder="Schlagwortsuche im Dashboard (Einträge, Nutzer, Titel, Inhalte, E-Mails)..." 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{padding: '0.8rem', width: '100%', borderRadius: '6px', border: '1px solid var(--color-border)', background: 'rgba(0,0,0,0.5)', color: '#fff', fontSize: '1rem'}}
        />
        
        <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1, minWidth: '200px'}}>
            <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem'}}>Sortieren:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              style={{padding: '0.5rem', flex: 1, borderRadius: '6px', background: 'rgba(0,0,0,0.5)', color: '#fff', border: '1px solid var(--color-border)'}}
            >
              <option value="default">Standard / Neueste zuerst</option>
              <option value="title">Titel / Name (A-Z)</option>
              <option value="year_asc">Jahr (Aufsteigend)</option>
              <option value="year_desc">Jahr (Absteigend)</option>
            </select>
          </div>
        </div>

        <div style={{marginTop: '0.5rem'}}>
          <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem', display: 'block', marginBottom: '0.5rem'}}>Bereiche anzeigen & filtern:</label>
          <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
            {[
              { id: 'pending', label: '🛡️ Freigaben' },
              { id: 'users', label: '👥 Benutzer' },
              { id: 'archive', label: '🏛️ Archiv' },
              { id: 'timeline', label: '⏳ Timeline' },
              { id: 'songs', label: '🎵 Lieder' },
              { id: 'recipes', label: '📜 Rezepte' },
              { id: 'links', label: '🔗 Links' }
            ].map(sec => (
              <label key={sec.id} style={{display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', color: 'var(--color-text-main)', fontSize: '0.9rem'}}>
                <input 
                  type="checkbox" 
                  checked={selectedSections.includes(sec.id)}
                  onChange={() => handleSectionToggle(sec.id)}
                />
                {sec.label}
              </label>
            ))}
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        {['admin', 'moderator'].includes(currentUser?.role) && selectedSections.includes('pending') && (
          <div className="dashboard-card glass" style={{padding: '2rem', gridColumn: '1 / -1', border: totalPendingCount > 0 ? '2px solid var(--color-accent-gold)' : '1px solid rgba(255,255,255,0.1)', background: totalPendingCount > 0 ? 'rgba(255, 215, 0, 0.05)' : 'rgba(0,0,0,0.3)'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem'}}>
              <h3 style={{margin: 0, color: 'var(--color-accent-gold)', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                <span>🛡️ Freigaben (Warteschlange)</span>
                {totalPendingCount > 0 && (
                  <span style={{background: '#e53935', color: 'white', padding: '0.2rem 0.6rem', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 'bold'}}>
                    {totalPendingCount} {searchQuery ? 'Treffer' : 'neu'}
                  </span>
                )}
              </h3>
              <span style={{fontSize: '0.9rem', color: '#ccc'}}>Einträge warten auf Bestätigung</span>
            </div>

            {totalPendingCount === 0 ? (
              <p style={{color: '#aaa', fontStyle: 'italic', margin: 0}}>{searchQuery ? 'Keine ausstehenden Freigaben für diese Suche.' : 'Keine ausstehenden Freigaben. Alle Inhalte sind geprüft!'}</p>
            ) : (
              <div style={{display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
                {filteredPending.guestbook?.length > 0 && (
                  <div>
                    <h4 style={{color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.4rem', marginBottom: '0.8rem'}}>
                      📖 Gästebuch ({filteredPending.guestbook.length})
                    </h4>
                    <ul className="admin-list" style={{margin: 0}}>
                      {filteredPending.guestbook.map(item => (
                        <li key={item.id} className="admin-list-item" style={{background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '8px', marginBottom: '0.5rem'}}>
                          <div>
                            <strong style={{color: 'var(--color-accent-gold)'}}>{item.name}</strong> <small style={{color: '#aaa'}}>({item.email}) - {item.created_at}</small>
                            <p style={{margin: '0.4rem 0 0', color: '#eee', fontSize: '0.95rem', whiteSpace: 'pre-wrap'}}>{item.message}</p>
                          </div>
                          <div className="admin-actions" style={{gap: '0.5rem'}}>
                            <button onClick={() => handleApprove('guestbook', item.id)} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', background: '#2e7d32', borderColor: '#4caf50'}}>✔ Freigeben</button>
                            <button onClick={() => handleReject('guestbook', item.id)} className="delete-btn" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem'}}>✖ Ablehnen</button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {filteredPending.archive?.length > 0 && (
                  <div>
                    <h4 style={{color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.4rem', marginBottom: '0.8rem'}}>
                      🖼️ Archiv / Postkarten ({filteredPending.archive.length})
                    </h4>
                    <ul className="admin-list" style={{margin: 0}}>
                      {filteredPending.archive.map(item => (
                        <li key={item.id} className="admin-list-item" style={{background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '8px', marginBottom: '0.5rem'}}>
                          <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                            {item.image_url && <img src={item.image_url.startsWith('http') || item.image_url.startsWith('/') ? item.image_url : `http://localhost:8091/${item.image_url}`} alt={item.title} style={{width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px'}} />}
                            <div>
                              <strong style={{color: 'var(--color-accent-gold)'}}>{item.title}</strong> {item.year && <small style={{color: '#aaa'}}>({item.year})</small>}
                              {item.description && <p style={{margin: '0.2rem 0 0', color: '#ccc', fontSize: '0.9rem'}}>{item.description}</p>}
                            </div>
                          </div>
                          <div className="admin-actions" style={{gap: '0.5rem'}}>
                            <button onClick={() => handleApprove('archive', item.id)} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', background: '#2e7d32', borderColor: '#4caf50'}}>✔ Freigeben</button>
                            <button onClick={() => handleReject('archive', item.id)} className="delete-btn" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem'}}>✖ Ablehnen</button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {filteredPending.timeline?.length > 0 && (
                  <div>
                    <h4 style={{color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.4rem', marginBottom: '0.8rem'}}>
                      ⏳ Zeitstrahl Ereignisse ({filteredPending.timeline.length})
                    </h4>
                    <ul className="admin-list" style={{margin: 0}}>
                      {filteredPending.timeline.map(item => (
                        <li key={item.id} className="admin-list-item" style={{background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '8px', marginBottom: '0.5rem'}}>
                          <div>
                            <strong style={{color: 'var(--color-accent-gold)'}}>{item.title}</strong> <small style={{color: '#aaa'}}>({item.event_date})</small>
                            <p style={{margin: '0.2rem 0 0', color: '#ccc', fontSize: '0.9rem'}}>{item.content}</p>
                          </div>
                          <div className="admin-actions" style={{gap: '0.5rem'}}>
                            <button onClick={() => handleApprove('timeline', item.id)} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', background: '#2e7d32', borderColor: '#4caf50'}}>✔ Freigeben</button>
                            <button onClick={() => handleReject('timeline', item.id)} className="delete-btn" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem'}}>✖ Ablehnen</button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {filteredPending.songs?.length > 0 && (
                  <div>
                    <h4 style={{color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.4rem', marginBottom: '0.8rem'}}>
                      🎵 Historische Lieder ({filteredPending.songs.length})
                    </h4>
                    <ul className="admin-list" style={{margin: 0}}>
                      {filteredPending.songs.map(item => (
                        <li key={item.id} className="admin-list-item" style={{background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '8px', marginBottom: '0.5rem'}}>
                          <div>
                            <strong style={{color: 'var(--color-accent-gold)'}}>{item.title}</strong> {item.year && <small style={{color: '#aaa'}}>({item.year})</small>}
                            {item.history && <p style={{margin: '0.2rem 0 0', color: '#ccc', fontSize: '0.9rem'}}>{item.history}</p>}
                          </div>
                          <div className="admin-actions" style={{gap: '0.5rem'}}>
                            <button onClick={() => handleApprove('songs', item.id)} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', background: '#2e7d32', borderColor: '#4caf50'}}>✔ Freigeben</button>
                            <button onClick={() => handleReject('songs', item.id)} className="delete-btn" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem'}}>✖ Ablehnen</button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {filteredPending.recipes?.length > 0 && (
                  <div>
                    <h4 style={{color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.4rem', marginBottom: '0.8rem'}}>
                      🍲 Historische Rezepte ({filteredPending.recipes.length})
                    </h4>
                    <ul className="admin-list" style={{margin: 0}}>
                      {filteredPending.recipes.map(item => (
                        <li key={item.id} className="admin-list-item" style={{background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '8px', marginBottom: '0.5rem'}}>
                          <div>
                            <strong style={{color: 'var(--color-accent-gold)'}}>{item.title}</strong> {item.year && <small style={{color: '#aaa'}}>({item.year})</small>}
                            {item.ingredients && <p style={{margin: '0.2rem 0 0', color: '#ccc', fontSize: '0.9rem'}}>Zutaten: {item.ingredients.substring(0, 100)}...</p>}
                          </div>
                          <div className="admin-actions" style={{gap: '0.5rem'}}>
                            <button onClick={() => handleApprove('recipes', item.id)} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', background: '#2e7d32', borderColor: '#4caf50'}}>✔ Freigeben</button>
                            <button onClick={() => handleReject('recipes', item.id)} className="delete-btn" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem'}}>✖ Ablehnen</button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {['admin', 'moderator'].includes(currentUser?.role) && selectedSections.includes('users') && (
          <div className="dashboard-card glass" style={{padding: '2rem', gridColumn: '1 / -1'}}>
            <h3 style={{marginBottom: '1.5rem', color: 'var(--color-accent-gold)'}}>Benutzerverwaltung ({filteredUsers.length})</h3>
            <div style={{overflowX: 'auto'}}>
              <table style={{width: '100%', textAlign: 'left', borderCollapse: 'collapse'}}>
                <thead>
                  <tr style={{borderBottom: '1px solid rgba(255,255,255,0.2)'}}>
                    <th style={{padding: '0.5rem'}}>ID</th>
                    <th style={{padding: '0.5rem'}}>Benutzername</th>
                    <th style={{padding: '0.5rem'}}>E-Mail</th>
                    <th style={{padding: '0.5rem'}}>IP-Adresse</th>
                    <th style={{padding: '0.5rem'}}>Rolle</th>
                    <th style={{padding: '0.5rem'}}>Aktionen</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map(u => (
                    <tr key={u.id} style={{borderBottom: '1px solid rgba(255,255,255,0.1)'}}>
                      <td style={{padding: '0.5rem'}}>{u.id}</td>
                      <td style={{padding: '0.5rem'}}>{u.username}</td>
                      <td style={{padding: '0.5rem'}}>{u.email}</td>
                      <td style={{padding: '0.5rem', fontFamily: 'monospace', color: '#ffd700'}}>{u.ip_address || 'Unbekannt'}</td>
                      <td style={{padding: '0.5rem'}}>
                        {currentUser?.role === 'admin' || (currentUser?.role === 'moderator' && !['admin', 'moderator'].includes(u.role)) ? (
                          <select 
                            value={u.role} 
                            onChange={(e) => updateUserRole(u.id, e.target.value)}
                            style={{
                              padding: '0.3rem', 
                              background: 'rgba(255,255,255,0.1)', 
                              color: 'white', 
                              border: '1px solid var(--color-accent-gold)',
                              borderRadius: '4px'
                            }}
                          >
                            {currentUser?.role === 'admin' && <option value="admin" style={{color: 'black'}}>Admin</option>}
                            {currentUser?.role === 'admin' && <option value="moderator" style={{color: 'black'}}>Moderator</option>}
                            <option value="user" style={{color: 'black'}}>Benutzer</option>
                            <option value="guest" style={{color: 'black'}}>Gast</option>
                          </select>
                        ) : (
                          <span style={{color: 'white', textTransform: 'capitalize'}}>{u.role}</span>
                        )}
                      </td>
                      <td style={{padding: '0.5rem', textAlign: 'center', display: 'flex', gap: '0.5rem', justifyContent: 'center', alignItems: 'center'}}>
                        {currentUser?.role === 'admin' && u.ip_address && u.ip_address !== 'Unbekannt' && (
                          <button onClick={() => blockUserIp(u.ip_address)} style={{padding: '0.2rem 0.5rem', fontSize: '0.8rem', background: 'rgba(255,0,0,0.2)', border: '1px solid red', color: '#ff6b6b', borderRadius: '4px'}}>
                            IP sperren
                          </button>
                        )}
                        {currentUser?.role === 'admin' && u.username !== 'David' && <button onClick={() => deleteUser(u.id)} className="delete-btn" style={{padding: '0.2rem 0.5rem', fontSize: '0.8rem'}}>Löschen</button>}
                      </td>
                    </tr>
                  ))}
                  {filteredUsers.length === 0 && (
                    <tr>
                      <td colSpan="6" style={{padding: '1rem', textAlign: 'center', color: 'gray'}}>Keine Benutzer für diese Suche gefunden.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {currentUser?.role === 'admin' && (
              <>
                <div style={{marginTop: '3rem'}}>
                  <h3 style={{color: 'var(--color-accent-gold)', marginBottom: '1rem'}}>Blockierte E-Mail-Adressen</h3>
                  <form onSubmit={handleBlockEmail} style={{display: 'flex', gap: '1rem', marginBottom: '1.5rem'}}>
                    <input type="email" name="emailToBlock" placeholder="E-Mail zum Blockieren" required style={{padding: '0.5rem', borderRadius: '4px', border: '1px solid #444', background: 'rgba(0,0,0,0.2)', color: 'white'}} />
                    <button type="submit" className="hero-cta" style={{padding: '0.5rem 1rem'}}>Blockieren</button>
                  </form>
                  <ul className="admin-list">
                    {blockedEmails.map(b => (
                      <li key={b.id} className="admin-list-item">
                        <span>{b.email}</span>
                        <button onClick={() => unblockEmail(b.id)} className="delete-btn" style={{background: 'transparent', color: 'var(--color-accent-gold)', border: '1px solid var(--color-accent-gold)'}}>Aufheben</button>
                      </li>
                    ))}
                    {blockedEmails.length === 0 && <li style={{color: 'gray'}}>Keine blockierten E-Mails.</li>}
                  </ul>
                </div>

                <div style={{marginTop: '3rem'}}>
                  <h3 style={{color: 'var(--color-accent-gold)', marginBottom: '1rem'}}>Blockierte IP-Adressen</h3>
                  <form onSubmit={handleBlockIp} style={{display: 'flex', gap: '1rem', marginBottom: '1.5rem'}}>
                    <input type="text" name="ipToBlock" placeholder="IP-Adresse zum Blockieren" required style={{padding: '0.5rem', borderRadius: '4px', border: '1px solid #444', background: 'rgba(0,0,0,0.2)', color: 'white'}} />
                    <button type="submit" className="hero-cta" style={{padding: '0.5rem 1rem'}}>Blockieren</button>
                  </form>
                  <ul className="admin-list">
                    {blockedIps.map(b => (
                      <li key={b.id} className="admin-list-item">
                        <span>{b.ip_address}</span>
                        <button onClick={() => unblockIp(b.id)} className="delete-btn" style={{background: 'transparent', color: 'var(--color-accent-gold)', border: '1px solid var(--color-accent-gold)'}}>Aufheben</button>
                      </li>
                    ))}
                    {blockedIps.length === 0 && <li style={{color: 'gray'}}>Keine blockierten IPs.</li>}
                  </ul>
                </div>
              </>
            )}
          </div>
        )}

        {selectedSections.includes('archive') && (
          <div className="dashboard-card glass" style={{padding: '2rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
              <h3 style={{color: 'var(--color-accent-gold)'}}>Archiv-Einträge ({filteredPostcards.length})</h3>
              {['admin', 'moderator', 'user'].includes(currentUser?.role) && <button onClick={() => newItem('archive')} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>+ Neu</button>}
            </div>
            <ul className="admin-list">
              {filteredPostcards.map(pc => (
                <li key={pc.id} className="admin-list-item" style={{flexDirection: 'column', alignItems: 'flex-start', gap: '0.8rem'}}>
                  <div style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span style={{fontWeight: 'bold', color: 'var(--color-accent-gold)'}}>{pc.title} <small style={{color: 'gray'}}>({pc.item_type || 'Postkarte'}{pc.year ? ` - ${pc.year}` : ''})</small></span>
                    <div className="admin-actions">
                      {['admin', 'moderator'].includes(currentUser?.role) && <button onClick={() => editItem('archive', pc.id)}>Edit</button>}
                      {currentUser?.role === 'admin' && <button onClick={() => deletePostcard(pc.id)} className="delete-btn">Del</button>}
                    </div>
                  </div>
                  {pc.description && (
                    <div style={{width: '100%', background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '4px', fontSize: '0.9rem', color: '#ddd', whiteSpace: 'pre-wrap', borderLeft: '3px solid var(--color-accent-gold)'}}>
                      {pc.description}
                    </div>
                  )}
                </li>
              ))}
              {filteredPostcards.length === 0 && <li style={{color: 'gray'}}>Keine Treffer für Archiv-Einträge.</li>}
            </ul>
          </div>
        )}

        {selectedSections.includes('timeline') && (
          <div className="dashboard-card glass" style={{padding: '2rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
              <h3 style={{color: 'var(--color-accent-gold)'}}>Timeline Ereignisse ({filteredEvents.length})</h3>
              {['admin', 'moderator', 'user'].includes(currentUser?.role) && <button onClick={() => newItem('timeline')} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>+ Neu</button>}
            </div>
            <ul className="admin-list">
              {filteredEvents.map(ev => (
                <li key={ev.id} className="admin-list-item" style={{flexDirection: 'column', alignItems: 'flex-start', gap: '0.8rem'}}>
                  <div style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span style={{fontWeight: 'bold', color: 'var(--color-accent-gold)'}}>{ev.title} {ev.event_date && <small style={{color: 'gray'}}>({ev.event_date})</small>}</span>
                    <div className="admin-actions">
                      {['admin', 'moderator'].includes(currentUser?.role) && <button onClick={() => editItem('timeline', ev.id)}>Edit</button>}
                      {currentUser?.role === 'admin' && <button onClick={() => deleteEvent(ev.id)} className="delete-btn">Del</button>}
                    </div>
                  </div>
                  {ev.content && (
                    <div style={{width: '100%', background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '4px', fontSize: '0.9rem', color: '#ddd', whiteSpace: 'pre-wrap', borderLeft: '3px solid var(--color-accent-gold)'}}>
                      {ev.content}
                    </div>
                  )}
                </li>
              ))}
              {filteredEvents.length === 0 && <li style={{color: 'gray'}}>Keine Treffer für Timeline-Ereignisse.</li>}
            </ul>
          </div>
        )}

        {selectedSections.includes('songs') && (
          <div className="dashboard-card glass" style={{padding: '2rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
              <h3 style={{color: 'var(--color-accent-gold)'}}>Historische Lieder ({filteredSongs.length})</h3>
              {['admin', 'moderator', 'user'].includes(currentUser?.role) && <button onClick={() => newItem('song')} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>+ Neu</button>}
            </div>
            <ul className="admin-list">
              {filteredSongs.map(song => (
                <li key={song.id} className="admin-list-item" style={{flexDirection: 'column', alignItems: 'flex-start', gap: '0.8rem'}}>
                  <div style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span style={{fontWeight: 'bold', color: 'var(--color-accent-gold)'}}>{song.title} {song.author && <small style={{color: 'gray'}}>({song.author})</small>}</span>
                    <div className="admin-actions">
                      {['admin', 'moderator'].includes(currentUser?.role) && <button onClick={() => editItem('song', song.id)}>Edit</button>}
                      {currentUser?.role === 'admin' && <button onClick={() => deleteSong(song.id)} className="delete-btn">Del</button>}
                    </div>
                  </div>
                  {(song.lyrics || song.history) && (
                    <div style={{width: '100%', background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '4px', fontSize: '0.9rem', color: '#ddd', whiteSpace: 'pre-wrap', borderLeft: '3px solid var(--color-accent-gold)', display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                      {song.lyrics && <div><strong style={{color: '#aaa'}}>Text:</strong><br/>{song.lyrics}</div>}
                      {song.history && <div><strong style={{color: '#aaa'}}>Hintergrund:</strong><br/>{song.history}</div>}
                    </div>
                  )}
                </li>
              ))}
              {filteredSongs.length === 0 && <li style={{color: 'gray'}}>Keine Treffer für Lieder.</li>}
            </ul>
          </div>
        )}

        {selectedSections.includes('recipes') && (
          <div className="dashboard-card glass" style={{padding: '2rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
              <h3 style={{color: 'var(--color-accent-gold)'}}>Historische Rezepte ({filteredRecipes.length})</h3>
              {['admin', 'moderator', 'user'].includes(currentUser?.role) && <button onClick={() => newItem('recipe')} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>+ Neu</button>}
            </div>
            <ul className="admin-list">
              {filteredRecipes.map(recipe => (
                <li key={recipe.id} className="admin-list-item" style={{flexDirection: 'column', alignItems: 'flex-start', gap: '0.8rem'}}>
                  <div style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span style={{fontWeight: 'bold', color: 'var(--color-accent-gold)'}}>{recipe.title} {recipe.year && <small style={{color: 'gray'}}>({recipe.year})</small>}</span>
                    <div className="admin-actions">
                      {['admin', 'moderator'].includes(currentUser?.role) && <button onClick={() => editItem('recipe', recipe.id)}>Edit</button>}
                      {currentUser?.role === 'admin' && <button onClick={() => deleteRecipe(recipe.id)} className="delete-btn">Del</button>}
                    </div>
                  </div>
                  {(recipe.ingredients || recipe.instructions || recipe.history) && (
                    <div style={{width: '100%', background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '4px', fontSize: '0.9rem', color: '#ddd', whiteSpace: 'pre-wrap', borderLeft: '3px solid var(--color-accent-gold)', display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                      {recipe.ingredients && <div><strong style={{color: '#aaa'}}>Zutaten:</strong><br/>{recipe.ingredients}</div>}
                      {recipe.instructions && <div><strong style={{color: '#aaa'}}>Zubereitung:</strong><br/>{recipe.instructions}</div>}
                      {recipe.history && <div><strong style={{color: '#aaa'}}>Hintergrund:</strong><br/>{recipe.history}</div>}
                    </div>
                  )}
                </li>
              ))}
              {filteredRecipes.length === 0 && <li style={{color: 'gray'}}>Keine Treffer für Rezepte.</li>}
            </ul>
          </div>
        )}

        {selectedSections.includes('links') && (
          <div className="dashboard-card glass" style={{padding: '2rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
              <h3 style={{color: 'var(--color-accent-gold)'}}>Links & Verweise ({filteredLinks.length})</h3>
              {currentUser?.role === 'admin' && <button onClick={() => newItem('link')} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>+ Neu</button>}
            </div>
            <ul className="admin-list">
              {filteredLinks.map(link => (
                <li key={link.id} className="admin-list-item" style={{flexDirection: 'column', alignItems: 'flex-start', gap: '0.8rem'}}>
                  <div style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span style={{fontWeight: 'bold', color: 'var(--color-accent-gold)'}}>{link.title} {link.url && <small style={{color: 'gray'}}>({link.url})</small>}</span>
                    <div className="admin-actions">
                      {currentUser?.role === 'admin' && <button onClick={() => editItem('link', link.id)}>Edit</button>}
                      {currentUser?.role === 'admin' && <button onClick={() => deleteLink(link.id)} className="delete-btn">Del</button>}
                    </div>
                  </div>
                  {link.description && (
                    <div style={{width: '100%', background: 'rgba(0,0,0,0.3)', padding: '0.8rem', borderRadius: '4px', fontSize: '0.9rem', color: '#ddd', whiteSpace: 'pre-wrap', borderLeft: '3px solid var(--color-accent-gold)'}}>
                      {link.description}
                    </div>
                  )}
                </li>
              ))}
              {filteredLinks.length === 0 && <li style={{color: 'gray'}}>Keine Treffer für Links.</li>}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Admin;
