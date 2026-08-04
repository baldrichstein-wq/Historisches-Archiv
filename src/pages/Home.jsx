import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="hero-section">
      <h1 className="hero-title">Willkommen im Historischen Archiv</h1>
      <p className="hero-subtitle">
        Entdecken Sie verborgene Geschichten, alte Postkarten und historische Dokumente,
        die unsere Vergangenheit lebendig machen.
      </p>
      <Link to="/gallery" className="hero-cta">
        Archiv betreten
      </Link>
    </div>
  );
}

export default Home;
