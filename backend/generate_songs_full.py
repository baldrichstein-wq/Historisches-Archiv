import json

song_data = [
    ("Ich hatt' einen Kameraden", "Ludwig Uhland", 1809, """Ich hatt' einen Kameraden,
Einen bessern findst du nit.
Die Trommel schlug zum Streite,
Er ging an meiner Seite
In gleichem Schritt und Tritt.

Eine Kugel kam geflogen:
Gilt's mir oder gilt es dir?
Ihn hat es weggerissen,
Er liegt zu meinen Füßen
Als wär's ein Stück von mir.

Will mir die Hand noch reichen,
Derweil ich eben lad'.
"Kann dir die Hand nicht geben,
Bleib du im ew'gen Leben
Mein guter Kamerad!\""""),

    ("Lützows wilde Jagd", "Carl Theodor Körner", 1813, """Was glänzt dort vom Walde im Sonnenschein?
Hör's näher und näher brausen.
Es zieht sich hinunter in dunklen Reih'n,
Und gellende Hörner erschallen darein,
Und erfüllen die Seele mit Grausen.
Und wenn ihr die schwarzen Gesellen fragt:
Das ist Lützows wilde verwegene Jagd!

Was streift dort rasch durch den finstern Wald
Und streift von Bergen zu Bergen?
Es legt sich in nächtlichen Hinterhalt,
Das Hurra jauchzt und die Büchse knallt,
Es fallen die fränkischen Schergen.
Und wenn ihr die schwarzen Gesellen fragt:
Das ist Lützows wilde verwegene Jagd!

Die wilde Jagd und die deutsche Jagd
Auf Henkersblut und Tyrannen!
Drum, die ihr uns liebt, nicht geweint und geklagt!
Das Land ist ja frei und der Morgen tagt,
Wenn wir's auch nur sterbend gewannen.
Und von Enkeln zu Enkeln sei's nachgesagt:
Das war Lützows wilde verwegene Jagd!"""),

    ("Was ist des Deutschen Vaterland?", "Ernst Moritz Arndt", 1813, """Was ist des Deutschen Vaterland?
Ist's Preußenland? Ist's Schwabenland?
Ist's, wo am Rhein die Rebe blüht?
Ist's, wo am Belt die Möwe zieht?
O nein, nein, nein!
Sein Vaterland muss größer sein!

Was ist des Deutschen Vaterland?
Ist's Bayerland? Ist's Steierland?
Ist's, wo des Marsen Rind sich streckt?
Ist's, wo der Märker Eisen reckt?
O nein, nein, nein!
Sein Vaterland muss größer sein!

Was ist des Deutschen Vaterland?
So nenne mir das große Land!
Gewiss, es ist das Österreich,
An Ehren und an Siegen reich?
O nein, nein, nein!
Sein Vaterland muss größer sein!

Was ist des Deutschen Vaterland?
So nenne endlich mir das Land!
So weit die deutsche Zunge klingt
Und Gott im Himmel Lieder singt,
Das soll es sein!
Das, wackrer Deutscher, nenne dein!

Das ist des Deutschen Vaterland,
Wo Eide schwört der Druck der Hand,
Wo Treue hell vom Auge blitzt,
Und Liebe warm im Herzen sitzt.
Das soll es sein!
Das, wackrer Deutscher, nenne dein!"""),

    ("Die Gedanken sind frei", "Unbekannt", 1780, """Die Gedanken sind frei, wer kann sie erraten,
sie fliegen vorbei wie nächtliche Schatten.
Kein Mensch kann sie wissen, kein Jäger erschießen
mit Pulver und Blei: Die Gedanken sind frei!

Ich denke was ich will und was mich beglücket,
doch alles in der Still', und wie es sich schicket.
Mein Wunsch und Begehren kann niemand mir wehren,
es bleibet dabei: Die Gedanken sind frei!

Und sperrt man mich ein im finsteren Kerker,
das alles sind rein vergebliche Werke.
Denn meine Gedanken zerreißen die Schranken
und Mauern entzwei: Die Gedanken sind frei!

Drum will ich auf immer den Sorgen entsagen
und will mich auch nimmer mit Grillen mehr plagen.
Man kann ja im Herzen stets lachen und scherzen
und denken dabei: Die Gedanken sind frei!"""),

    ("Der Mond ist aufgegangen", "Matthias Claudius", 1779, """Der Mond ist aufgegangen,
die goldnen Sternlein prangen
am Himmel hell und klar;
der Wald steht schwarz und schweiget,
und aus den Wiesen steiget
der weiße Nebel wunderbar.

Wie ist die Welt so stille,
und in der Dämm'rung Hülle
so traulich und so hold!
Als eine stille Kammer,
wo ihr des Tages Jammer
verschlafen und vergessen sollt.

Seht ihr den Mond dort stehen?
Er ist nur halb zu sehen,
und ist doch rund und schön!
So sind wohl manche Sachen,
die wir getrost belachen,
weil unsre Augen sie nicht sehn.

Wir stolzen Menschenkinder
sind eitel arme Sünder
und wissen gar nicht viel;
wir spinnen Luftgespinste
und suchen viele Künste
und kommen weiter von dem Ziel.

So legt euch denn, ihr Brüder,
in Gottes Namen nieder;
kalt ist der Abendhauch.
Verschon uns, Gott, mit Strafen,
und lass uns ruhig schlafen!
Und unsern kranken Nachbarn auch!"""),

    ("Am Brunnen vor dem Tore", "Wilhelm Müller", 1822, """Am Brunnen vor dem Tore,
Da steht ein Lindenbaum:
Ich träumt' in seinem Schatten
So manchen süßen Traum.

Ich schnitt in seine Rinde
So manches liebe Wort;
Es zog in Freud und Leide
Zu ihm mich immer fort.

Ich musst' auch heute wandern
Vorbei in tiefer Nacht,
Da hab ich noch im Dunkel
Die Augen zugemacht.

Und seine Zweige rauschten,
Als riefen sie mir zu:
Komm her zu mir, Geselle,
Hier findst du deine Ruh!

Die kalten Winde bliesen
Mir grad in's Angesicht;
Der Hut flog mir vom Kopfe,
Ich wendete mich nicht.

Nun bin ich manche Stunde
Entfernt von jenem Ort,
Und immer hör ich's rauschen:
Du fändest Ruhe dort!"""),

    ("Das Wandern ist des Müllers Lust", "Wilhelm Müller", 1821, """Das Wandern ist des Müllers Lust,
Das Wandern!
Das muss ein schlechter Müller sein,
Dem niemals fiel das Wandern ein,
Das Wandern.

Vom Wasser haben wir's gelernt,
Vom Wasser!
Das hat nicht Rast bei Tag und Nacht,
Ist stets auf Wanderschaft bedacht,
Das Wasser.

Das sehn wir auch den Rädern ab,
Den Rädern!
Die gar nicht gerne stille stehn,
Die sich mein Tag nicht müde drehn,
Die Räder.

Die Steine selbst, so schwer sie sind,
Die Steine!
Sie tanzen mit den muntern Reihn
Und wollen gar noch schneller sein,
Die Steine.

O Wandern, Wandern, meine Lust,
O Wandern!
Herr Meister und Frau Meisterin,
Lasst mich in Frieden weiterziehn
Und wandern."""),

    ("Kein schöner Land in dieser Zeit", "Anton Wilhelm von Zuccalmaglio", 1840, """Kein schöner Land in dieser Zeit,
Als hier das unsre weit und breit,
Wo wir uns finden wohl unter Linden
Zur Abendzeit, zur Abendzeit.

Da haben wir so manche Stund'
Gesessen da in froher Rund',
Und taten singen, die Lieder klingen
Im Eichengrund, im Eichengrund.

Dass wir uns hier in diesem Tal
Noch treffen so viel hundertmal,
Gott mag es schenken, Gott mag es lenken,
Er hat die Gnad', er hat die Gnad'.

Nun Brüder, eine gute Nacht,
Der Herr im hohen Himmel wacht!
In seiner Güten uns zu behüten,
Ist er bedacht, ist er bedacht."""),

    ("Guten Abend, gut' Nacht", "Des Knaben Wunderhorn", 1808, """Guten Abend, gut' Nacht,
mit Rosen bedacht,
mit Näglein besteckt,
schlupf unter die Deck:
Morgen früh, wenn Gott will,
wirst du wieder geweckt,
morgen früh, wenn Gott will,
wirst du wieder geweckt.

Guten Abend, gut' Nacht,
von Englein bewacht,
die zeigen im Traum
dir Christkindleins Baum:
Schlaf nun selig und süß,
schau im Traum 's Paradies,
schlaf nun selig und süß,
schau im Traum 's Paradies."""),

    ("Hoch auf dem gelben Wagen", "Rudolf Baumbach", 1878, """Hoch auf dem gelben Wagen
sitz ich beim Schwager vorn.
Vorwärts die Rosse traben,
lustig schmettert das Horn.
Felder, Wiesen und Auen,
leuchtendes Ährengold:
Ich möchte so gerne noch schauen,
aber der Wagen, der rollt.
Ich möchte so gerne noch schauen,
aber der Wagen, der rollt.

Postillion in der Schenke
füttert die Rosse im Flug.
Schäumendes Gerstengetränke
reicht mir der Wirt im Krug.
Hinter den Fensterscheiben
lacht ein Gesicht so hold.
Ich möchte so gerne noch bleiben,
aber der Wagen, der rollt.

Flöten hör ich und Geigen,
lustiges Bassgebrumm.
Junges Volk im Reigen
tanzt um die Linde herum.
Wirbelt wie Blätter im Winde,
jauchzt und lacht und tollt.
Ich bliebe so gern bei der Linde,
aber der Wagen, der rollt.

Einmal wird es heißen:
Steig aus, du bist am Ziel!
Dann muss ich Abschied nehmen
von all dem holden Spiel.
Andere mögen nun fahren,
ich habe meine Schuld bezollt.
Ich möchte so gerne noch bleiben,
aber der Wagen, der rollt."""),

    ("Wenn die bunten Fahnen wehen", "Hermann Löns", 1911, """Wenn die bunten Fahnen wehen,
geht die Fahrt wohl übers Meer,
wollen wir auf Kaper gehen,
rüsten wir uns schwer.
Hei, hei, heia, safari!
Geht die Fahrt wohl übers Meer.

Wir haben die Segel gehisst,
der Wind, der weht uns ins Gesicht.
Und wer kein rechter Seemann ist,
der fahre mit uns nicht.
Hei, hei, heia, safari!
Der fahre mit uns nicht.

Und kommen wir nach Madagaskar,
und haben wir das Gold an Bord,
dann trinken wir den besten Wein,
an jenem schönen Ort.
Hei, hei, heia, safari!
An jenem schönen Ort."""),

    ("Im Frühtau zu Berge", "Schwedisches Volkslied", 1900, """Im Frühtau zu Berge wir ziehn, fallera,
Es grünen alle Wälder, alle Höhn, fallera.
Wir wandern ohne Sorgen
Singend in den Morgen,
Noch ehe im Tale die Hähne krähn.

Ihr alten und hochweisen Leut', fallera,
Ihr denkt wohl, wir wären nicht gescheit, fallera?
Wer sollte aber singen,
Wenn wir schon Grillen fingen
In dieser so herrlichen Frühlingszeit?

Werft ab alle Sorgen und Pein, fallera,
Und wandert mit uns in den Tag hinein, fallera!
Wir sind hinausgegangen,
Den Sonnenschein zu fangen:
Kommt mit und lasst all eure Sorgen sein!"""),

    ("Wir lieben die Stürme", "Unbekannt", 1900, """Wir lieben die Stürme, die brausenden Wogen,
Der eiskalten Winde raues Gesicht.
Wir sind schon der Meere so viele gezogen,
Und dennoch sank unsre Fahne nicht.
Heio, heio, heio, heio, heioho, heio, heio, heioho!

Unser Schiff, das gleitet durch die Wellen,
Es trotzt der Gefahr und der dunklen Nacht.
Wir sind des Meeres wilde Gesellen,
Haben so manche Schlacht schon mitgemacht.
Heio, heio, heio, heio, heioho, heio, heio, heioho!

Und ruft uns der Tod in das kühle Grab,
So sinken wir still in die Fluten hinab.
Wir haben das Leben so herrlich genossen,
Wir haben als freie Piraten geschlossen.
Heio, heio, heio, heio, heioho, heio, heio, heioho!"""),

    ("Mein Vater war ein Wandersmann", "Unbekannt", 1800, """Mein Vater war ein Wandersmann,
Und mir steckt's auch im Blut;
Drum wandr' ich flott, so lang ich kann,
Und schwenke meinen Hut.
Faleri, falera, faleri,
Falera ha ha ha ha ha ha
Faleri, falera,
Und schwenke meinen Hut!

Das Wandern ist ein schöner Brauch,
Es macht die Seele frei;
Die Sorgen und den Kummer auch,
Wirft man gar leicht vorbei.
Faleri, falera...

Und find' ich ein feins Liebchen dann,
Am sonnigen Gestad',
So nehm' ich's mit als Wandersmann,
Auf meinem Wanderpfad.
Faleri, falera..."""),

    ("Es klappert die Mühle am rauschenden Bach", "Ernst Anschütz", 1824, """Es klappert die Mühle am rauschenden Bach,
Klipp klapp!
Bei Tag und bei Nacht ist der Müller stets wach,
Klipp klapp!
Er mahlet das Korn zu dem kräftigen Brot,
Und haben wir dieses, so hat's keine Not.
Klipp klapp, klipp klapp, klipp klapp!

Flink laufen die Räder und drehen den Stein,
Klipp klapp!
Und mahlen den Weizen zu Mehl uns so fein,
Klipp klapp!
Der Bäcker dann bäckt uns den Kuchen daraus,
Der kommt auf den Tisch dann im fröhlichen Haus.
Klipp klapp, klipp klapp, klipp klapp!

Wenn reichliche Körner das Ackerfeld trägt,
Klipp klapp!
Die Mühle dann flink ihre Räder bewegt,
Klipp klapp!
Und schenkt uns der Himmel nur immerdar Brot,
So sind wir geborgen und leiden nicht Not.
Klipp klapp, klipp klapp, klipp klapp!"""),

    ("Alle Vögel sind schon da", "Hoffmann von Fallersleben", 1835, """Alle Vögel sind schon da,
Alle Vögel, alle!
Welch ein Singen, Musiziern,
Pfeifen, Zwitschern, Tiriliern!
Frühling will nun einmarschiern,
Kommt mit Sang und Schalle.

Wie sie alle lustig sind,
Flink und froh sich regen!
Amsel, Drossel, Fink und Star
Und die ganze Vogelschar
Wünschen dir ein frohes Jahr,
Lauter Heil und Segen.

Was sie uns verkünden nun,
Nehmen wir zu Herzen:
Wir auch wollen lustig sein,
Lustig wie die Vögelein,
Hier und dort, feldaus, feldein,
Singen, springen, scherzen."""),

    ("Kuckuck, Kuckuck, ruft's aus dem Wald", "Hoffmann von Fallersleben", 1835, """Kuckuck, Kuckuck, ruft's aus dem Wald.
Lasset uns singen,
Tanzen und springen!
Frühling, Frühling wird es nun bald!

Kuckuck, Kuckuck, lässt nicht sein Schrei'n:
Komm in die Felder,
Wiesen und Wälder!
Frühling, Frühling, stelle dich ein!

Kuckuck, Kuckuck, trefflicher Held!
Was du gesungen,
Ist dir gelungen:
Winter, Winter räumet das Feld!"""),

    ("O Tannenbaum", "Ernst Anschütz", 1824, """O Tannenbaum, o Tannenbaum,
wie treu sind deine Blätter!
Du grünst nicht nur zur Sommerzeit,
nein, auch im Winter, wenn es schneit.
O Tannenbaum, o Tannenbaum,
wie treu sind deine Blätter!

O Tannenbaum, o Tannenbaum,
du kannst mir sehr gefallen!
Wie oft hat nicht zur Weihnachtszeit
ein Baum von dir mich hoch erfreut!
O Tannenbaum, o Tannenbaum,
du kannst mir sehr gefallen!

O Tannenbaum, o Tannenbaum,
dein Kleid will mich was lehren:
Die Hoffnung und Beständigkeit
gibt Trost und Kraft zu jeder Zeit.
O Tannenbaum, o Tannenbaum,
dein Kleid will mich was lehren."""),

    ("In einem kühlen Grunde", "Joseph von Eichendorff", 1807, """In einem kühlen Grunde
Da geht ein Mühlenrad,
Mein Liebchen ist verschwunden,
Das dort gewohnet hat.

Sie hat mir Treu versprochen,
Gab mir ein'n Ring dabei,
Sie hat die Treu gebrochen,
Mein Ringlein sprang entzwei.

Ich möcht als Spielmann reisen
Weit in die Welt hinaus,
Und singen meine Weisen,
Und gehn von Haus zu Haus.

Ich möcht als Reiter fliegen
Wohl in die blut'ge Schlacht,
Um stille Feuer liegen
Im Feld bei dunkler Nacht.

Hör ich das Mühlrad gehen:
Ich weiß nicht, was ich will -
Ich möcht am liebsten sterben,
Da wär's auf einmal still!"""),

    ("Sah ein Knab' ein Röslein stehn", "Johann Wolfgang von Goethe", 1771, """Sah ein Knab' ein Röslein stehn,
Röslein auf der Heiden,
War so jung und morgenschön,
Lief er schnell, es nah zu sehn,
Sah's mit vielen Freuden.
Röslein, Röslein, Röslein rot,
Röslein auf der Heiden.

Knabe sprach: Ich breche dich,
Röslein auf der Heiden!
Röslein sprach: Ich steche dich,
Dass du ewig denkst an mich,
Und ich will's nicht leiden.
Röslein, Röslein, Röslein rot,
Röslein auf der Heiden.

Und der wilde Knabe brach
's Röslein auf der Heiden;
Röslein wehrte sich und stach,
Half ihr doch kein Weh und Ach,
Musst' es eben leiden.
Röslein, Röslein, Röslein rot,
Röslein auf der Heiden."""),
    
    ("Fuchs, du hast die Gans gestohlen", "Ernst Anschütz", 1824, """Fuchs, du hast die Gans gestohlen,
Gib sie wieder her!
Gib sie wieder her!
Sonst wird dich der Jäger holen,
Mit dem Schießgewehr.
Sonst wird dich der Jäger holen,
Mit dem Schießgewehr.

Seine große, lange Flinte
Schießt auf dich den Schrot,
Schießt auf dich den Schrot,
Dass dich färbt die rote Tinte,
Und dann bist du tot.
Dass dich färbt die rote Tinte,
Und dann bist du tot.

Liebes Füchslein, lass dir raten,
Sei doch nur kein Dieb;
Sei doch nur kein Dieb;
Nimm, du brauchst nicht Gänsebraten,
Mit der Maus vorlieb.
Nimm, du brauchst nicht Gänsebraten,
Mit der Maus vorlieb."""),

    ("Lili Marleen", "Hans Leip / Norbert Schultze", 1915, """Vor der Kaserne
Vor dem großen Tor
Stand eine Laterne
Und steht sie noch davor
So woll'n wir uns da wieder seh'n
Bei der Laterne wollen wir steh'n
Wie einst Lili Marleen.
Wie einst Lili Marleen.

Unsere beide Schatten
Sah'n wie einer aus
Dass wir so lieb uns hatten
Das sah man gleich daraus
Und alle Leute soll'n es seh'n
Wenn wir bei der Laterne steh'n
Wie einst Lili Marleen.
Wie einst Lili Marleen.

Schon rief der Posten,
Sie blasen Zapfenstreich
Das kann drei Tage kosten
Kam'rad, ich komm sogleich
Da sagten wir auf Wiedersehen
Wie gerne wollt ich mit dir geh'n
Mit dir Lili Marleen.
Mit dir Lili Marleen.

Deine Schritte kennt sie,
Deinen zieren Gang
Alle Abend brennt sie,
Doch mich vergaß sie lang
Und sollte mir ein Leid gescheh'n
Wer wird bei der Laterne steh'n
Mit dir Lili Marleen?
Mit dir Lili Marleen?

Aus dem stillen Raume,
Aus der Erde Grund
Hebt mich wie im Traume
Dein verliebter Mund
Wenn sich die späten Nebel drehn
Werd' ich bei der Laterne steh'n
Wie einst Lili Marleen.
Wie einst Lili Marleen."""),

    ("Sag mir, wo die Blumen sind", "Pete Seeger / Max Colpet", 1955, """Sag mir, wo die Blumen sind,
wo sind sie geblieben?
Sag mir, wo die Blumen sind,
was ist geschehen?
Sag mir, wo die Blumen sind,
Mädchen pflückten sie geschwind.
Wann wird man je verstehen?
Wann wird man je verstehen?

Sag mir, wo die Mädchen sind,
wo sind sie geblieben?
Sag mir, wo die Mädchen sind,
was ist geschehen?
Sag mir, wo die Mädchen sind,
Männer nahmen sie geschwind.
Wann wird man je verstehen?
Wann wird man je verstehen?

Sag mir, wo die Männer sind,
wo sind sie geblieben?
Sag mir, wo die Männer sind,
was ist geschehen?
Sag mir, wo die Männer sind,
zogen fort, der Krieg beginnt.
Wann wird man je verstehen?
Wann wird man je verstehen?

Sag mir, wo die Soldaten sind,
wo sind sie geblieben?
Sag mir, wo die Soldaten sind,
was ist geschehen?
Sag mir, wo die Soldaten sind,
über Gräbern weht der Wind.
Wann wird man je verstehen?
Wann wird man je verstehen?

Sag mir, wo die Gräber sind,
wo sind sie geblieben?
Sag mir, wo die Gräber sind,
was ist geschehen?
Sag mir, wo die Gräber sind,
Blumen wehen im Sommerwind.
Wann wird man je verstehen?
Wann wird man je verstehen?

Sag mir, wo die Blumen sind,
wo sind sie geblieben?
Sag mir, wo die Blumen sind,
was ist geschehen?
Sag mir, wo die Blumen sind,
Mädchen pflückten sie geschwind.
Wann wird man je verstehen?
Wann wird man je verstehen?"""),

    ("God Save the King", "Traditional", 1745, "Vereinigtes Königreich", "Englisch", """God save our gracious King,
Long live our noble King,
God save the King!
Send him victorious,
Happy and glorious,
Long to reign over us,
God save the King!

O Lord our God arise,
Scatter his enemies
And make them fall;
Confound their politics,
Frustrate their knavish tricks,
On Thee our hopes we fix,
God save us all!

Thy choicest gifts in store
On him be pleased to pour,
Long may he reign;
May he defend our laws,
And ever give us cause
To sing with heart and voice,
God save the King!"""),

    ("It's a Long Way to Tipperary", "Jack Judge", 1912, "Vereinigtes Königreich", "Englisch", """Up to mighty London came an Irishman one day,
As the streets are paved with gold, sure ev'ryone was gay;
Singing songs of Piccadilly, Strand and Leicester Square,
Till Paddy got excited, then he shouted to them there:

It's a long way to Tipperary,
It's a long way to go.
It's a long way to Tipperary
To the sweetest girl I know!
Goodbye, Piccadilly,
Farewell, Leicester Square!
It's a long long way to Tipperary,
But my heart's right there.

Paddy wrote a letter to his Irish Molly O',
Saying, "Should you not receive it, write and let me know!
If I make mistakes in spelling, Molly dear", said he,
"Remember it's the pen that's bad, don't lay the blame on me."

It's a long way to Tipperary...

Molly wrote a neat reply to Irish Paddy O',
Saying, "Mike Maloney wants to marry me, and so
Leave the Strand and Piccadilly, or you'll be to blame,
For love has fairly drove me silly, hoping you're the same!"

It's a long way to Tipperary..."""),

    ("Auld Lang Syne", "Robert Burns", 1788, "Schottland", "Englisch", """Should auld acquaintance be forgot,
And never brought to mind?
Should auld acquaintance be forgot,
And auld lang syne!

For auld lang syne, my jo,
For auld lang syne,
We'll tak a cup o' kindness yet,
For auld lang syne.

And surely ye'll be your pint-stowp!
And surely I'll be mine!
And we'll tak a cup o' kindness yet,
For auld lang syne.

For auld lang syne, my jo,
For auld lang syne,
We'll tak a cup o' kindness yet,
For auld lang syne."""),

    ("La Marseillaise", "Claude Joseph Rouget de Lisle", 1792, "Frankreich", "Französisch", """Allons enfants de la Patrie,
Le jour de gloire est arrivé!
Contre nous de la tyrannie
L'étendard sanglant est levé,
L'étendard sanglant est levé,
Entendez-vous dans les campagnes
Mugir ces féroces soldats?
Ils viennent jusque dans vos bras
Égorger vos fils, vos compagnes!

Aux armes, citoyens,
Formez vos bataillons,
Marchons, marchons!
Qu'un sang impur
Abreuve nos sillons!

Amour sacré de la Patrie,
Conduis, soutiens nos bras vengeurs
Liberté, Liberté chérie,
Combats avec tes défenseurs!
Combats avec tes défenseurs!
Sous nos drapeaux que la victoire
Accoure à tes mâles accents,
Que tes ennemis expirants
Voient ton triomphe et notre gloire!

Aux armes, citoyens,
Formez vos bataillons,
Marchons, marchons!
Qu'un sang impur
Abreuve nos sillons!"""),

    ("Le Chant de l'Oignon", "Traditional", 1800, "Frankreich", "Französisch", """J'aime l'oignon frit à l'huile,
J'aime l'oignon quand il est bon.
J'aime l'oignon frit à l'huile,
J'aime l'oignon, j'aime l'oignon.

Au pas camarades, au pas camarades,
Au pas, au pas, au pas,
Au pas camarades, au pas camarades,
Au pas, au pas, au pas.

Un seul oignon frit à l'huile,
Un seul oignon nous rend lions.
Un seul oignon frit à l'huile,
Un seul oignon nous rend lions.

Au pas camarades, au pas camarades,
Au pas, au pas, au pas,
Au pas camarades, au pas camarades,
Au pas, au pas, au pas.

Mais pas d'oignons aux Autrichiens,
Non pas d'oignons à tous ces chiens.
Mais pas d'oignons aux Autrichiens,
Non pas d'oignons, non pas d'oignons.

Au pas camarades, au pas camarades,
Au pas, au pas, au pas,
Au pas camarades, au pas camarades,
Au pas, au pas, au pas."""),

    ("La Madelon", "Camille Robert / Louis Bousquet", 1914, "Frankreich", "Französisch", """Pour le repos, le plaisir du militaire,
Il est là-bas à deux pas de la forêt
Une maison aux murs tout couverts de lierre
Aux Tourlourous c'est le nom du cabaret.
La servante est jeune et gentille,
Légère comme un papillon.
Comme son vin son œil pétille,
Nous l'appelons la Madelon.
Nous en rêvons la nuit, nous y pensons le jour,
Ce n'est que la Madelon, mais pour nous c'est l'amour.

Quand Madelon vient nous servir à boire,
Sous la tonnelle on frôle son jupon,
Et chacun lui raconte une histoire,
Une histoire à sa façon.
La Madelon pour nous n'est pas sévère,
Quand on lui prend la taille ou le menton,
Elle rit, c'est tout le mal qu'elle sait faire,
Madelon, Madelon, Madelon!""")
]

result = []
for item in song_data:
    if len(item) == 4:
        title, author, year, lyrics = item
        origin, language = "Deutschland", "Deutsch"
    else:
        title, author, year, origin, language, lyrics = item
        
    result.append({
        "title": title,
        "author": author,
        "year": year,
        "lyrics": lyrics,
        "origin": origin,
        "language": language
    })

with open('backend/songs_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
