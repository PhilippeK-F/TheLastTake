import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "Personnes analysées": df["personne"].nunique(),
        "Films analysés": df["film"].nunique(),
        "Note moyenne": f"{df['note_tmdb'].mean():.2f}",
        "Période": f"{df['annee'].min()} — {df['annee'].max()}",
    }


def films_par_statut(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("statut_carriere")
        .agg(nb_films=("film", "count"), note_moyenne=("note_tmdb", "mean"))
        .reset_index()
        .sort_values("nb_films", ascending=False)
    )


def evolution_carriere(df: pd.DataFrame, personne: str) -> pd.DataFrame:
    return (
        df[df["personne"] == personne]
        .groupby("annee")
        .agg(note_moyenne=("note_tmdb", "mean"), nb_films=("film", "count"))
        .reset_index()
        .sort_values("annee")
    )


def top_films_par_personne(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.sort_values("note_tmdb", ascending=False)
        .groupby("personne")
        .first()
        .reset_index()[["personne", "film", "annee", "note_tmdb", "cas"]]
    )


def films_par_cas(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("cas")
        .agg(nb_films=("film", "count"), note_moyenne=("note_tmdb", "mean"))
        .reset_index()
        .sort_values("nb_films", ascending=False)
    )


def note_avant_apres_pic(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["personne", "statut_carriere"])
        .agg(note_moyenne=("note_tmdb", "mean"), nb_films=("film", "count"))
        .reset_index()
    )


def films_par_decennie(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("decennie")
        .agg(nb_films=("film", "count"), note_moyenne=("note_tmdb", "mean"))
        .reset_index()
        .sort_values("decennie")
    )