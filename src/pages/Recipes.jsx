import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Recipes() {
  const [recipes, setRecipes] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('title');
  const [selectedEras, setSelectedEras] = useState([]);
  const [selectedCountries, setSelectedCountries] = useState([]);

  const availableCountries = [...new Set(recipes.map(r => r.country).filter(Boolean))].sort();

  const handleCountryToggle = (country) => {
    setSelectedCountries(prev => 
      prev.includes(country) 
        ? prev.filter(c => c !== country)
        : [...prev, country]
    );
  };

  const handleEraToggle = (era) => {
    setSelectedEras(prev => 
      prev.includes(era) 
        ? prev.filter(e => e !== era)
        : [...prev, era]
    );
  };

  useEffect(() => {
    fetch('http://localhost:8091/api/recipes')
      .then(res => res.json())
      .then(data => setRecipes(data))
      .catch(err => console.error(err));
  }, []);

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canAdd = token && ['admin', 'moderator', 'user'].includes(userRole);

  return (
    <div className="page-container fade-in">
      <header className="page-header" style={{position: 'relative'}}>
        <h1 className="page-title">Historische Rezepte</h1>
        <p className="page-description">Gerichte und Rationen aus der Kriegs- und Krisenzeit.</p>
        {canAdd && (
          <div style={{marginTop: '1rem'}}>
            <Link to="/admin/new/recipe" className="hero-cta" style={{padding: '0.5rem 1rem', fontSize: '0.9rem', display: 'inline-block'}}>
              + Neues Rezept hinzufügen
            </Link>
          </div>
        )}
      </header>

      <div className="glass" style={{maxWidth: '800px', margin: '0 auto 2rem auto', padding: '1.5rem', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
        <input 
          type="text" 
          placeholder="Schlagwortsuche in Titel, Zutaten oder Beschreibung..." 
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

        {availableCountries.length > 0 && (
          <div style={{marginTop: '1rem'}}>
            <label style={{color: 'var(--color-text-muted)', fontSize: '0.9rem', display: 'block', marginBottom: '0.5rem'}}>Herkunftsland:</label>
            <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
              {availableCountries.map(country => (
                <label key={country} style={{display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', color: 'var(--color-text-main)', fontSize: '0.9rem'}}>
                  <input 
                    type="checkbox" 
                    checked={selectedCountries.includes(country)}
                    onChange={() => handleCountryToggle(country)}
                  />
                  {country}
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      <div>
        {recipes.length === 0 ? (
          <p style={{textAlign: 'center', color: 'gray'}}>Noch keine Rezepte vorhanden.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, margin: '0 auto', maxWidth: '800px' }}>
            {[...recipes].filter(recipe => {
              const searchLower = (searchQuery || '').toLowerCase();
              const matchesSearch = (recipe.title && recipe.title.toLowerCase().includes(searchLower)) || 
                                    (recipe.ingredients && recipe.ingredients.toLowerCase().includes(searchLower)) ||
                                    (recipe.history && recipe.history.toLowerCase().includes(searchLower));
              
              let matchesEra = true;
              if (selectedEras.length > 0) {
                const y = recipe.year;
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

              let matchesCountry = true;
              if (selectedCountries.length > 0) {
                matchesCountry = selectedCountries.includes(recipe.country);
              }

              return matchesSearch && matchesEra && matchesCountry;
            }).sort((a, b) => {
              if (sortBy === 'title') return a.title.localeCompare(b.title);
              if (sortBy === 'year_asc') return (a.year || 0) - (b.year || 0);
              if (sortBy === 'year_desc') return (b.year || 0) - (a.year || 0);
              return 0;
            }).map((recipe) => (
              <li 
                key={recipe.id} 
                style={{
                  padding: '1rem 0',
                  borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
                }}
              >
                <Link 
                  to={`/recipes/${recipe.id}`} 
                  style={{ display: 'block', textDecoration: 'none', color: 'inherit' }}
                  onMouseEnter={(e) => { e.currentTarget.querySelector('h3').style.color = 'var(--color-accent-hover)' }}
                  onMouseLeave={(e) => { e.currentTarget.querySelector('h3').style.color = 'var(--color-text-main)' }}
                >
                  <h3 style={{ margin: 0, transition: 'color 0.2s', color: 'var(--color-text-main)', fontSize: '1.2rem' }}>
                    {recipe.title}
                  </h3>
                  <div style={{ display: 'flex', gap: '15px', fontSize: '0.85rem', color: 'var(--color-text-muted)', marginTop: '0.4rem', flexWrap: 'wrap' }}>
                    {recipe.year && <span className="timeline-date">{recipe.year}</span>}
                    {recipe.country && <span>📍 {recipe.country}</span>}
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

export default Recipes;
