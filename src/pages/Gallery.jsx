import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Gallery() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null); // null = Category Overview
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('title');
  const [selectedEras, setSelectedEras] = useState([]);

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canAdd = token && ['admin', 'moderator', 'user'].includes(userRole);

  const categories = [
    { 
      id: 'Postkarte', 
      name: 'Postkarten', 
      desc: 'Historische Ansichtskarten, Feldpost, Briefe und persönliche Korrespondenzen.', 
      icon: '✉️' 
    },
    { 
      id: 'Dokument', 
      name: 'Dokumente', 
      desc: 'Amtliche Urkunden, Ausweise, militärische Befehle und offizielle Schreiben.', 
      icon: '📜' 
    },
    { 
      id: 'Zeitschrift', 
      name: 'Zeitschriften', 
      desc: 'Historische Zeitungen, Magazine, illustrierte Blätter und Flugschriften.', 
      icon: '📰' 
    },
    { 
      id: 'Vordruck', 
      name: 'Vordrucke', 
      desc: 'Formulare, Bezugsscheine, Lebensmittelkarten, Stammkarten und Blanko-Dokumente.', 
      icon: '📋' 
    }
  ];

  const handleEraToggle = (era) => {
    setSelectedEras(prev => 
      prev.includes(era) 
        ? prev.filter(e => e !== era)
        : [...prev, era]
    );
  };

  useEffect(() => {
    fetch('http://localhost:8000/api/archive')
      .then(response => response.json())
      .then(data => {
        setItems(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Fehler beim Laden der Archiv-Daten:", error);
        setLoading(false);
      });
  }, []);

  const getCategoryCount = (catId) => {
    return items.filter(i => i.item_type === catId).length;
  };

  const filteredAndSortedItems = items.filter(item => {
    // Category filter (must match selected category)
    if (selectedCategory && item.item_type !== selectedCategory) {
      return false;
    }

    // Search query filter
    const searchLower = (searchQuery || '').toLowerCase();
    const matchesSearch = (item.title && item.title.toLowerCase().includes(searchLower)) || 
                          (item.description && item.description.toLowerCase().includes(searchLower)) ||
                          (item.item_type && item.item_type.toLowerCase().includes(searchLower));
    if (!matchesSearch) return false;

    // Era filter
    if (selectedEras.length > 0) {
      const y = item.year;
      if (!y) return false;
      const matchesEra = selectedEras.some(era => {
        if (era === 'pre1850') return y < 1850;
        if (era === '1850to1899') return y >= 1850 && y <= 1899;
        if (era === '1900to1913') return y >= 1900 && y <= 1913;
        if (era === 'ww1') return y >= 1914 && y <= 1918;
        if (era === 'post1918') return y > 1918;
        return false;
      });
      if (!matchesEra) return false;
    }

    return true;
  }).sort((a, b) => {
    if (sortBy === 'title') return (a.title || '').localeCompare(b.title || '');
    if (sortBy === 'year_asc') return (a.year || 0) - (b.year || 0);
    if (sortBy === 'year_desc') return (b.year || 0) - (a.year || 0);
    return 0;
  });

  const currentCatObj = categories.find(c => c.id === selectedCategory);

  return (
    <div>
      {/* Category Overview View (when no category is selected) */}
      {!selectedCategory ? (
        <div>
          <header className="page-header" style={{position: 'relative'}}>
            <h1 className="page-title">Das Archiv</h1>
            <p className="page-description">Wählen Sie eine Kategorie, um unsere historischen Bestände und Schätze zu durchstöbern.</p>
            {canAdd && (
              <div style={{marginTop: '1rem'}}>
                <Link to="/admin/new/archive" className="hero-cta" style={{padding: '0.5rem 1rem', fontSize: '0.9rem', display: 'inline-block'}}>
                  + Neuen Archiv-Eintrag hinzufügen
                </Link>
              </div>
            )}
          </header>

          {loading ? (
            <p style={{ textAlign: 'center' }}>Daten werden geladen...</p>
          ) : (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 280px), 1fr))',
              gap: '2rem',
              maxWidth: '1000px',
              margin: '0 auto 3rem auto',
              padding: '0 1rem'
            }}>
              {categories.map(cat => {
                const count = getCategoryCount(cat.id);
                return (
                  <div 
                    key={cat.id} 
                    className="gallery-card glass"
                    style={{
                      padding: '2.5rem 2rem',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease',
                      border: '1px solid rgba(255, 215, 0, 0.3)'
                    }}
                    onClick={() => {
                      setSelectedCategory(cat.id);
                      setSearchQuery('');
                      setSelectedEras([]);
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateY(-6px)';
                      e.currentTarget.style.borderColor = 'var(--color-accent-gold)';
                      e.currentTarget.style.boxShadow = '0 10px 25px rgba(255, 215, 0, 0.2)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.borderColor = 'rgba(255, 215, 0, 0.3)';
                      e.currentTarget.style.boxShadow = 'none';
                    }}
                  >
                    <div>
                      <div style={{ fontSize: '3.5rem', marginBottom: '1rem', textAlign: 'center' }}>
                        {cat.icon}
                      </div>
                      <h2 style={{ fontSize: '1.8rem', color: 'var(--color-accent-gold)', marginBottom: '0.8rem', textAlign: 'center' }}>
                        {cat.name}
                      </h2>
                      <p style={{ color: 'var(--color-text-main)', fontSize: '1rem', lineHeight: '1.6', textAlign: 'center', marginBottom: '1.5rem' }}>
                        {cat.desc}
                      </p>
                    </div>
                    
                    <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.1)', paddingTop: '1.2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ background: 'rgba(255, 215, 0, 0.15)', color: 'var(--color-accent-gold)', padding: '0.3rem 0.8rem', borderRadius: '12px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                        {count} {count === 1 ? 'Eintrag' : 'Einträge'}
                      </span>
                      <span style={{ color: 'var(--color-text-main)', fontWeight: 'bold', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                        Öffnen ➔
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      ) : (
        /* Category Detail View (when a category is clicked) */
        <div>
          <div style={{ maxWidth: '1000px', margin: '0 auto 1.5rem auto', padding: '0 1rem' }}>
            <button 
              onClick={() => setSelectedCategory(null)}
              className="hero-cta"
              style={{
                background: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid var(--color-border)',
                color: '#fff',
                padding: '0.5rem 1.2rem',
                fontSize: '0.9rem',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem',
                borderRadius: '8px'
              }}
            >
              ← Zurück zur Kategorie-Übersicht
            </button>
          </div>

          <header className="page-header" style={{ marginTop: '0.5rem' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>{currentCatObj?.icon}</div>
            <h1 className="page-title">{currentCatObj?.name}</h1>
            <p className="page-description">{currentCatObj?.desc}</p>
          </header>
          
          <div className="glass" style={{maxWidth: '800px', margin: '0 auto 2rem auto', padding: '1.5rem', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
            <input 
              type="text" 
              placeholder={`Schlagwortsuche in ${currentCatObj?.name}...`} 
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
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
            {categories.map(cat => (
              <button 
                key={cat.id} 
                onClick={() => {
                  setSelectedCategory(cat.id);
                  setSearchQuery('');
                  setSelectedEras([]);
                }}
                className={`hero-cta ${selectedCategory === cat.id ? 'active' : ''}`}
                style={{
                  background: selectedCategory === cat.id ? 'var(--color-accent-gold)' : 'rgba(255, 255, 255, 0.1)',
                  color: selectedCategory === cat.id ? 'black' : 'white',
                  border: '1px solid var(--color-accent-gold)',
                  padding: '0.5rem 1.2rem',
                  cursor: 'pointer',
                  borderRadius: '20px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  fontSize: '0.9rem'
                }}
              >
                <span>{cat.icon}</span> {cat.name}
              </button>
            ))}
          </div>
          
          {loading ? (
            <p style={{ textAlign: 'center' }}>Daten werden geladen...</p>
          ) : filteredAndSortedItems.length === 0 ? (
            <p style={{ textAlign: 'center', color: 'gray' }}>Keine Einträge in dieser Kategorie gefunden, die den Suchkriterien entsprechen.</p>
          ) : (
            <div className="gallery-grid">
              {filteredAndSortedItems.map(item => (
                <div key={item.id} className="gallery-card glass">
                  {item.image_url ? (
                    <div 
                      className="card-image-placeholder" 
                      style={{ 
                        backgroundImage: `url(${item.image_url})`, 
                        backgroundSize: 'cover', 
                        backgroundPosition: 'center' 
                      }}
                    ></div>
                  ) : (
                    <div className="card-image-placeholder">Kein Bild vorhanden</div>
                  )}
                  <h3 className="card-title">{item.title}</h3>
                  <p className="card-meta">
                    {item.item_type || 'Unkategorisiert'} {item.year ? `• ${item.year}` : ''}
                  </p>
                  {item.description && (
                    <p className="card-description" style={{ fontSize: '0.9em', marginTop: '10px', whiteSpace: 'pre-line' }}>
                      {item.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Gallery;
