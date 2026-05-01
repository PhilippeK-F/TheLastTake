import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = "8d3a33b23227f074de476550974c8092"
BASE_URL = "https://api.themoviedb.org/3"

PERSONNES = [
    {"nom": "Daniel Radcliffe",   "type": "Acteur",      "cas": "Post-franchise", "franchise": "Harry Potter"},
    {"nom": "Emma Watson",        "type": "Acteur",      "cas": "Post-franchise", "franchise": "Harry Potter"},
    {"nom": "Rupert Grint",       "type": "Acteur",      "cas": "Post-franchise", "franchise": "Harry Potter"},
    {"nom": "Robert Pattinson",   "type": "Acteur",      "cas": "Post-franchise", "franchise": "Twilight"},
    {"nom": "Kristen Stewart",    "type": "Acteur",      "cas": "Post-franchise", "franchise": "Twilight"},
    {"nom": "Jake Lloyd",         "type": "Acteur",      "cas": "Post-franchise", "franchise": "Star Wars"},
    {"nom": "Hayden Christensen", "type": "Acteur",      "cas": "Post-franchise", "franchise": "Star Wars"},
    {"nom": "Mark Hamill",        "type": "Acteur",      "cas": "Post-franchise", "franchise": "Star Wars"},
    {"nom": "Justin Chatwin",     "type": "Acteur",      "cas": "Flop",           "franchise": "Dragon Ball Evolution"},
    {"nom": "Taylor Kitsch",      "type": "Acteur",      "cas": "Flop",           "franchise": "John Carter"},
    {"nom": "John Travolta",      "type": "Acteur",      "cas": "Flop",           "franchise": "Battlefield Earth"},
    {"nom": "Macaulay Culkin",    "type": "Acteur",      "cas": "Disparu",        "franchise": "Home Alone"},
    {"nom": "M. Night Shyamalan", "type": "Realisateur", "cas": "Declin",         "franchise": "The Sixth Sense"},
    {"nom": "Michael Cimino",     "type": "Realisateur", "cas": "Flop",           "franchise": "Heaven's Gate"},
    {"nom": "Kevin Smith",        "type": "Realisateur", "cas": "Declin",         "franchise": "Clerks"},
]


def search_person(nom):
    url = f"{BASE_URL}/search/person"
    params = {"api_key": API_KEY, "query": nom, "language": "fr-FR"}
    r = requests.get(url, params=params)
    results = r.json().get("results", [])
    return results[0] if results else None


def get_filmography(person_id, person_type):
    url = f"{BASE_URL}/person/{person_id}/movie_credits"
    params = {"api_key": API_KEY, "language": "fr-FR"}
    r = requests.get(url, params=params)
    data = r.json()
    if person_type == "Realisateur":
        return data.get("crew", [])
    return data.get("cast", [])


def scrape_all():
    rows = []

    for personne in PERSONNES:
        print(f"Recherche : {personne['nom']}")

        result = search_person(personne["nom"])
        if not result:
            print(f"  Non trouve")
            continue

        person_id = result["id"]
        popularite = result.get("popularity", 0)

        films = get_filmography(person_id, personne["type"])
        films = [f for f in films if f.get("release_date") and len(f["release_date"]) >= 4]
        films = sorted(films, key=lambda x: x["release_date"])

        print(f"  {len(films)} films trouves")

        for film in films:
            annee = int(film["release_date"][:4])
            if annee < 1980:
                continue

            rows.append({
                "personne":        personne["nom"],
                "type_personne":   personne["type"],
                "cas":             personne["cas"],
                "franchise_cle":   personne["franchise"],
                "film":            film.get("title", ""),
                "annee":           annee,
                "note_tmdb":       film.get("vote_average"),
                "nb_votes_tmdb":   film.get("vote_count"),
                "popularite_tmdb": popularite,
                "tmdb_movie_id":   film.get("id"),
            })

        time.sleep(0.3)

    df = pd.DataFrame(rows)
    df.to_csv("data/raw/thelasttake_raw.csv", index=False, encoding="utf-8-sig")
    print(f"\nDataset brut : {len(df)} lignes sauvegardees")
    return df


if __name__ == "__main__":
    df = scrape_all()
    print(df.head(10))