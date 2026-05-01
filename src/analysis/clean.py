import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    df = df.drop_duplicates()
    df = df.dropna(how="all")

    df["annee"] = pd.to_numeric(df["annee"], errors="coerce").astype("Int64")
    df["note_tmdb"] = pd.to_numeric(df["note_tmdb"], errors="coerce")
    df["nb_votes_tmdb"] = pd.to_numeric(df["nb_votes_tmdb"], errors="coerce")
    df["popularite_tmdb"] = pd.to_numeric(df["popularite_tmdb"], errors="coerce")

    for col in ["personne", "film", "cas", "franchise_cle", "type_personne"]:
        if col in df.columns:
            df[col] = df[col].str.strip()

    df = df[df["nb_votes_tmdb"] >= 10]

    df["decennie"] = df["annee"].apply(
        lambda x: "1980s" if x < 1990
        else ("1990s" if x < 2000
        else ("2000s" if x < 2010
        else ("2010s" if x < 2020
        else "2020s")))
    )

    # Calcul annee_pic uniquement si pas déjà présente
    if "annee_pic" not in df.columns:
        idx_pic = df.groupby("personne")["nb_votes_tmdb"].idxmax()
        pic_annee = df.loc[idx_pic, ["personne", "annee"]].rename(columns={"annee": "annee_pic"})
        df = df.merge(pic_annee, on="personne", how="left")

    df["annees_apres_pic"] = df["annee"] - df["annee_pic"]

    def statut(row):
        if row["annees_apres_pic"] < 0:
            return "Avant pic"
        elif row["annees_apres_pic"] == 0:
            return "Pic"
        elif row["annees_apres_pic"] <= 5:
            return "Post-pic récent"
        else:
            return "Déclin"

    df["statut_carriere"] = df.apply(statut, axis=1)

    return df


if __name__ == "__main__":
    df_raw = pd.read_csv("data/raw/thelasttake_raw.csv", encoding="utf-8-sig")
    df = clean(df_raw)
    df.to_csv("data/processed/thelasttake_clean.csv", index=False, encoding="utf-8-sig")
    print(f"Dataset nettoyé : {len(df)} lignes, {len(df.columns)} colonnes")