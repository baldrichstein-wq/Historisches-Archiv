import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function RecipeDetail() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/recipes')
      .then(res => res.json())
      .then(data => {
        const found = data.find(r => r.id.toString() === id);
        setRecipe(found);
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
        <p style={{textAlign: 'center', color: 'gray'}}>Lade Rezept...</p>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="page-container fade-in">
        <div style={{textAlign: 'center', marginTop: '2rem'}}>
          <h2 style={{color: 'var(--color-accent-gold)'}}>Rezept nicht gefunden</h2>
          <Link to="/recipes" className="hero-cta" style={{display: 'inline-block', marginTop: '1rem'}}>Zurück zur Übersicht</Link>
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
        <Link to="/recipes" style={{color: 'var(--color-accent-gold)', textDecoration: 'none'}}>
          &larr; Zurück zur Rezept-Übersicht
        </Link>
        {canEdit && (
          <Link to={`/admin/edit/recipe/${recipe.id}`} className="hero-cta" style={{padding: '0.4rem 0.8rem', fontSize: '0.9rem'}}>
            ✏️ Bearbeiten
          </Link>
        )}
      </div>

      <div className="glass" style={{padding: '2rem', borderRadius: '12px'}}>
        <h1 style={{fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--color-text-main)'}}>{recipe.title}</h1>
        
        <div style={{display: 'flex', gap: '20px', fontSize: '1rem', color: 'var(--color-text-muted)', marginBottom: '2rem', flexWrap: 'wrap'}}>
          {recipe.year && <span className="timeline-date">{recipe.year}</span>}
        </div>

        {recipe.history && (
          <div style={{marginBottom: '3rem', padding: '1.5rem', background: 'rgba(255, 215, 0, 0.05)', borderRadius: '8px', borderLeft: '4px solid var(--color-accent-gold)'}}>
            <h3 style={{marginBottom: '0.8rem', color: 'var(--color-accent-gold)'}}>Historischer Kontext</h3>
            <p style={{lineHeight: '1.6', color: 'var(--color-text-main)', fontSize: '1.05rem', margin: 0}}>
              {recipe.history}
            </p>
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {recipe.ingredients && (
            <div className="recipe-ingredients">
              <h3 style={{ color: 'var(--color-text)', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>Zutaten</h3>
              <p style={{ whiteSpace: 'pre-line', lineHeight: 1.6, color: 'var(--color-text-muted)', fontSize: '1.05rem' }}>
                {recipe.ingredients}
              </p>
            </div>
          )}

          {recipe.instructions && (
            <div className="recipe-instructions">
              <h3 style={{ color: 'var(--color-text)', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>Zubereitung</h3>
              <p style={{ whiteSpace: 'pre-line', lineHeight: 1.6, color: 'var(--color-text-muted)', fontSize: '1.05rem' }}>
                {recipe.instructions}
              </p>
            </div>
          )}
        </div>

        {recipe.image_url && (
          <div style={{marginTop: '3rem'}}>
            <img src={recipe.image_url} alt={`Bild für ${recipe.title}`} style={{width: '100%', borderRadius: '8px', border: '1px solid var(--color-border)'}} />
          </div>
        )}
      </div>
    </div>
  );
}

export default RecipeDetail;
