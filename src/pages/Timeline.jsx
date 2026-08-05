import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Timeline() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedEvents, setExpandedEvents] = useState({});

  useEffect(() => {
    fetch('http://localhost:8091/api/timeline')
      .then(response => response.json())
      .then(data => {
        setEvents(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Fehler beim Laden der Zeitstrahl-Daten:", error);
        setLoading(false);
      });
  }, []);

  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const canAdd = token && ['admin', 'moderator', 'user'].includes(userRole);

  return (
    <div>
      <header className="page-header" style={{position: 'relative'}}>
        <h1 className="page-title">Zeitstrahl</h1>
        <p className="page-description">Historische Ereignisse chronologisch sortiert.</p>
        {canAdd && (
          <div style={{marginTop: '1rem'}}>
            <Link to="/admin/new/timeline" className="hero-cta" style={{padding: '0.5rem 1rem', fontSize: '0.9rem', display: 'inline-block'}}>
              + Neues Ereignis hinzufügen
            </Link>
          </div>
        )}
      </header>
      
      {loading ? (
        <p style={{ textAlign: 'center' }}>Daten werden geladen...</p>
      ) : (
        <div className="timeline-container">
          {(() => {
            // Gruppiere Events nach Jahr
            const groupedEvents = {};
            events.forEach(event => {
              const year = event.event_date ? new Date(event.event_date).getFullYear().toString() : 'Unbekannt';
              if (!groupedEvents[year]) {
                groupedEvents[year] = [];
              }
              groupedEvents[year].push(event);
            });

            // Sortiere Jahre (aufsteigend, "Unbekannt" ganz nach hinten)
            const sortedYears = Object.keys(groupedEvents).sort((a, b) => {
              if (a === 'Unbekannt') return 1;
              if (b === 'Unbekannt') return -1;
              return parseInt(a) - parseInt(b);
            });

            const toggleEvent = (id) => {
              setExpandedEvents(prev => ({
                ...prev,
                [id]: !prev[id]
              }));
            };

            return sortedYears.map((year, index) => (
              <div key={year} className={`timeline-row ${index % 2 === 0 ? 'left' : 'right'}`}>
                <div className="timeline-date-marker">
                  {year}
                </div>
                <div className="timeline-card-wrapper" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                  {groupedEvents[year].map(event => (
                    <div 
                      key={event.id} 
                      className="timeline-content glass" 
                      style={{ width: '100%', textAlign: 'left', cursor: 'pointer', transition: 'all 0.3s ease' }}
                      onClick={() => toggleEvent(event.id)}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <h3 className="card-title" style={{ fontSize: '1.2rem', margin: 0, color: expandedEvents[event.id] ? 'var(--color-accent-gold)' : 'var(--color-text-main)', transition: 'color 0.3s ease' }}>
                          {event.title}
                        </h3>
                        <span style={{ fontSize: '1.5rem', color: 'var(--color-accent-gold)', transform: expandedEvents[event.id] ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s ease' }}>
                          ▼
                        </span>
                      </div>
                      
                      {expandedEvents[event.id] && (
                        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255, 215, 0, 0.2)' }}>
                          {event.event_date && (
                            <div className="timeline-date" style={{ marginBottom: '1rem', color: 'var(--color-accent-gold)', fontSize: '0.9rem', fontWeight: 'bold' }}>
                              Genaues Datum: {new Date(event.event_date).toLocaleDateString('de-DE')}
                            </div>
                          )}
                          <p className="card-meta" style={{ fontSize: '1.05rem', lineHeight: '1.6', margin: 0, color: 'var(--color-text-main)' }}>
                            {event.content}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ));
          })()}
        </div>
      )}
    </div>
  );
}

export default Timeline;
