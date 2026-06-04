<?php
// Prüfen, ob das Formular über die POST-Methode gesendet wurde
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // 1. Eingaben abrufen und aus Sicherheitsgründen bereinigen (verhindert das Einschleusen von Schadcode)
    $name = htmlspecialchars(trim($_POST["name"]));
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $betreff = htmlspecialchars(trim($_POST["betreff"]));
    $nachricht = htmlspecialchars(trim($_POST["nachricht"]));

    // 2. Prüfen, ob alle Felder ausgefüllt sind und die E-Mail-Adresse ein gültiges Format hat
    if (empty($name) || empty($betreff) || empty($nachricht) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo "<h1>Fehler</h1>";
        echo "<p>Bitte füllen Sie alle Felder korrekt aus und geben Sie eine gültige E-Mail-Adresse an.</p>";
        echo "<p><a href='kontakt.html'>Zurück zum Formular</a></p>";
        exit; // Skript hier abbrechen
    }

    // 3. E-Mail-Einstellungen vorbereiten
    // WICHTIG: Trage hier die E-Mail-Adresse ein, an die die Nachrichten gesendet werden sollen!
    $empfaenger = "webmaster@32meininger.de"; 
    $email_betreff = "Neue Kontaktanfrage (Archiv): " . $betreff;
    
    // Den Text der E-Mail zusammenstellen
    $email_inhalt = "Du hast eine neue Nachricht über das Kontaktformular erhalten.\n\n";
    $email_inhalt .= "Name: $name\n";
    $email_inhalt .= "E-Mail: $email\n\n";
    $email_inhalt .= "Nachricht:\n$nachricht\n";

    // E-Mail-Header (Sorgt dafür, dass Umlaute stimmen und man direkt auf die E-Mail antworten kann)
    $headers = "From: $email\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // 4. E-Mail senden und Erfolgs- oder Fehlermeldung ausgeben
    if (mail($empfaenger, $email_betreff, $email_inhalt, $headers)) {
        echo "<h1>Vielen Dank!</h1>";
        echo "<p>Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns in Kürze bei Ihnen.</p>";
        echo "<p><a href='index.html'>Zurück zur Startseite</a></p>";
    } else {
        echo "<h1>Ein Fehler ist aufgetreten</h1>";
        echo "<p>Leider gab es ein serverseitiges Problem beim Senden Ihrer Nachricht. Bitte versuchen Sie es später noch einmal.</p>";
        echo "<p><a href='kontakt.html'>Zurück zum Formular</a></p>";
    }

} else {
    // Falls jemand die Datei direkt im Browser aufruft, ohne das Formular zu nutzen
    echo "<p>Es gab ein Problem mit Ihrer Anfrage. Bitte nutzen Sie das <a href='kontakt.html'>Kontaktformular</a>.</p>";
}
?>