// Warte, bis die Seite vollständig geladen ist
document.addEventListener("DOMContentLoaded", () => {
    
    // ==========================================
    // 1. CHRONIK-BEREICH
    // ==========================================
    const chronikContainer = document.getElementById('chronik-container');
    
    // NEU: Prüfung, ob der Container existiert (verhindert Fehler auf anderen Unterseiten)
    if (chronikContainer) {
        // Die JSON-Datei abrufen
        fetch('texte/chronik.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error("Fehler beim Laden der Textdaten.");
                }
                return response.json();
            })
            .then(data => {
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
                    chronikContainer.appendChild(itemDiv);
                });
            })
            .catch(error => {
                console.error("Es gab ein Problem:", error);
                chronikContainer.innerHTML = "<p>Fehler: Chronik konnte nicht geladen werden.</p>";
            });
    }

    // ==========================================
    // 2. POSTKARTEN- & PDF-BEREICH (auf postcard.html)
    // ==========================================
    const postkartenContainer = document.getElementById('postkarten-container');
    
    if (postkartenContainer) { // Wird nur ausgeführt, wenn 'postkarten-container' existiert
        fetch('texte/postkarten.json')
            .then(response => {
                if (!response.ok) throw new Error("Fehler beim Laden der Postkarten-Daten.");
                return response.json();
            })
            .then(data => {
                data.postkarten.forEach(eintrag => {
                    const itemDiv = document.createElement('div');
                    itemDiv.classList.add('postkarten-item');
                    itemDiv.style.marginBottom = "40px";
                    itemDiv.style.paddingBottom = "20px";
                    itemDiv.style.borderBottom = "1px dashed #ccc";
                    
                    let vorschauHTML = "";

                    // Unterscheidung: Ist es ein PDF oder ein Bild?
                    if (eintrag.typ === "pdf") {
                        // Der Zusatz #toolbar=0 am Ende der URL versteckt die Download- und Drucken-Buttons in vielen Browsern.
                        // Der Download-Link wurde absichtlich entfernt, um das Speichern zu erschweren.
                        vorschauHTML = `
                        <iframe src="${eintrag.datei}#toolbar=0" width="100%" height="900px" style="border: 1px solid #ddd; margin-bottom: 10px;" oncontextmenu="return false;"></iframe>
                        `;
                    } else {
           //             vorschauHTML = `
             //               <a href="${eintrag.datei}" target="_blank">
               //                 <img src="${eintrag.datei}" alt="${eintrag.titel}" style="max-width: 100%; height: auto; border: 1px solid #ddd; display: block; margin-bottom: 10px;">
                 //           </a>
                   //     `
                   vorschauHTML = `
                   <div style='background-image: url("${eintrag.datei}"); background-size: contain; background-repeat: no-repeat; background-position: center; width: ${eintrag.width}px; height: ${eintrag.height}px; border: 1px solid #ddd; margin-bottom: 10px;' oncontextmenu="return false;"></div>
                    `;
                    }
                    

                    // Den Inhalt zusammenbauen
                    itemDiv.innerHTML = `
                        <h2 style="margin-top: 0;">${eintrag.titel}</h2>
                        ${vorschauHTML}
                        <p style="font-style: italic; color: #555;">${eintrag.beschreibung}</p>
                    `;
                    
                    // In die Seite einfügen
                    postkartenContainer.appendChild(itemDiv);
                });
            })
            .catch(error => {
                console.error("Es gab ein Problem mit den Postkarten:", error);
                postkartenContainer.innerHTML = "<p>Fehler: Postkarten und PDFs konnten nicht geladen werden.</p>";
            });
    }

    // ==========================================
    // 3. KOPIERSCHUTZ FÜR BILDER
    // ==========================================
    
    // Rechtsklick auf Bildern verhindern (Kontextmenü blockieren)
    document.addEventListener('contextmenu', function(e) {
        if (e.target.tagName === 'IMG') {
            e.preventDefault(); // Blockiert das Menü
        }
    });

    // Drag & Drop (Ziehen von Bildern) verhindern
    document.addEventListener('dragstart', function(e) {
        if (e.target.tagName === 'IMG') {
            e.preventDefault(); // Blockiert das Ziehen
        }
    }); // KORREKTUR: Fehlende schließende Klammer und Semikolon hinzugefügt

}); // KORREKTUR: Korrekter Abschluss des "DOMContentLoaded"-Listeners