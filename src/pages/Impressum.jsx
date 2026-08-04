import { Link } from 'react-router-dom';

function Impressum() {
  return (
    <div className="page-container fade-in" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <div className="glass" style={{ padding: '2.5rem' }}>
        <h1 className="page-title" style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>Impressum</h1>

        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--color-accent-gold)', marginBottom: '1rem', fontSize: '1.5rem' }}>Angaben gemäß § 5 TMG</h2>
          <p>
            David Ludwig <br />
            Heiliges Kreuz 9 <br />
            99880 Waltershausen <br />
            Deutschland
          </p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--color-accent-gold)', marginBottom: '1rem', fontSize: '1.5rem' }}>Kontakt</h2>
          <p>
            Telefon: +49 (0) 123 44 55 66<br />
            E-Mail: webmaster@32meininger.de
          </p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--color-accent-gold)', marginBottom: '1rem', fontSize: '1.5rem' }}>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h2>
          <p>
            David Ludwig<br />
            Heiliges Kreuz 9<br />
            99880 Waltershausen
          </p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--color-accent-gold)', marginBottom: '1rem', fontSize: '1.5rem' }}>Haftung für Inhalte</h2>
          <p style={{ lineHeight: '1.6', marginBottom: '1rem' }}>
            Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.
          </p>
          <p style={{ lineHeight: '1.6' }}>
            Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden von entsprechenden Rechtsverletzungen werden wir diese Inhalte umgehend entfernen.
          </p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--color-accent-gold)', marginBottom: '1rem', fontSize: '1.5rem' }}>Haftung für Links</h2>
          <p style={{ lineHeight: '1.6' }}>
            Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar. Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.
          </p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--color-accent-gold)', marginBottom: '1rem', fontSize: '1.5rem' }}>Urheberrecht (Copyright)</h2>
          <p style={{ lineHeight: '1.6', marginBottom: '1rem' }}>
            Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.
          </p>
          <p style={{ lineHeight: '1.6', marginBottom: '1rem' }}>
            <strong>Besonderer Hinweis zu historischen Dokumenten:</strong><br/>
            Dieses Archiv präsentiert historische Inhalte (Schwerpunkt 1800 bis 1925), darunter historische Rezepte, Lieder, Postkarten und Dokumente. Viele dieser Originalwerke sind aufgrund ihres Alters mittlerweile <em>gemeinfrei</em> (Public Domain). Die digitale Aufbereitung, Transkription, das Webdesign und etwaige begleitende Informationstexte sind jedoch als geistiges Eigentum des Seitenbetreibers durch das Urheberrecht geschützt.
          </p>
          <p style={{ lineHeight: '1.6' }}>
            Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Inhalte umgehend entfernen.
          </p>
        </section>

        <div style={{ marginTop: '3rem', textAlign: 'center' }}>
          <Link to="/" className="hero-cta" style={{ display: 'inline-block' }}>Zurück zur Startseite</Link>
        </div>
      </div>
    </div>
  );
}

export default Impressum;
