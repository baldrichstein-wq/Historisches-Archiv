import json

song_data = [
    ("Ich hatt' einen Kameraden", "Ludwig Uhland", 1809, "Ich hatt' einen Kameraden,\nEinen bessern findst du nit.\nDie Trommel schlug zum Streite,\nEr ging an meiner Seite\nIn gleichem Schritt und Tritt."),
    ("Lützows wilde Jagd", "Carl Theodor Körner", 1813, "Was glänzt dort vom Walde im Sonnenschein?\nHör's näher und näher brausen.\nEs zieht sich hinunter in dunklen Reih'n,\nUnd gellende Hörner erschallen darein,\nUnd erfüllen die Seele mit Grausen."),
    ("Was ist des Deutschen Vaterland?", "Ernst Moritz Arndt", 1813, "Was ist des Deutschen Vaterland?\nIst's Preußenland? Ist's Schwabenland?\nIst's, wo am Rhein die Rebe blüht?\nIst's, wo am Belt die Möwe zieht?\nO nein, nein, nein!\nSein Vaterland muss größer sein!"),
    ("Die Gedanken sind frei", "Unbekannt", 1780, "Die Gedanken sind frei, wer kann sie erraten,\nsie fliegen vorbei wie nächtliche Schatten.\nKein Mensch kann sie wissen, kein Jäger erschießen\nmit Pulver und Blei: Die Gedanken sind frei!"),
    ("Steigerlied", "Unbekannt", 1531, "Glück auf, Glück auf! Der Steiger kommt,\nund er hat sein helles Licht bei der Nacht,\nund er hat sein helles Licht bei der Nacht\nschon angezünd't, schon angezünd't."),
    ("Der Mond ist aufgegangen", "Matthias Claudius", 1779, "Der Mond ist aufgegangen,\ndie goldnen Sternlein prangen\nam Himmel hell und klar;\nder Wald steht schwarz und schweiget,\nund aus den Wiesen steiget\nder weiße Nebel wunderbar."),
    ("Am Brunnen vor dem Tore", "Wilhelm Müller", 1822, "Am Brunnen vor dem Tore\nDa steht ein Lindenbaum;\nIch träumt in seinem Schatten\nSo manchen süßen Traum."),
    ("In einem kühlen Grunde", "Joseph von Eichendorff", 1807, "In einem kühlen Grunde\nDa geht ein Mühlenrad,\nMein Liebchen ist verschwunden,\nDas dort gewohnet hat."),
    ("Sah ein Knab' ein Röslein stehn", "Johann Wolfgang von Goethe", 1771, "Sah ein Knab' ein Röslein stehn,\nRöslein auf der Heiden,\nWar so jung und morgenschön,\nLief er schnell, es nah zu sehn."),
    ("Wem Gott will rechte Gunst erweisen", "Joseph von Eichendorff", 1822, "Wem Gott will rechte Gunst erweisen,\nDen schickt er in die weite Welt;\nDem will er seine Wunder weisen\nIn Berg und Wald und Strom und Feld."),
    ("Das Wandern ist des Müllers Lust", "Wilhelm Müller", 1821, "Das Wandern ist des Müllers Lust,\nDas Wandern!\nDas muss ein schlechter Müller sein,\nDem niemals fiel das Wandern ein."),
    ("Muß i denn, muß i denn zum Städtele hinaus", "Heinrich Wagner", 1827, "Muß i denn, muß i denn zum Städtele hinaus,\nStädtele hinaus, und du, mein Schatz, bleibst hier?\nWenn i komm, wenn i komm, wenn i wiedrum komm,\nwiedrum komm, kehr i ein, mein Schatz, bei dir."),
    ("Kein schöner Land in dieser Zeit", "Anton Wilhelm von Zuccalmaglio", 1840, "Kein schöner Land in dieser Zeit,\nals hier das unsre weit und breit,\nwo wir uns finden wohl unter Linden\nzur Abendzeit."),
    ("Guten Abend, gut' Nacht", "Des Knaben Wunderhorn", 1808, "Guten Abend, gut' Nacht,\nmit Rosen bedacht,\nmit Näglein besteckt,\nschlupf unter die Deck."),
    ("Ein Jäger aus Kurpfalz", "Unbekannt", 1763, "Ein Jäger aus Kurpfalz,\nDer reitet durch den grünen Wald,\nEr schießt das Wild daher,\nGleich wie es ihm gefällt."),
    ("Hoch auf dem gelben Wagen", "Rudolf Baumbach", 1878, "Hoch auf dem gelben Wagen\nSitz ich beim Schwager vorn.\nVorwärts die Rosse traben,\nLustig schmettert das Horn."),
    ("Wenn die bunten Fahnen wehen", "Hermann Löns", 1911, "Wenn die bunten Fahnen wehen,\nGeht die Fahrt wohl übers Meer,\nWollen wir auf Kaper gehen,\nRüsten wir uns schwer."),
    ("Schwarzbraun ist die Haselnuss", "Unbekannt", 1830, "Schwarzbraun ist die Haselnuss,\nSchwarzbraun bin auch ich, ja bin auch ich;\nSchwarzbraun muss mein Mädel sein,\nGerade so wie ich."),
    ("Im Frühtau zu Berge", "Unbekannt", 1900, "Im Frühtau zu Berge wir ziehn, fallera,\nEs grünen alle Wälder, alle Höhn, fallera."),
    ("Wir lieben die Stürme", "Unbekannt", 1900, "Wir lieben die Stürme, die brausenden Wogen,\nDer eiskalten Winde raues Gesicht;\nWir sind schon der Meere so viele gezogen,\nUnd dennoch sank unsre Fahne nicht."),
    ("Wahre Freundschaft soll nicht wanken", "Unbekannt", 1700, "Wahre Freundschaft soll nicht wanken,\nWenn man gleich entfernet ist;\nLebe fort in den Gedanken\nUnd der treuen Liebesfrist."),
    ("Auf der Lüneburger Heide", "Hermann Löns", 1911, "Auf der Lüneburger Heide,\nIn dem wunderschönen Land,\nGing ich auf und ging ich unter,\nAllerlei am Weg ich fand."),
    ("Ein Vogel wollte Hochzeit machen", "Unbekannt", 1600, "Ein Vogel wollte Hochzeit machen\nIn dem grünen Walde.\nFidirallala, fidirallala, fidirallalalala!"),
    ("Die Affen rasen durch den Wald", "Unbekannt", 1900, "Die Affen rasen durch den Wald,\nDer eine macht den andern kalt,\nDie ganze Affenbande brüllt:\nWo ist die Kokosnuss?"),
    ("Mein Vater war ein Wandersmann", "Unbekannt", 1800, "Mein Vater war ein Wandersmann,\nUnd mir steckt's auch im Blut;\nDrum wandr' ich flott, so lang ich kann,\nUnd schwenke meinen Hut."),
    ("Es klappert die Mühle am rauschenden Bach", "Ernst Anschütz", 1824, "Es klappert die Mühle am rauschenden Bach,\nKlipp klapp!\nBei Tag und bei Nacht ist der Müller stets wach,\nKlipp klapp!"),
    ("Fuchs, du hast die Gans gestohlen", "Ernst Anschütz", 1824, "Fuchs, du hast die Gans gestohlen,\nGib sie wieder her!\nSonst wird dich der Jäger holen,\nMit dem Schießgewehr."),
    ("Alle Vögel sind schon da", "Hoffmann von Fallersleben", 1835, "Alle Vögel sind schon da,\nAlle Vögel, alle!\nWelch ein Singen, Musiziern,\nPfeifen, Zwitschern, Tiriliern!"),
    ("Kuckuck, Kuckuck, ruft's aus dem Wald", "Hoffmann von Fallersleben", 1835, "Kuckuck, Kuckuck, ruft's aus dem Wald.\nLasset uns singen,\nTanzen und springen!\nFrühling, Frühling wird es nun bald!"),
    ("O Tannenbaum", "Ernst Anschütz", 1824, "O Tannenbaum, o Tannenbaum,\nWie treu sind deine Blätter!\nDu grünst nicht nur zur Sommerzeit,\nNein, auch im Winter, wenn es schneit.")
]

result = []
for title, author, year, lyrics in song_data:
    result.append({
        "title": title,
        "author": author,
        "year": year,
        "lyrics": lyrics,
        "origin": "Deutschland",
        "language": "Deutsch"
    })

with open('backend/songs_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
