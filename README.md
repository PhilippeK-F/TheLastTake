# TheLastTake — Analyse des carrières cinématographiques (1980–2024)

## Description

Projet data analyst personnel analysant les trajectoires de carrière d'acteurs et réalisateurs célèbres : ceux qui ont disparu après une franchise majeure, ceux qui ont connu un flop monumental, et ceux dont la carrière a progressivement décliné.

Les données sont récupérées via l'API TMDB et couvrent 15 personnalités sur la période 1980–2024.

---

## Stack technique

| Outil | Usage |
|---|---|
| Python | Pipeline de données |
| Pandas | Nettoyage et analyse |
| Matplotlib / Seaborn | Visualisations |
| Streamlit | Dashboard interactif |
| Power BI | Dashboard analytics |
| TMDB API | Source des données |
| Docker | Conteneurisation |
| GitHub | Versioning |

---

## Structure du projet

```
TheLastTake/
│
├── data/
│   ├── raw/
│   │   └── thelasttake_raw.csv         # Données brutes TMDB
│   └── processed/
│       └── thelasttake_clean.csv       # Dataset nettoyé (556 lignes, 14 colonnes)
│
├── src/
│   ├── loaders/
│   │   ├── load_csv.py
│   │   └── scraper_tmdb.py             # Scraping via API TMDB
│   └── analysis/
│       ├── clean.py
│       ├── analyze.py
│       └── visualize.py
│
├── dashboard/
│   ├── streamlit_app.py                # Dashboard Streamlit (3 onglets)
│   └── TheLastTake.pbix                # Dashboard Power BI
│
├── notebooks/
├── .env                                # Clé API TMDB (non versionnée)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Dataset

**556 films analysés** pour 15 personnalités (1980–2024).

| Colonne | Description |
|---|---|
| `personne` | Nom de l'acteur ou réalisateur |
| `type_personne` | Acteur ou Réalisateur |
| `cas` | Post-franchise / Flop / Declin / Disparu |
| `franchise_cle` | Franchise ou film déclencheur |
| `film` | Titre du film |
| `annee` | Année de sortie |
| `note_tmdb` | Note TMDB |
| `nb_votes_tmdb` | Nombre de votes TMDB |
| `popularite_tmdb` | Score de popularité TMDB |
| `annee_pic` | Année du pic de carrière |
| `annees_apres_pic` | Années écoulées depuis le pic |
| `statut_carriere` | Avant pic / Pic / Post-pic récent / Déclin |
| `decennie` | 1980s / 1990s / 2000s / 2010s / 2020s |

---

## Personnalités analysées

| Personne | Type | Cas | Franchise |
|---|---|---|---|
| Daniel Radcliffe | Acteur | Post-franchise | Harry Potter |
| Emma Watson | Acteur | Post-franchise | Harry Potter |
| Rupert Grint | Acteur | Post-franchise | Harry Potter |
| Robert Pattinson | Acteur | Post-franchise | Twilight |
| Kristen Stewart | Acteur | Post-franchise | Twilight |
| Jake Lloyd | Acteur | Post-franchise | Star Wars |
| Hayden Christensen | Acteur | Post-franchise | Star Wars |
| Mark Hamill | Acteur | Post-franchise | Star Wars |
| Justin Chatwin | Acteur | Flop | Dragon Ball Evolution |
| Taylor Kitsch | Acteur | Flop | John Carter |
| John Travolta | Acteur | Flop | Battlefield Earth |
| Macaulay Culkin | Acteur | Disparu | Home Alone |
| M. Night Shyamalan | Réalisateur | Declin | The Sixth Sense |
| Michael Cimino | Réalisateur | Flop | Heaven's Gate |
| Kevin Smith | Réalisateur | Declin | Clerks |

---

## Dashboards

### Streamlit (3 onglets)
- **Carrières** — évolution d'une carrière, note par statut, films par décennie
- **Comparaisons** — note par personne, films par cas, scatter notes dans le temps
- **Données brutes** — table complète + export CSV

### Power BI
- 3 KPI Cards : Popularité moyenne, Total films, Note TMDB moyenne
- 2 Slicers : Type de personne, Type de cas
- Line chart : Films par année par type de cas
- Bar chart : Films par personne
- Bar chart : Top films par note
- Donut : Répartition par type de cas
- Table : Détail des films

---

## Lancement

### Avec Docker

```bash
docker-compose up --build
```

Accès : **http://localhost:8502**

### Sans Docker

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py
```

### Relancer le scraping

```bash
python src/loaders/scraper_tmdb.py
python src/analysis/clean.py
```

---

## Sources

- TMDB API — **https://www.themoviedb.org**
- Presse spécialisée (Variety, The Hollywood Reporter)

---

## Principaux enseignements

1. **Les acteurs Post-franchise dominent** — 60% des films analysés viennent de franchises Harry Potter, Twilight et Star Wars
2. **Mark Hamill et John Travolta** ont les filmographies les plus longues malgré leur déclin
3. **Robert Pattinson** est un cas atypique — comeback réussi après Twilight avec des films d'auteur
4. **Les flops monumentaux** ont un impact durable — Justin Chatwin et Taylor Kitsch n'ont jamais retrouvé un rôle majeur
5. **Les réalisateurs en déclin** maintiennent une note moyenne plus stable que les acteurs

---

## Conclusion

TheLastTake met en lumière une réalité peu visible du cinéma : être associé à une franchise ou à un flop peut définir — et parfois briser — une carrière entière.

L'analyse montre que le phénomène touche aussi bien les acteurs que les réalisateurs, et que la décennie 2000s a été particulièrement marquée par ces trajectoires brisées. Certains s'en sont remis (Robert Pattinson, Hayden Christensen avec son retour dans Star Wars), d'autres non.

Ce projet pourrait être enrichi en ajoutant davantage de personnalités, en intégrant les données de box-office via l'API TMDB, et en affinant l'algorithme de détection du pic de carrière.

---

## Auteur

**Philippe Kirstetter-Fender**
Projet personnel — Data Analyst / Data Engineer
Passionné de cinéma — en recherche active d'un poste de Data Engineer en France et à l'étranger.