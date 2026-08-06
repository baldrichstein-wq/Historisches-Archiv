import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Recipe, Category, User

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/historisches_archiv.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

admin = db.query(User).filter_user(username="admin").first() if hasattr(User, 'filter_user') else db.query(User).filter(User.username == "admin").first()
cat = db.query(Category).filter(Category.name == "Rezepte").first()

new_recipes = [
    {
        "title": "Gaisburger Marsch",
        "ingredients": "500g Rindfleisch (Siedefleisch), 1 L Rinderbrühe, 300g Kartoffeln, 200g Spätzle, 2 Zwiebeln, 2 EL Butter, Schnittlauch, Salz, Pfeffer.",
        "instructions": "Rindfleisch in der Brühe weich kochen und in Würfel schneiden. Kartoffeln würfeln und in der Brühe garen. Spätzle separat kochen und hinzufügen. Zwiebeln in Ringe schneiden, in Butter goldbraun rösten. Eintopf mit Fleisch, Spätzle und Kartoffeln mischen, mit Röstzwiebeln und Schnittlauch garnieren.",
        "history": "Ein traditioneller schwäbischer Eintopf, der angeblich im 19. Jahrhundert in Stuttgart-Gaisburg populär wurde. Soldaten auf dem Marsch kehrten gerne in die dortigen Wirtshäuser ein, um diesen herzhaften Eintopf zu essen.",
        "year": 1850,
        "country": "Deutschland"
    },
    {
        "title": "Sächsischer Sauerbraten",
        "ingredients": "1 kg Rindfleisch, 500ml Essig, 500ml Wasser, Lorbeerblätter, Nelken, Wacholderbeeren, 2 Zwiebeln, 100g Rosinen, 50g Lebkuchen (Saucenlebkuchen), 2 EL Rübensirup.",
        "instructions": "Fleisch 3-5 Tage in der Essig-Wasser-Gewürz-Marinade einlegen. Fleisch anbraten, mit Marinade ablöschen und 2 Stunden schmoren. Lebkuchen und Rosinen zur Sauce geben, mit Rübensirup süß-sauer abschmecken. Dazu Rotkohl und Klöße servieren.",
        "history": "Sauerbraten war eine beliebte Methode, um Fleisch vor der Erfindung des Kühlschranks haltbar zu machen und zähe Stücke mürbe zu bekommen. Die sächsische Variante zeichnet sich durch die süße Note von Rosinen und Lebkuchen aus.",
        "year": 1880,
        "country": "Deutschland"
    },
    {
        "title": "Falscher Hase",
        "ingredients": "500g Hackfleisch (halb Rind, halb Schwein), 1 altes Brötchen (in Milch eingeweicht), 1 Zwiebel, 1 Ei, 2 hartgekochte Eier, Senf, Salz, Pfeffer, Majoran.",
        "instructions": "Hackfleisch mit dem ausgedrückten Brötchen, Zwiebelwürfeln, rohem Ei und Gewürzen verkneten. Die Hälfte der Masse zu einem Laib formen, die hartgekochten Eier der Länge nach darauflegen und mit dem restlichen Hackfleisch abdecken. Bei 180°C ca. 60 Minuten im Ofen backen.",
        "history": "Ein klassischer Hackbraten, der im Ersten und Zweiten Weltkrieg besonders populär wurde. Der Name 'Falscher Hase' entstand, weil echter Hasenbraten in Krisenzeiten für viele unerschwinglich war, weshalb man den Braten in speziellen Hasen-Brätern formte.",
        "year": 1915,
        "country": "Deutschland"
    },
    {
        "title": "Steckrübeneintopf (Kohlrübensuppe)",
        "ingredients": "1 kg Steckrüben, 500g Kartoffeln, 2 Karotten, 1 Zwiebel, 1 L Gemüse- oder Knochenbrühe, etwas Fett oder Talg, Salz, Pfeffer, Petersilie.",
        "instructions": "Steckrüben, Kartoffeln und Karotten schälen und würfeln. Zwiebel im Fett andünsten, das Gemüse hinzugeben und mit der Brühe auffüllen. Etwa 45 Minuten weichkochen. Wenn vorhanden, etwas Speck oder Wurstreste hinzufügen. Mit Petersilie bestreuen.",
        "history": "Das Symbol des 'Steckrübenwinters' 1916/17 im Ersten Weltkrieg in Deutschland. Aufgrund massiver Missernten und der britischen Seeblockade wurde die eigentlich als Viehfutter gedachte Steckrübe zum Hauptnahrungsmittel der hungernden Bevölkerung.",
        "year": 1917,
        "country": "Deutschland"
    },
    {
        "title": "Pumpernickel-Suppe",
        "ingredients": "200g Pumpernickel, 1 L Rinderbrühe, 1 Zwiebel, 2 EL Schmalz, 100ml Sahne oder Milch, Salz, Pfeffer, Muskatnuss.",
        "instructions": "Pumpernickel zerkrümeln. Zwiebel würfeln und in Schmalz anbraten. Pumpernickelkrümel kurz mitrösten, dann mit der Brühe ablöschen. 20 Minuten köcheln lassen, bis das Brot zerfällt. Pürieren, mit Sahne verfeinern und abschmecken.",
        "history": "Ein traditionelles westfälisches Arme-Leute-Essen aus dem 19. Jahrhundert, bei dem altes, hart gewordenes Pumpernickel verwertet wurde. Es wärmte und sättigte gut an kalten Tagen.",
        "year": 1820,
        "country": "Deutschland"
    },
    {
        "title": "Himmel und Erde (Himmel un Ääd)",
        "ingredients": "500g Kartoffeln, 500g Äpfel, 2 Zwiebeln, 4 Scheiben Blutwurst (Flönz), 2 EL Butter, Salz, Zucker, Essig.",
        "instructions": "Kartoffeln schälen und kochen. Äpfel schälen, stückeln und mit etwas Wasser, Zucker und Essig zu Kompott einkochen. Kartoffeln stampfen und mit dem Apfelkompott vermengen. Zwiebeln in Ringe schneiden und in Butter rösten. Blutwurstscheiben kross anbraten und zum Stampf servieren.",
        "history": "Ein traditionelles rheinisches Gericht. Der Name stammt aus dem 18. und 19. Jahrhundert: 'Himmel' steht für die Äpfel an den Bäumen, 'Erde' für die Kartoffeln (Erdäpfel) im Boden.",
        "year": 1800,
        "country": "Deutschland"
    },
    {
        "title": "Leipziger Allerlei",
        "ingredients": "200g junge Erbsen, 200g Karotten, 200g Spargel, 100g Morcheln (oder Champignons), 100g Flusskrebsschwänze, 2 EL Butter, 2 EL Mehl, 200ml Brühe, Muskat.",
        "instructions": "Gemüse separat bissfest kochen. Aus Butter und Mehl eine Mehlschwitze herstellen, mit Brühe ablöschen. Das Gemüse, Pilze und Flusskrebse in die Sauce geben und kurz ziehen lassen. Mit Muskat abschmecken.",
        "history": "Ein berühmtes Gemüsegericht aus Sachsen, das im 19. Jahrhundert weit über Leipzig hinaus bekannt wurde. Ursprünglich ein sehr reiches Gericht mit Krebsen und Morcheln, später oft als einfaches Dosengemüse verfälscht.",
        "year": 1850,
        "country": "Deutschland"
    },
    {
        "title": "Königsberger Klopse",
        "ingredients": "500g Hackfleisch (Kalb oder halb/halb), 1 altes Brötchen, 1 Ei, 1 Zwiebel, 2 Sardellenfilets, 1 L Brühe. Sauce: 2 EL Butter, 2 EL Mehl, 2 EL Kapern, Schuss Essig oder Weißwein, 1 Eigelb, 3 EL Sahne.",
        "instructions": "Aus Hackfleisch, eingeweichtem Brötchen, Ei, Zwiebel und gehackten Sardellen Klopse formen. In heißer Brühe 15 Minuten garziehen (nicht sprudelnd kochen). Für die Sauce Butter und Mehl anschwitzen, mit etwas Kochbrühe ablöschen, Kapern und Säure zugeben. Vom Herd nehmen und mit Eigelb und Sahne legieren. Klopse in der Sauce servieren.",
        "history": "Ein preußischer Klassiker aus Ostpreußen (Königsberg). Die Verwendung von Sardellen und Kapern verlieh dem Gericht eine feine Säure und galt im 19. Jahrhundert als Zeichen gehobener bürgerlicher Küche.",
        "year": 1890,
        "country": "Deutschland"
    },
    {
        "title": "Bismarckhering",
        "ingredients": "4 frische Heringe (filetiert), 500ml Essig, 500ml Wasser, 2 EL Zucker, 2 Zwiebeln, 2 Lorbeerblätter, 1 TL Senfkörner, 1 TL Pfefferkörner.",
        "instructions": "Wasser, Essig, Zucker, Zwiebelringe und Gewürze aufkochen und abkühlen lassen. Die Heringsfilets in einem Gefäß schichten und mit dem abgekühlten Sud übergießen. Mindestens 3 Tage im Kühlen ziehen lassen.",
        "history": "Sauer eingelegter Hering, benannt nach Reichskanzler Otto von Bismarck (um 1871), der diesen Fisch angeblich sehr schätzte. Der Kaufmann Johann Wiechmann soll das Rezept als erster unter diesem Namen vermarktet haben.",
        "year": 1871,
        "country": "Deutschland"
    },
    {
        "title": "Kaiserschmarrn",
        "ingredients": "4 Eier (getrennt), 150g Mehl, 200ml Milch, 2 EL Zucker, 1 Prise Salz, 40g Rosinen, 2 EL Butter, Puderzucker zum Bestreuen.",
        "instructions": "Eigelb mit Milch, Mehl und Salz zu einem glatten Teig verrühren. Eiweiß mit Zucker steif schlagen und unterheben. Butter in einer großen Pfanne schmelzen, Teig eingießen, Rosinen darüberstreuen. Wenn die Unterseite gebräunt ist, wenden (darf brechen), dann mit zwei Gabeln in Stücke reißen. Mit Puderzucker und Zwetschgenröster servieren.",
        "history": "Ein berühmtes österreichisches Dessert, das Kaiser Franz Joseph I. von Österreich gewidmet wurde. Legenden besagen, er entstand 1854 bei der Hochzeit mit Sisi aus einem missglückten, zerrissenen Pfannkuchen.",
        "year": 1854,
        "country": "Österreich"
    },
    {
        "title": "Wiener Schnitzel",
        "ingredients": "4 dünne Kalbsschnitzel (aus der Oberschale), 2 Eier, 100g Mehl, 150g feines Paniermehl (Semmelbrösel), Butterschmalz zum Ausbacken, Salz, Zitronenspalten.",
        "instructions": "Schnitzel plattieren (ca. 4-5 mm), salzen. In Mehl wenden, durch verschlagene Eier ziehen und in Semmelbröseln wälzen (nicht andrücken). In reichlich heißem Butterschmalz schwimmend goldbraun backen, dabei die Pfanne schwenken ('soufflieren'). Mit Zitrone servieren.",
        "history": "Der absolute Klassiker der Wiener Küche. Die erste bekannte Erwähnung unter diesem exakten Namen stammt aus einem Kochbuch von 1831. Die Paniertechnik war in Österreich aber schon früher bekannt.",
        "year": 1831,
        "country": "Österreich"
    },
    {
        "title": "Tafelspitz",
        "ingredients": "1.5 kg Tafelspitz (Rind), 3 L Wasser, Rinderknochen, 2 Zwiebeln (halbiert und geröstet), 2 Karotten, 1 Sellerie, 1 Lauch, Lorbeer, Pfefferkörner, Salz.",
        "instructions": "Zwiebelhälften auf der Schnittfläche in einer Pfanne ohne Fett dunkelbraun rösten (für die Farbe der Brühe). Wasser aufkochen, Fleisch, Knochen und Gewürze zugeben. Ca. 2-3 Stunden sanft sieden (nicht kochen). Gemüse in der letzten Stunde zugeben. Fleisch gegen die Faser in Scheiben schneiden. Mit Apfelkren und Schnittlauchsauce servieren.",
        "history": "Tafelspitz galt als das Leibgericht von Kaiser Franz Joseph. In der k.u.k. Monarchie im späten 19. Jahrhundert wurde es in Wien zum Inbegriff der gepflegten Rindfleischküche.",
        "year": 1880,
        "country": "Österreich"
    },
    {
        "title": "Sachertorte",
        "ingredients": "130g Zartbitterschokolade, 130g Butter, 110g Puderzucker, 6 Eier (getrennt), 110g Zucker, 130g Mehl, 200g Marillenmarmelade (Aprikose), Schokoladenglasur.",
        "instructions": "Butter, Puderzucker und Eigelb schaumig rühren. Geschmolzene Schokolade unterrühren. Eiweiß mit Zucker steif schlagen, unterheben, Mehl vorsichtig einmelieren. In einer Springform bei 170°C ca. 55 Min. backen. Auskühlen lassen, horizontal halbieren, mit erwärmter Marillenmarmelade füllen und bestreichen. Mit Schokoladenglasur überziehen.",
        "history": "1832 von dem erst 16-jährigen Kochlehrling Franz Sacher am Hof des Fürsten Metternich in Wien erfunden, als der Chefkoch krank war und ein besonderes Dessert für Gäste verlangt wurde.",
        "year": 1832,
        "country": "Österreich"
    },
    {
        "title": "Linzer Torte",
        "ingredients": "150g Butter, 150g Zucker, 150g gemahlene Nüsse (Mandeln oder Haselnüsse), 150g Mehl, 1 Ei, 1 TL Zimt, 1 Prise Nelkenpulver, 200g Ribiselmarmelade (Johannisbeere).",
        "instructions": "Aus Butter, Zucker, Nüssen, Mehl, Ei und Gewürzen einen Mürbeteig kneten und kühlen. Zwei Drittel des Teigs in eine Springform drücken, mit Marmelade bestreichen. Den restlichen Teig zu Rollen formen und als Gitter auf die Marmelade legen. Bei 180°C ca. 45 Minuten backen.",
        "history": "Gilt als die älteste namentlich bekannte Torte der Welt (Erste Rezepte stammen aus dem 17. Jh). Im 19. Jahrhundert wurde sie im Biedermeier als Kaffeehaus-Klassiker massiv popularisiert.",
        "year": 1810,
        "country": "Österreich"
    },
    {
        "title": "Palatschinken",
        "ingredients": "2 Eier, 250ml Milch, 120g Mehl, 1 Prise Salz, 1 TL Zucker, Butter zum Backen, Marillenmarmelade zum Füllen.",
        "instructions": "Aus Eiern, Milch, Mehl, Salz und Zucker einen flüssigen Teig rühren. In einer flachen Pfanne in etwas Butter hauchdünne Fladen backen. Mit Marillenmarmelade bestreichen, einrollen und mit Puderzucker bestreuen.",
        "history": "Der Name stammt vom lateinischen 'placenta' (Kuchen) über das ungarische 'palacsinta'. Im 19. Jahrhundert wurden die feinen, dünnen Palatschinken zu einem festen Bestandteil der Wiener Mehlspeisenküche.",
        "year": 1890,
        "country": "Österreich"
    },
    {
        "title": "Beef Wellington",
        "ingredients": "800g Rinderfilet am Stück, 400g Champignons, 1 Zwiebel, 100g Gänseleberpastete (oder Trüffelpaste), 8 Scheiben Parmaschinken, 1 Rolle Blätterteig, 1 Eigelb, Senf, Butter.",
        "instructions": "Rinderfilet scharf anbraten, abkühlen lassen, mit Senf bestreichen. Pilze und Zwiebeln sehr fein hacken und ohne Fett braten, bis alle Flüssigkeit verdampft ist (Duxelles). Schinken auf Frischhaltefolie auslegen, mit Duxelles bestreichen, Filet darauflegen und fest einrollen. Kühlen. Dann in Blätterteig einschlagen, mit Eigelb bestreichen und bei 200°C backen, bis der Teig goldbraun und das Filet medium ist.",
        "history": "Das Gericht wurde angeblich anlässlich des Sieges von Arthur Wellesley, dem 1. Duke of Wellington, über Napoleon in der Schlacht bei Waterloo 1815 kreiert.",
        "year": 1815,
        "country": "England / UK"
    },
    {
        "title": "Fish and Chips",
        "ingredients": "4 Kabeljau- oder Schellfischfilets, 150g Mehl, 1 TL Backpulver, 200ml dunkles Bier (Ale), 800g mehlige Kartoffeln, Pflanzenöl oder Rindertalg zum Frittieren, Salz, Malzessig (Malt Vinegar).",
        "instructions": "Kartoffeln in dicke Stifte schneiden und zweimal frittieren: erst bei 140°C weich garen, abkühlen lassen, dann bei 180°C knusprig backen. Für den Fisch Mehl, Backpulver und Bier zu einem Ausbackteig verrühren. Fisch durch den Teig ziehen und bei 180°C goldbraun frittieren. Mit Malzessig servieren.",
        "history": "Das legendäre britische Fast-Food entstand um 1860, als die Eisenbahn frischen Fisch schnell ins Landesinnere transportieren konnte und jüdische Einwanderer die Technik des frittierten Fisches nach London brachten.",
        "year": 1860,
        "country": "England / UK"
    },
    {
        "title": "Cornish Pasty",
        "ingredients": "Für den Teig: 300g Mehl, 75g Butter, 75g Schmalz, Prise Salz, etwas Wasser. Für die Füllung: 300g Rindfleischwürfel (Skirt Steak), 1 Kartoffel, 1 Kohlrübe (Swede), 1 Zwiebel, reichlich schwarzer Pfeffer, Salz.",
        "instructions": "Mürbeteig herstellen und ruhen lassen. Füllung (alles roh und gewürfelt) kräftig mit Salz und Pfeffer würzen. Teig ausrollen (kreisförmig), Füllung auf eine Hälfte geben, zuklappen und den Rand typisch eindrehen (Crimp). Bei 190°C ca. 45 Minuten backen.",
        "history": "Die traditionelle Mahlzeit der Zinnminenarbeiter in Cornwall. Der dicke Teigrand diente als 'Griff', den man mit den schmutzigen (und teils arsenverseuchten) Händen anfassen und danach wegwerfen konnte.",
        "year": 1850,
        "country": "England / UK"
    },
    {
        "title": "Shepherd's Pie",
        "ingredients": "500g Lammhackfleisch, 1 Zwiebel, 2 Karotten, 150ml Lamm- oder Rinderbrühe, 1 EL Worcestershire-Sauce, 800g Kartoffeln, 50g Butter, Schuss Milch, Salz, Pfeffer.",
        "instructions": "Hackfleisch, Zwiebel und Karotten anbraten. Mit Brühe und Worcestershire-Sauce ablöschen und einkochen lassen, bis eine dicke Sauce entsteht. Kartoffeln kochen, mit Butter und Milch zu Püree stampfen. Fleischmasse in eine Auflaufform geben, Kartoffelpüree darüberstreichen und mit einer Gabel ein Muster ziehen. Bei 200°C backen, bis das Püree goldbraun ist.",
        "history": "Ein britischer Klassiker aus der viktorianischen Ära, um Bratenreste oder Fleischabschnitte wirtschaftlich zu verwerten. Mit Lamm heißt es Shepherd's Pie (Schäfer), mit Rindfleisch Cottage Pie.",
        "year": 1870,
        "country": "England / UK"
    },
    {
        "title": "Victoria Sponge Cake",
        "ingredients": "200g weiche Butter, 200g Zucker, 4 Eier, 200g Mehl, 1 TL Backpulver. Füllung: Erdbeermarmelade, Puderzucker zum Bestäuben. (Moderne Versionen nutzen zusätzlich geschlagene Sahne).",
        "instructions": "Butter und Zucker cremig schlagen. Eier einzeln unterrühren. Mehl und Backpulver unterheben. Teig auf zwei gleich große Springformen verteilen. Bei 180°C ca. 20-25 Minuten backen. Auskühlen lassen. Den Boden mit Marmelade bestreichen, den zweiten Kuchen daraufsetzen und mit Puderzucker bestäuben.",
        "history": "Benannt nach Queen Victoria, die nach dem Tod ihres Mannes Albert 1861 anfing, gerne Kuchen zum 'Afternoon Tea' zu essen. Das Backpulver, eine Erfindung Mitte des 19. Jahrhunderts, machte den Biskuit besonders fluffig.",
        "year": 1855,
        "country": "England / UK"
    },
    {
        "title": "Lancashire Hotpot",
        "ingredients": "500g Lammfleisch (Gulasch), 3 Lammkoteletts, 3 Zwiebeln, 800g Kartoffeln (in Scheiben), 500ml Rinderbrühe, 1 EL Butter, Salz, Pfeffer, frischer Thymian.",
        "instructions": "Zwiebeln andünsten, Fleisch anbraten. In einem Tontopf abwechselnd Fleisch, Zwiebeln und Kartoffelscheiben schichten, kräftig würzen. Die oberste Schicht müssen sich überlappende Kartoffelscheiben sein. Brühe aufgießen, Butterflöckchen auf die Kartoffeln setzen. Zugedeckt bei 160°C ca. 2 Stunden schmoren, dann ohne Deckel 30 Min. bräunen.",
        "history": "Ein herzhaftes Arbeiteressen aus den Baumwollstädten von Lancashire während der industriellen Revolution. Es wurde am Morgen in den Topf gegeben, auf kleinem Feuer stehen gelassen und war fertig, wenn die Arbeiter aus der Fabrik kamen.",
        "year": 1840,
        "country": "England / UK"
    },
    {
        "title": "Anzac Biscuits",
        "ingredients": "100g Haferflocken, 100g Mehl, 100g Zucker, 80g Kokosraspeln, 100g Butter, 2 EL heller Sirup (Golden Syrup), 1 TL Natron, 2 EL kochendes Wasser.",
        "instructions": "Trockene Zutaten (außer Natron) mischen. Butter und Sirup schmelzen. Natron im kochenden Wasser auflösen und in die Buttermischung geben (schäumt!). Flüssigkeit zu den trockenen Zutaten geben und vermengen. Kleine Kugeln formen, auf ein Blech drücken und bei 160°C ca. 15 Minuten goldbraun backen.",
        "history": "Entwickelt während des Ersten Weltkriegs von Frauen in Australien und Neuseeland für die Soldaten des ANZAC (Australian and New Zealand Army Corps). Die Kekse enthalten keine Eier und bleiben daher monatelang auf dem Seeweg haltbar.",
        "year": 1915,
        "country": "England / UK"
    },
    {
        "title": "Bouillabaisse",
        "ingredients": "1,5 kg gemischter Edelfisch (Drachenkopf, Knurrhahn, Seeteufel, etc.), 500g Muscheln, 1 Fenchel, 1 Lauch, 2 Zwiebeln, 4 Tomaten, 2 Knoblauchzehen, Orangenschale, Safran, Olivenöl, Pastis, Weißwein. Dazu: Rouille (scharfe Knoblauchmayonnaise) und geröstetes Baguette.",
        "instructions": "Gemüse in Olivenöl anschwitzen. Tomaten, Wein, Pastis, Orangenschale und Safran zugeben, aufkochen. Fischabfälle/Gräten mitkochen, dann Brühe passieren. Die festkochenden Fische zuerst in der kochenden Brühe garziehen, dann die zarteren Fische und Muscheln. Fisch und Brühe getrennt mit Baguette und Rouille servieren.",
        "history": "Ursprünglich ein simples Eintopfgericht der Fischer in Marseille aus dem späten 18. und frühen 19. Jahrhundert, in das Fische wanderten, die zu klein oder zu unansehnlich für den Verkauf waren. Mit dem Tourismus an der Côte d'Azur wurde es zum Luxusgericht.",
        "year": 1880,
        "country": "Frankreich"
    },
    {
        "title": "Coq au Vin",
        "ingredients": "1 großer Hahn (oder Hähnchen), in 8 Teile zerlegt, 1 Flasche kräftiger Rotwein (Burgunder), 200g geräucherter Speck, 250g Champignons, 15 kleine Perlzwiebeln, 2 Möhren, Bouquet Garni, Knoblauch, Butter, etwas Mehl.",
        "instructions": "Fleisch am Vortag im Rotwein marinieren. Fleisch trocken tupfen, in Butter und Speckfett anbraten. Möhren und Knoblauch mitbraten, mit etwas Mehl bestäuben, mit der Weinmarinade ablöschen. Bouquet Garni zugeben und 1,5 bis 2 Stunden sanft schmoren. Perlzwiebeln und Pilze separat in Butter glasieren und gegen Ende hinzufügen.",
        "history": "Ein urfranzösisches Gericht aus dem Burgund. Obwohl Legenden seine Herkunft bis auf Julius Cäsar zurückführen wollen, findet man in Kochbüchern Rezepte für 'Coq au Vin' erst ab dem frühen 20. Jahrhundert als Inbegriff der französischen Landküche.",
        "year": 1900,
        "country": "Frankreich"
    },
    {
        "title": "Boeuf Bourguignon",
        "ingredients": "1 kg Rindfleisch (Schulter), 1 Flasche Rotwein (Burgunder), 200g Speck, 250g Champignons, 15 Perlzwiebeln, 2 Möhren, Rinderbrühe, Bouquet Garni, Butter, Mehl.",
        "instructions": "Ähnlich wie beim Coq au Vin: Rindfleisch in große Würfel schneiden, scharf anbraten. Speck, Zwiebeln und Möhren andünsten. Fleisch mit Mehl bestäuben, mit Rotwein und etwas Brühe ablöschen. Kräuter zugeben. Im geschlossenen Topf bei 160°C im Ofen für 3 Stunden sanft schmoren lassen. Am Ende glasierte Perlzwiebeln und gebratene Pilze untermischen.",
        "history": "Ein traditionelles Schmorgericht der französischen Landbevölkerung, das im 19. Jahrhundert durch Pariser Bistros veredelt und als Klassiker der Haute Cuisine etabliert wurde (oft durch Auguste Escoffier standardisiert).",
        "year": 1890,
        "country": "Frankreich"
    },
    {
        "title": "Ratatouille",
        "ingredients": "1 Aubergine, 2 Zucchini, 1 rote Paprika, 1 gelbe Paprika, 4 große Tomaten, 2 Zwiebeln, 3 Knoblauchzehen, Olivenöl, Thymian, Rosmarin, Salz, Pfeffer.",
        "instructions": "Gemüse grob würfeln. Wichtig: Auberginen, Zucchini, Paprika und Zwiebeln nacheinander einzeln in Olivenöl anbraten und herausnehmen. Dann Tomaten, Knoblauch und Kräuter einkochen. Das gebratene Gemüse wieder zugeben und alles gemeinsam 20 Minuten sanft schmoren lassen.",
        "history": "Ein bäuerliches Gemüsegericht aus der Provence rund um Nizza. Der Name taucht Ende des 18. Jahrhunderts als Begriff für ein grobes Eintopfgericht auf, in der modernen Gemüsekombination ist es ab Ende des 19. Jahrhunderts belegt.",
        "year": 1870,
        "country": "Frankreich"
    },
    {
        "title": "Crêpes Suzette",
        "ingredients": "Für Crêpes: 250g Mehl, 4 Eier, 500ml Milch, Prise Salz, 50g flüssige Butter. Für die Sauce: 100g Butter, 100g Zucker, Saft und Schale von 2 Orangen, 5cl Grand Marnier (Orangenlikör) zum Flambieren.",
        "instructions": "Aus den Teigzutaten dünne Crêpes backen. In einer großen Pfanne Zucker karamellisieren, Butter einrühren, mit Orangensaft ablöschen und Schale zugeben. Sauce einkochen. Crêpes zu Dreiecken falten und in die Sauce legen. Grand Marnier darüber gießen und flambieren. Sofort servieren.",
        "history": "Legende: 1895 in Monte Carlo kreierte ein Kellnerlehrling dieses Gericht versehentlich, als der Likör Feuer fing. Er servierte es dem Prince of Wales (dem späteren Edward VII.), der es nach seiner schönen Begleiterin Suzette benannte.",
        "year": 1895,
        "country": "Frankreich"
    },
    {
        "title": "Quiche Lorraine",
        "ingredients": "Teig: 200g Mehl, 100g kalte Butter, 1 Ei, Prise Salz. Füllung: 200g geräucherter Speck (Lardons), 3 Eier, 200ml Crème fraîche, Salz, Pfeffer, Muskat.",
        "instructions": "Mürbeteig herstellen, 30 Min. kühlen. Teig ausrollen, in eine Tarteform geben und blindbacken (10 Min.). Speckwürfel in einer Pfanne knusprig auslassen. Eier mit Crème fraîche und Gewürzen verquirlen. Speck auf dem Teig verteilen, Eiermischung darübergießen. Bei 180°C ca. 30 Minuten backen, bis die Masse gestockt und leicht gebräunt ist.",
        "history": "Ursprünglich ein Gericht aus Lothringen (Lorraine) aus dem 16. Jahrhundert (gebaut aus Brotteig und Ei). Die Version mit Mürbeteig und Speck etablierte sich im 19. Jahrhundert in ganz Frankreich. Traditionell enthält die echte Quiche Lorraine keinen Käse!",
        "year": 1850,
        "country": "Frankreich"
    },
    {
        "title": "Cassoulet",
        "ingredients": "500g weiße Bohnen (Tarbais), 300g Schweinebauch, 300g Lammfleisch, 4 Toulouse-Würste, 2 Enten-Confit-Keulen (oder Gänse-Confit), Zwiebeln, Knoblauch, Tomatenmark, Bouquet Garni.",
        "instructions": "Bohnen über Nacht einweichen. Fleisch (Schwein, Lamm) anbraten, Zwiebeln und Knoblauch mitdünsten. Alles mit Bohnen und Brühe in einer großen Tonform (Cassole) im Ofen bei 150°C für 3-4 Stunden schmoren. Regelmäßig die sich bildende Kruste in den Eintopf drücken. Gegen Ende Würste und Enten-Confit zugeben und bräunen lassen.",
        "history": "Ein deftiger Bohneneintopf aus Südfrankreich (Toulouse, Carcassonne, Castelnaudary). Seinen Höhepunkt als Nationalgericht erreichte es im 19. Jahrhundert mit der Verbreitung der Enten-Confits.",
        "year": 1840,
        "country": "Frankreich"
    },
    {
        "title": "New England Clam Chowder",
        "ingredients": "500g Venusmuscheln (Clams, frisch oder Dose), 150g Räucherspeck, 1 Zwiebel, 2 Kartoffeln (gewürfelt), 500ml Milch, 200ml Sahne, 2 EL Butter, 2 EL Mehl, Salz, Pfeffer, Oyster Crackers.",
        "instructions": "Speck auslassen und Zwiebel darin weichdünsten. Butter und Mehl einrühren (Mehlschwitze). Mit Muschelsaft und Milch aufgießen. Kartoffeln zugeben und köcheln lassen, bis sie weich sind. Muschelfleisch und Sahne einrühren, nicht mehr kochen lassen. Mit Pfeffer abschmecken und mit Oyster Crackers servieren.",
        "history": "Die cremige weiße Muschelsuppe der Ostküste der USA. Um 1830 tauchen die ersten gedruckten Rezepte auf. Der Begriff 'Chowder' leitet sich vom französischen Kessel 'chaudière' ab, den bretonische Fischer mitbrachten.",
        "year": 1830,
        "country": "USA"
    },
    {
        "title": "Jambalaya",
        "ingredients": "200g Andouille-Wurst (oder Chorizo), 300g Hähnchenbrust, 200g Garnelen, 1 Zwiebel, 1 grüne Paprika, 2 Stangen Sellerie (Die 'Holy Trinity'), 3 Knoblauchzehen, 1 Dose Tomaten, 2 Tassen Langkornreis, Cajun-Gewürzmischung, Geflügelbrühe.",
        "instructions": "Wurst und Hähnchen anbraten. Das Gemüse (Trinity) hinzufügen und weichdünsten. Tomaten, Reis, Gewürze und Brühe hinzugeben. Abdecken und ca. 25 Minuten sanft köcheln lassen, bis der Reis gar ist. Fünf Minuten vor Ende die Garnelen unterheben.",
        "history": "Ein kreolisches/cajun-Gericht aus Louisiana. Es hat spanische (Paella) und französische Wurzeln. Im 19. Jahrhundert etablierte es sich als preiswertes und nahrhaftes Gericht, das in großen Kesseln über offenem Feuer gekocht wurde.",
        "year": 1850,
        "country": "USA"
    },
    {
        "title": "Gumbo",
        "ingredients": "200g Andouille-Wurst, 300g Garnelen, 100ml Öl, 100g Mehl (für dunkle Roux), 1 Zwiebel, 1 Paprika, Sellerie ('Holy Trinity'), Okraschoten oder Filé-Pulver zum Andicken, Hühnerbrühe, Knoblauch.",
        "instructions": "Öl und Mehl in einem Topf unter ständigem Rühren langsam bräunen, bis eine sehr dunkle Mehlschwitze (Roux) entsteht (Dauer: bis zu 30 Min.). Gemüse zugeben, Brühe angießen. Wurst zugeben und 45 Min köcheln. Okra oder Garnelen erst gegen Ende zufügen. Mit Reis servieren.",
        "history": "Ein weiteres ikonisches Gericht aus Louisiana. Der Name stammt vermutlich von einem westafrikanischen Wort für Okra ('ki ngombo'). Im späten 19. Jahrhundert wurde es zu einem Symbol der kulturellen Verschmelzung im US-Süden.",
        "year": 1880,
        "country": "USA"
    },
    {
        "title": "Waldorf Salad",
        "ingredients": "2 säuerliche Äpfel (z.B. Granny Smith), 2 Stangen Staudensellerie, 100g Walnüsse (leicht geröstet), 100g Mayonnaise, 2 EL Joghurt oder Sahne, Zitronensaft, Salz, Pfeffer, Salatblätter zur Deko.",
        "instructions": "Äpfel entkernen und mit dem Sellerie in feine Streifen (Julienne) oder Stücke schneiden. Sofort mit Zitronensaft vermengen, damit sie nicht braun werden. Mayonnaise mit Joghurt verrühren, würzen. Äpfel, Sellerie und Nüsse mit dem Dressing vermischen. Auf Salatblättern anrichten.",
        "history": "Kreiert 1893 von Oscar Tschirky, dem Maître d'hôtel des neu eröffneten Waldorf-Astoria Hotels in New York City. Das Originalrezept bestand nur aus Äpfeln, Sellerie und Mayonnaise; Walnüsse kamen erst etwas später hinzu.",
        "year": 1893,
        "country": "USA"
    },
    {
        "title": "Macaroni and Cheese",
        "ingredients": "300g Makkaroni, 3 EL Butter, 3 EL Mehl, 500ml Milch, 250g geriebener scharfer Cheddar, 50g Parmesan, Prise Muskat, Salz, Pfeffer, Semmelbrösel.",
        "instructions": "Nudeln kochen. Aus Butter und Mehl eine helle Mehlschwitze machen, mit Milch aufkochen (Béchamel). Den Käse darin schmelzen lassen. Mit Gewürzen abschmecken. Nudeln unter die Käsesauce mischen. In eine Auflaufform geben, mit Semmelbröseln bestreuen und bei 200°C überbacken.",
        "history": "Der US-Präsident Thomas Jefferson brachte die Nudelmaschine und Rezepte aus Europa mit. 1802 servierte er 'Macaroni Pie' bei einem Staatsbankett. In der US-Kultur wurde das Gericht im 19. Jahrhundert extrem populär.",
        "year": 1802,
        "country": "USA"
    },
    {
        "title": "Borschtsch",
        "ingredients": "500g Rindfleisch (mit Knochen), 4 Rote Beten, 2 Karotten, 1/4 Weißkohl, 2 Kartoffeln, 1 Zwiebel, 2 EL Tomatenmark, 2 EL Essig, Dill, saure Sahne (Smetana), Salz, Pfeffer.",
        "instructions": "Aus Fleisch und Wasser eine Brühe kochen. Rote Bete und Karotten raspeln, in Essig und etwas Tomatenmark andünsten. Kartoffeln und gewürfelten Kohl zur Fleischbrühe geben. Angedünstetes Gemüse hinzufügen. 20 Min köcheln. Fleisch in Würfel schneiden und zurückgeben. Mit viel frischem Dill und einem Klecks saurer Sahne servieren.",
        "history": "Der berühmte Rote-Bete-Eintopf der osteuropäischen und russischen Küche. Im 19. Jahrhundert wurde er sowohl auf Bauernhöfen als auch an den zaristischen Höfen hoch geschätzt und bot wichtige Vitamine im kalten Winter.",
        "year": 1850,
        "country": "Russland"
    },
    {
        "title": "Pelmeni",
        "ingredients": "Teig: 300g Mehl, 1 Ei, 100ml Wasser, Prise Salz. Füllung: 300g gemischtes Hackfleisch (Schwein, Rind), 1 Zwiebel fein gerieben, Salz, Pfeffer. Dazu: Saure Sahne, Essig.",
        "instructions": "Aus den Zutaten einen glatten Teig kneten, 30 Min ruhen lassen. Dünn ausrollen, kleine Kreise ausstechen. Einen halben Teelöffel Füllung darauf geben, zu einem Halbmond falten und die Enden zusammendrücken (Tortellini-Form). In kochendem Salzwasser garen, bis sie an der Oberfläche schwimmen. Mit Butter, Schuss Essig und saurer Sahne servieren.",
        "history": "Eine ursprünglich sibirische Teigtasche, die durch das raue Klima geprägt wurde: Pelmeni konnten im Winter draußen eingefroren und über Monate gelagert werden. Mit dem Bau der Transsibirischen Eisenbahn Ende des 19. Jahrhunderts verbreiteten sie sich im ganzen russischen Reich.",
        "year": 1890,
        "country": "Russland"
    },
    {
        "title": "Beef Stroganoff (Bœuf Stroganoff)",
        "ingredients": "500g Rinderfilet (in Streifen), 2 Zwiebeln, 300g Champignons, 2 EL Butter, 2 EL Mehl, 200ml Rinderbrühe, 150g saure Sahne (Smetana), 1 EL scharfer Senf.",
        "instructions": "Rinderfiletstreifen sehr kurz, aber scharf anbraten und aus der Pfanne nehmen. Zwiebeln und Pilze in der Butter anbraten, mit Mehl bestäuben. Brühe angießen und aufkochen. Vom Herd nehmen, saure Sahne und Senf einrühren (nicht mehr kochen lassen!). Fleisch wieder zugeben und erwärmen.",
        "history": "Kreiert von einem französischen Koch für die einflussreiche russische Adelsfamilie Stroganow im späten 19. Jahrhundert in St. Petersburg. Ein perfektes Beispiel für die franko-russische Küchenkultur jener Zeit.",
        "year": 1891,
        "country": "Russland"
    },
    {
        "title": "Blini",
        "ingredients": "200g Buchweizenmehl, 100g Weizenmehl, 15g frische Hefe, 500ml lauwarme Milch, 2 Eier (getrennt), 2 EL geschmolzene Butter, Prise Salz. Beilage: Kaviar oder Räucherlachs, saure Sahne.",
        "instructions": "Hefe in etwas Milch auflösen. Mehle mischen, mit Milch, Hefe, Eigelb und Butter zu einem flüssigen Teig rühren. Eine Stunde an einem warmen Ort gehen lassen. Eiweiß steif schlagen und unterheben. In einer gebutterten Pfanne kleine, dicke Pfannkuchen backen. Warm mit saurer Sahne und Kaviar servieren.",
        "history": "Die traditionellen russischen Pfannkuchen haben heidnische Ursprünge und symbolisierten die Sonne. Sie waren im 19. Jahrhundert das Hauptgericht während der 'Masleniza' (Butterwoche), der festlichen Woche vor der orthodoxen Fastenzeit.",
        "year": 1880,
        "country": "Russland"
    },
    {
        "title": "Ossobuco alla Milanese",
        "ingredients": "4 Kalbshaxenscheiben (mit Knochen und Mark), Mehl, 2 Zwiebeln, 2 Karotten, 1 Selleriestange, 200ml trockener Weißwein, 400ml Fleischbrühe, 2 EL Tomatenmark, Butter. Gremolata: 1 Bio-Zitrone (Schale), 2 Knoblauchzehen, viel Petersilie.",
        "instructions": "Fleisch mehlieren und in Butter anbraten. Gemüse sehr fein würfeln und mitbraten. Tomatenmark zugeben, mit Weißwein ablöschen. Brühe zugießen. Zugedeckt 2 Stunden sanft schmoren. Gremolata-Zutaten extrem fein hacken und mischen. Kurz vor dem Servieren die Gremolata über das Fleisch streuen.",
        "history": "Ein traditionelles lombardisches Gericht aus dem 19. Jahrhundert. Das Knochenmark (Osso buco = Knochen mit Loch) gilt als das absolute Highlight des Gerichts.",
        "year": 1890,
        "country": "Italien"
    },
    {
        "title": "Risotto alla Milanese",
        "ingredients": "300g Risottoreis (Carnaroli oder Arborio), 1 kleine Zwiebel, 50g Rindermark (optional), 50g Butter, 100ml trockener Weißwein, 1 L heiße Rinderbrühe, 1 Döschen Safranfäden, 80g frisch geriebener Parmesan.",
        "instructions": "Safran in etwas heißer Brühe einweichen. Zwiebeln und Rindermark in halber Butter glasig dünsten. Reis zugeben und kurz mitrösten. Mit Wein ablöschen. Heiße Brühe kelleweise zugeben und unter ständigem Rühren einkochen lassen (ca. 18 Min.). Zum Schluss Safranwasser, restliche Butter und Parmesan kräftig unterrühren ('Mantecatura').",
        "history": "Der Legende nach entstand es bereits im 16. Jh. beim Bau des Mailänder Doms. Als standardisiertes bürgerliches Rezept in Kochbüchern verfestigte es sich im frühen 19. Jahrhundert in Italien und ist die klassische Beilage zum Ossobuco.",
        "year": 1809,
        "country": "Italien"
    }
]

added = 0
for r_data in new_recipes:
    # Check if exists
    existing = db.query(Recipe).filter(Recipe.title == r_data["title"]).first()
    if not existing:
        new_r = Recipe(**r_data, owner_id=admin.id if admin else None, category_id=cat.id if cat else None)
        db.add(new_r)
        added += 1

db.commit()
print(f"Successfully seeded {added} new recipes!")
