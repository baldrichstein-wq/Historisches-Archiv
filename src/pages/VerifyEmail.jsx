import { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';

function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [status, setStatus] = useState('loading'); // 'loading', 'success', 'error'
  const [message, setMessage] = useState('Verifiziere E-Mail-Adresse...');

  const hasFetched = useRef(false);

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('Kein Token angegeben.');
      return;
    }

    if (hasFetched.current) return;
    hasFetched.current = true;

    fetch('http://localhost:8091/api/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token })
    })
    .then(async (res) => {
      const data = await res.json();
      if (res.ok) {
        setStatus('success');
        setMessage(data.message || 'E-Mail erfolgreich bestätigt!');
      } else {
        setStatus('error');
        setMessage(data.detail || 'Fehler bei der Verifizierung.');
      }
    })
    .catch(err => {
      console.error(err);
      setStatus('error');
      setMessage('Netzwerkfehler.');
    });
  }, [token]);

  return (
    <div className="page-container fade-in" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh'}}>
      <div className="glass" style={{padding: '3rem', textAlign: 'center', maxWidth: '500px', width: '100%'}}>
        <h2 style={{color: 'var(--color-accent-gold)', marginBottom: '1.5rem'}}>
          E-Mail Bestätigung
        </h2>
        
        <p style={{fontSize: '1.2rem', marginBottom: '2rem', color: status === 'error' ? 'red' : 'white'}}>
          {message}
        </p>

        {status === 'success' && (
          <Link to="/admin" className="hero-cta" style={{display: 'inline-block'}}>
            Zum Login
          </Link>
        )}
      </div>
    </div>
  );
}

export default VerifyEmail;
