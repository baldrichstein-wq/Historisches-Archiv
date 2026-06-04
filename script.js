// Warte, bis die Seite vollständig geladen ist
document.addEventListener("DOMContentLoaded", () => {
    
    // Die JSON-Datei abrufen
    fetch('texte/texte.json')
        .then(response => {
            if (!response.ok) {
                throw new Error("Fehler beim Laden der Textdaten.");
            }
            return response.json();
        })
        .then(data => {
            const container = document.getElementById('chronik-container');
            
            // Jeden Eintrag aus der JSON-Datei durchgehen
            data.chronik.forEach(eintrag => {
                // Ein neues div-Element für den Eintrag erstellen
                const itemDiv = document.createElement('div');
                itemDiv.classList.add('timeline-item');
                
                // Den HTML-Inhalt des Eintrags mit <details> und <summary> füllen
                itemDiv.innerHTML = `
                    <details style="cursor: pointer; margin-bottom: 10px;">
                        <summary style="font-weight: bold; font-size: 1.1em;">
                            ${eintrag.jahr} <span class="date" style="font-weight: normal; font-size: 0.9em;">(${eintrag.datum})</span>
                        </summary>
                        <p style="margin-top: 10px;">${eintrag.text}</p>
                    </details>
                `;
                
                // Das fertige Element in den Container auf der Webseite einfügen
                container.appendChild(itemDiv);
            });
        })
        .catch(error => {
            console.error("Es gab ein Problem:", error);
            document.getElementById('chronik-container').innerHTML = "<p>Fehler: Chronik konnte nicht geladen werden.</p>";
        });
});